---
layout: post
title: 'Distances and Divergences (Total Variation Distance, KL Divergence, Wasserstein Metric)'
date: 2026-09-01 00:00:00 +0900
slug: distances-divergences
render_with_liquid: false
use_math: true
categories:
- 공부
- 확률과 통계
tags:
- probability
- statistics
---

## 00_Distances and Divergences 개요

### Distance와 Divergence의 차이

distance(metric) $d(P,Q)$는 다음 세 조건을 만족하는 분포 간의 함수이다.

1. Non-negativity와 identity of indiscernibles: $d(P,Q)\ge 0$이며, $d(P,Q)=0 \Longleftrightarrow P=Q$이다.
2. Symmetry: $d(P,Q)=d(Q,P)$이다.
3. Triangle inequality: $d(P,Q)\le d(P,R)+d(R,Q)$이다.

divergence $D(P\Vert Q)$는 첫 번째 조건의 non-negativity와 identity를 일반적으로 만족하지만, symmetry나 triangle inequality까지 요구하지 않는다. 따라서 분포의 순서가 중요할 수 있으며 metric일 필요도 없다. KL divergence가 대표적인 asymmetric divergence이다.

## 01_Total Variation Distance

### 정의

Total Variation Distance는 두 확률분포 $P$와 $Q$가 얼마나 다른지를 특정 사건 $A\in\mathcal{F}$에서의 확률 차이로 정의한다.

<div style="text-align: center;">
  <img src="/assets/img/blog/distances-divergences/total-variation-distance.png" alt="서로 다른 두 확률밀도 p(x)와 q(x), 그리고 Total Variation Distance를 나타내는 색칠 영역" style="width: 50%;">
</div>

- 연속확률분포에서의 표현 

$$
P(A)=\int_A p(x)\,dx,
\qquad
Q(A)=\int_A q(x)\,dx.
$$

$$
\delta(P,Q)
=\frac{1}{2}\int_{\mathcal{X}}\left|p(x)-q(x)\right|\,dx

$$

- 이산 확률분포에서의 표현

$$
\delta(P,Q)=\frac{1}{2}\sum_x\left|P(x)-Q(x)\right|.
$$

### 주요 성질

- Total Variation Distance는 항상 $ 0\le\delta(P,Q)\le 1
$ 을 만족한다.
- $\delta(P,Q)=0 \Longleftrightarrow P=Q$인 필요충분조건을 만족한다.즉, 두 분포가 같으면 Total Variation Distance는 0이 된다.
- Symmetry: $\delta(P,Q)=\delta(Q,P)$이다.
- Triangle inequality: $\delta(P,Q)\le\delta(P,R)+\delta(R,Q)$이다.

## 02_Kullback–Leibler Divergence

### 정의

밀도 $p,q$를 가지는 두 분포에 대해 $P$가 $Q$에 대해 absolutely continuous하다고 하자($P\ll Q$). Kullback-Leibler divergence는 $P$에서 관측한 값이 $Q$와 얼마나 다른지를 $P$를 기준으로 평균낸 값이다.

$$
D_{\mathrm{KL}}(P\Vert Q)
=\int_{\mathcal{X}}p(x)\log\left(\frac{p(x)}{q(x)}\right)\,dx
=\mathbb{E}_{X\sim P}\left[\log\left(\frac{p(X)}{q(X)}\right)\right].
$$

이산 분포에서는 다음과 같이 쓴다.

$$
D_{\mathrm{KL}}(P\Vert Q)=\sum_x P(x)\log\left(\frac{P(x)}{Q(x)}\right).
$$

### 주요 성질

1. KL divergence는 항상 음이 아닌 값을 가진다.
$$
D_{\mathrm{KL}}(P\Vert Q)\ge 0,
$$

2. KL divergence가 0이라는 의미는 확률분포 $P$와 $Q$가 같다.
$$
D_{\mathrm{KL}}(P\Vert Q)=0\Longleftrightarrow P=Q
$$

3. 비대칭성: KL divergence는 일반적으로 비대칭이다.
$$
D_{\mathrm{KL}}(P\Vert Q)\ne D_{\mathrm{KL}}(Q\Vert P)
$$

4. assymetric이며, triangle inequality를 만족하지 않으므로 metric이 아니고 divergence이다.

5. 분모가 0이면 $D_{\mathrm{KL}}(P\Vert Q)=+\infty$가 된다. 따라서 KL divergence는 두 분포의 존재하는 영역이 서로 겹치지 않으면 무한대가 된다. 이는 KL divergence가 분포의 공간적 위치를 충분히 반영하지 못한다는 것을 의미한다.

<iframe
  src="/assets/interactive/kl-divergence/"
  title="KL divergence interactive visualization"
  loading="lazy"
  style="width: 100%; height: 650px; border: 0;"
></iframe>

## 03_p-Wasserstein Distance

### 사용하는 이유

#### 1. 유사도가 낮은 분포의 공간적 거리 비교

<div style="text-align: center;">
  <img src="/assets/img/blog/distances-divergences/wasserstein-spatial-separation.png" alt="분포 P와 공간적으로 서로 다른 위치에 있는 Q1과 Q2" style="width: 100%;">
</div>

이 그림에서 $Q_2$는 $Q_1$보다 $P$에서 더 멀리 있다. 실제로 그림에서 보이는 것보다 $Q_1, Q_2$가 $P$와 거의 겹치지 않는다고 생각하면 
$$
\delta(P,Q_1) \approx \delta(P,Q_2),
\qquad
D_{\mathrm{KL}}(P\Vert Q_1) \approx D_{\mathrm{KL}}(P\Vert Q_2)
$$

가 된다. 따라서 TV distance와 KL divergence만으로는 $Q_2$가 $Q_1$보다 더 멀리 있다는 공간적 차이를 구분할 수 없다.

