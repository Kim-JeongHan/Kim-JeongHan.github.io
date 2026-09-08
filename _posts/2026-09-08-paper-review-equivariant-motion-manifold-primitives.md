---
layout: post
title: '[논문리뷰] Equivariant Motion Manifold Primitives'
date: 2026-09-08 00:00:00 +0900
slug: paper-review-equivariant-motion-manifold-primitives
render_with_liquid: false
use_math: true
categories:
- 논문리뷰
tags:
- Manifold
- Geometry
- paper-review
---

## 논문 정보

- Title: Equivariant Motion Manifold Primitives
- Authors: Byeongho Lee, Yonghyeon Lee, Seungyeon Kim, MinJun Son, Frank C. Park
- Venue / Year: Conference on Robot Learning (CoRL), 2023
- Links: [Paper](https://proceedings.mlr.press/v229/lee23a.html), [PDF](https://proceedings.mlr.press/v229/lee23a/lee23a.pdf), [Project](https://equimmp.github.io/), [Code](https://github.com/dlsfldl/EMMP-public)

## 한 줄 요약

Trajectory manifold를 저차원 latent space에 표현하고, encoder와 decoder로 task가 transformation 바뛰면 trajectory가 일관되게 바뀌어 생성되게 한 논문.

## 문제 정의

환경이 달라지거나 예상하지 못한 장애물, 새로운 제약이 생기면 기존에 학습한 movement primitive로 task를 수행하기 어려울 수 있다. 특정 task에서 학습한 움직임을 변화한 환경이나 task parameter에 맞게 일반화하는 데 한계가 있기 때문이다.

## 핵심 아이디어

저자들은 하나의 task를 수행할 수 있는 여러 trajectory가 이루는 manifold를 학습하고, 이를 latent space에 표현한 뒤 trajectory로 복원하는 방법을 제안한다.

또한 task가 갖는 대칭성을 활용해, task parameter가 변환될 때 trajectory manifold도 그에 맞게 변환되도록 한다. 예를 들어 start, goal, 장애물 등 task를 정의하는 요소들이 상대적인 기하 관계를 유지하면서 함께 translation되거나 rotation되는 경우를 생각할 수 있다. 이러한 변환이 해당 task의 대칭성에 해당한다면, 변환된 환경에서도 그에 대응하는 trajectory를 생성하고자 한다.

<img src="/assets/img/blog/paper-review-equivariant-motion-manifold-primitives/motion-manifold-overview.png" alt="물 붓기 궤적들이 이루는 manifold와 병의 배치 변화에 따른 궤적의 대칭 변환" style="width: 50%; max-width: 467px; height: auto; display: block; margin: 0 auto;">

이를 위해 다음 두 가지 방법을 제안한다.

1. Encoder는 대칭 변환에 대해 invariance를, decoder는 equivariance를 갖도록 구성해, 학습한 motion manifold가 해당 변환에 대한 equivariance를 갖도록 한다.
2. Start, goal 같은 task parameter $\tau$에 대응하는 motion manifold $\mathcal{M}_{\tau}$가 서로 homeomorphic하다고 가정한다. 이는 두 manifold 사이에 연속적인 일대일 대응이 존재하고, 그 역함수도 연속적이라는 뜻이다. 또한 $\tau$와 independent한 latent variable $z$가 존재한다고 가정해, 여러 task parameter에 걸쳐 latent space $\mathcal{Z}$와 하나의 latent distribution을 공유한다. 이를 학습하기 위해 autoencoder의 학습 loss에 independence regularization term을 추가해 independence를 유도한다.

## Method

저자들은 MMPs: Motion Manifold Primitives에서 EMMPs: Equivariant Motion Manifold Primitives로 이어지는 순서로 방법을 설명한다. MMPs에서는 motion manifold의 표현과 학습 방법을 소개하며, homeomorphic manifold 가정과 latent variable의 independence 조건을 자세히 다룬다.

### MMPs: Motion Manifold Primitives

<img src="/assets/img/blog/paper-review-equivariant-motion-manifold-primitives/task-trajectory-manifold-latent-space.png" alt="시작점과 목표점, 장애물이 주어진 task에서 가능한 궤적들이 manifold와 latent coordinate space에 대응하는 과정" style="width: 100%; max-width: 809px; height: auto; display: block; margin: 0 auto;">

Task parameter $\tau$가 달라져도, 각 $\tau$에 대응하는 trajectory manifold $\mathcal{M}_{\tau}$는 서로 homeomorphic하다고 가정한다. 이 가정은 대칭 변환으로 연결되는 경우를 포함해, 고려하는 모든 $\tau$의 manifold에 적용된다.

또한 $\tau$와 independent한 latent variable $z$가 존재한다고 가정하고, 이를 표현하는 shared latent space $\mathcal{Z}$를 찾고자 한다. 즉, 모든 $\tau$에 대해 latent distribution이 다음 조건을 만족하도록 학습한다.

$$
p(z \mid \tau) = p(z)
$$

기본 autoencoder 구성에서는 trajectory $x$와 task parameter $\tau$를 encoder $g$에 입력해 latent coordinate $z \in \mathcal{Z}$를 얻는다. Decoder $f$는 $z$와 $\tau$를 입력받아 해당 task의 trajectory $\hat{x}$를 복원한다.

$$
z = g(x, \tau),
\qquad
\hat{x} = f(z, \tau) \approx x
$$

Independence 가정을 적용한 MMP에서는 encoder를 trajectory $x$만 입력받는 $z = g(x)$ 형태로 단순화한다. Decoder에는 $\tau$를 계속 조건으로 제공해 $\hat{x} = f(z, \tau)$를 복원한다. 다만 encoder의 입력에서 $\tau$를 제외하는 것만으로 $z$와 $\tau$의 statistical independence가 보장되지는 않으므로, independence regularization term을 함께 사용해 independence를 유도한다.

$$
\mathcal{R}(\theta,\phi)
\mathrel{:=}
\frac{
\mathbb{E}_{(\cdot,x_{ij})\in\mathcal{D}}
\left[
\left\|
g_\phi(x_{ij})
-g_\phi\!\left(f_\theta(g_\phi(x_{ij}),\tau)\right)
\right\|^2
\right]
}{
\mathbb{E}_{(\cdot,x_{ij})\in\mathcal{D}}
\left[\left\|g_\phi(x_{ij})\right\|^2\right]
}
$$

여기서 $\mathcal{D}$는 task-trajectory dataset이며, $g_\phi$와 $f_\theta$는 각각 parameter $\phi$, $\theta$를 갖는 encoder와 decoder다. $\tau$는 task parameter space $\mathcal{T}$의 uniform distribution에서 새로 sample한다.

### EMMPs: Equivariant Motion Manifold Primitives

<img src="/assets/img/blog/paper-review-equivariant-motion-manifold-primitives/equivariant-manifold-transformation.png" alt="task parameter에 대칭 변환을 적용하면 trajectory manifold도 대응하는 형태로 변환되는 관계" style="width: 50%; max-width: 578px; height: auto; display: block; margin: 0 auto;">

EMMPs에서는 invariant encoder와 equivariant decoder를 설명한다. 여기서 $h \in H$는 task의 대칭 변환을 나타내며, $h \cdot (x, \tau)$는 trajectory와 task parameter에 해당 변환을 적용한 결과다. EMMP의 encoder는 대칭 변환을 처리하는 과정에서 $\tau$를 사용하므로 $g(x, \tau)$로 표기한다.

1. Invariant encoder는 $(x, \tau)$에 대칭 변환 $h$를 적용해도 동일한 latent coordinate $z$로 encoding한다.

   $$
   g\bigl(h \cdot (x, \tau)\bigr) = g(x, \tau) = z
   $$

2. Equivariant decoder는 latent coordinate $z$를 유지한 채 task parameter를 $h \cdot \tau$로 바꿔 입력하면, 원래 출력 trajectory에 대응하는 대칭 변환을 적용한 결과를 생성한다.

   $$
   f(z, h \cdot \tau)
   = \bigl[h \cdot (f(z, \tau), \tau)\bigr]_x
   $$

   여기서 $[\cdot]_x$는 변환된 trajectory와 task parameter 쌍에서 trajectory 성분을 꺼낸다는 뜻이다. Decoder의 출력은 trajectory이며, $\tau$는 입력 조건으로 주어진다.

## Experiments

### Goal-Reaching Task of a Planar Mobile Robot

<img src="/assets/img/blog/paper-review-equivariant-motion-manifold-primitives/planar-mobile-robot-task-symmetries.png" alt="십자 모양 벽을 피하는 평면 이동 로봇의 시작 위치와 벽 각도, 반사 및 회전 대칭" style="width: 70%; max-width: 691px; height: auto; display: block; margin: 0 auto;">

평면 이동 로봇이 십자 모양 벽과 충돌하지 않고, 시작점에서 가까운 두 통로 중 하나를 지나 중앙 목표점에 도달하는 trajectory를 생성하는 실험이다. 사람이 그린 demonstration trajectory로 학습한 뒤, 로봇의 시작 위치와 벽의 각도가 달라져도 task를 수행하는 경로를 생성하는지 평가한다.

### Water-Pouring Task of a Franka Panda Robot

<img src="/assets/img/blog/paper-review-equivariant-motion-manifold-primitives/water-pouring-task-symmetries.png" alt="컵 위치와 병의 초기 pose, 물의 양이 주어진 물 붓기 task와 평행이동 및 회전 대칭" style="width: 70%; max-width: 790px; height: auto; display: block; margin: 0 auto;">


Franka Panda 로봇 팔이 병을 기울여 컵에 물 150g을 붓는 실험이다. 컵 위치, 병의 초기 pose, 병에 담긴 물의 양을 task parameter로 주어 demonstration trajectory를 학습하고, 이 조건들이 달라졌을 때 생성한 물 붓기 동작의 성공 여부를 평가한다.

## 참고할 코드

https://github.com/dlsfldl/EMMP-public/blob/main/models/ae.py#L387-L457


| 구조                         | AE 방식       | VAE 방식       | 구조의 특징                     |
| -------------------------- | ----------- | ------------ | -------------------------- |
| 기본 Autoencoder             | **AE**      | **VAE**      | 입력 $x$를 압축하고 복원          |
| Motion Manifold Primitives | **MMP_AE**  | **MMP_VAE**  | decoder에 task $\tau$를 추가 |
| Equivariant MMP            | **EMMP_AE** | **EMMP_VAE** | MMP에 좌표계 변환을 추가해 대칭성 반영 |