반면 Wasserstein Distance는 확률질량을 실제로 옮기는 Optimal Transport 문제로 다루어 그 거리를 반영한다. 그림처럼 $P$의 질량을 $Q_1$으로 옮기는 거리가 $Q_2$로 옮기는 거리보다 짧으므로

$$
W_p(P,Q_1)<W_p(P,Q_2)
$$

로 두 분포를 구분한다. 같은 모양의 분포를 각각 $c_i$만큼 평행이동하여 $Q_i$를 만든 경우에는 모든 $p\ge 1$에 대해

$$
W_p(P,Q_i)=|c_i|
$$

가 된다. 이처럼 Wasserstein Distance는 분포의 모양뿐 아니라 질량이 이동해야 하는 공간적 거리도 함께 반영한다.

#### 2. Disjoint-support issue 보완

<div style="text-align: center;">
  <img src="/assets/img/blog/distances-divergences/wasserstein-disjoint-support.png" alt="support가 서로 겹치지 않는 파란색 확률분포 P와 빨간색 확률분포 Q1" style="width: 100%;">
</div>

다음 그림은 두 분포의 support가 전혀 겹치지 않는 disjoint-support issue를 보여준다. 해당 분포를 KL divergence로 비교하면 다음과 같다.

$$
D_{\mathrm{KL}}(P\Vert Q_1)=+\infty
$$

이는 P와 Q의 분포를 KL divergence로 비교할 수 없다는 것을 의미한다. 이 문제를 no disjoint-support issue라고 한다. KL divergence는 분포의 공간적 위치를 충분히 반영하지 못한다. 따라서 support가 겹치지 않는 경우에는 KL divergence가 무한대가 되어 분포 간의 차이를 비교할 수 없다.
이때, Wasserstein Distance는 분포의 위치상의 차이도 반영하여 이 문제를 보완한다.

### Coupling과 Optimal Transport 정의

이를 수식으로 정의하면, $P$와 $Q$의 coupling들의 집합 $\Gamma(P,Q)$는 다음과 같이 정의된다. 여기서 $ \gamma \in \Gamma(P,Q)$는 $P$의 질량을 $Q$로 어떻게 옮길지를 나타내는 transport plan으로, x의 질량중 얼마를 y로 보낼지를 결정한다. Wasserstein Distance는 이 transport plan 중에서 가장 적은 비용으로 옮기는 optimal transport plan을 찾는 문제로 정의된다.

$$
W_p(P,Q)
=
\left(
\inf_{\gamma\in\Gamma(P,Q)}
\int_{\mathcal{X}\times\mathcal{X}}d(x,y)^p\,d\gamma(x,y)
\right)^{1/p},
\qquad p\ge 1
$$

### CDF와 Quantile을 이용한 1차원 Wasserstein Distance의 직관적 이해

1차원에서는 CDF을 사용하면 Wasserstein Distance를 좀더 직관적으로 이해할 수 있다. $P$의 CDF는

$$
F_P(x)=P(X\le x)
$$

이고, CDF의 inverse는

$$
F_P^{-1}(u)=\inf\{x\in\mathbb{R}:F_P(x)\ge u\},
\qquad 0<u<1
$$

로 정의한다. 아래 그림은 PDF에서의 질량 이동이 CDF에서의 어떤 의미를 지니는지를 보여준다.

<div style="text-align: center;">
  <img src="/assets/img/blog/distances-divergences/wasserstein-pdf-cdf-intuition.png" alt="PDF와 CDF에서 Wasserstein Distance를 해석하는 직관" style="width: 100%;">
</div>

왼쪽 PDF에서는 작은 확률질량 $\Delta m$을 위치 $a$에서 $b$로 옮기는 상황을 생각할 수 있다. $p=1$일 때 이 이동의 비용은 

$$
\Delta m\,|b-a|
$$

이다. 오른쪽 CDF의 그림에서 $u=0.2$ 라인을 보면, $P$와 $Q$가 이 누적확률 수준에 도달하는 위치는 각각

$$
a=F_P^{-1}(0.2),
\qquad
b=F_Q^{-1}(0.2)
$$

로 읽을 수 있다. b와 a 사이의 가로 거리는

$$
\left|F_P^{-1}(0.2)-F_Q^{-1}(0.2)\right|
$$

이다. 이를 모든 $u\in(0,1)$에서 이 가로 거리를 측정해 $u$ 방향으로 적분하면 1차원 $p$-Wasserstein Distance의 quantile 공식이 된다.

$$
W_p(P,Q)
=
\left(
\int_0^1
\left|F_P^{-1}(u)-F_Q^{-1}(u)\right|^p\,du
\right)^{1/p},
\qquad p\ge 1.
$$

역함수를 사용한 적분의 물리적 의미는 x축 방향으로 적분하는 것이 아닌 y축방향을 따라 적분하는 것이다.

특히 $p=1$인 경우에는 다음과 같은 CDF 표현도 성립한다.

$$
W_1(P,Q)
=
\int_{-\infty}^{\infty}
\left|F_P(x)-F_Q(x)\right|\,dx.
$$

$p$는 이동 비용을 얼마나 강조할지를 결정한다. $p=1$에서는 이동 거리에 비례하는 선형 비용을 사용한다. $p=2$에서는 거리의 제곱을 비용으로 사용한 뒤 마지막에 제곱근을 취하므로, 먼 거리를 이동하는 일부 질량에 더 큰 가중치를 준다. 일반적으로 $p$가 커질수록 장거리 이동에 더 민감해진다. 유한한 $p$차 모멘트를 가지는 확률분포들의 공간에서 $W_p$는 non-negativity, identity, symmetry, triangle inequality를 모두 만족하는 metric이다.
