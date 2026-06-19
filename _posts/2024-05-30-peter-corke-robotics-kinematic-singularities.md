---
layout: post
title: '[Peter Corke Robotics] Kinematic Singularities'
date: 2024-05-30 21:00:00 +0900
slug: peter-corke-robotics-kinematic-singularities
render_with_liquid: false
use_math: true
categories:
- 공부
- 로봇공학
tags:
- robotics
- kinematics
last_modified_at: 2026-06-15 16:46:02 +0900
series: peter-corke-robotics
series_order: 1
---

Peter Corke의 로보틱스 책을 보면서 정리한 manipulator kinematics 메모다. 회전 표현에서 시작해, Jacobian과 singularity가 manipulator 해석에서 왜 중요한지 정리한다.

## Two-Vector Representation

End-effector의 방향을 표현할 때 자주 쓰는 방식이다. End-effector의 접근 방향을 $Z$축에 맞추고,

$$
\hat{a} = \{a_x, a_y, a_z\}
$$

손이 움직이는 방향을 $Y$축에 맞춘다.

$$
\hat{o} = \{o_x, o_y, o_z\}
$$

그다음 두 방향 벡터의 외적으로 $X$축 방향을 구한다.

$$
\hat{n} = \hat{o} \times \hat{a}
$$

따라서 회전행렬은 다음처럼 구성할 수 있다.

$$
R =
\begin{pmatrix}
n_x & o_x & a_x \\
n_y & o_y & a_y \\
n_z & o_z & a_z
\end{pmatrix}
$$

![two-vector representation](/assets/img/blog/peter-corke-robotics-kinematic-singularities/image-001.png)

## Angle-Axis

회전행렬은 하나의 unit vector와 회전량으로도 표현할 수 있다. 이를 angle-axis 표현이라고 한다.

### Proof

회전행렬의 eigenvalue와 eigenvector를 구하면, 회전행렬의 eigenvalue는 실근 $1$과 복소근 두 개로 나온다.

$$
\lambda = 1, \qquad \lambda = \cos\theta \pm j\sin\theta
$$

여기서 $\theta$는 rotation angle이다. 회전행렬 $R$에 대해

$$
R\mathbf{v} = \lambda \mathbf{v}
$$

이고, eigenvalue가 $1$인 경우에는

$$
R\mathbf{v} = \mathbf{v}
$$

가 된다. 즉, 회전 후에도 변하지 않는 방향 벡터가 존재한다. 이 eigenvector가 rotation axis가 된다.

### Inverse Formula

![angle-axis inverse formula](/assets/img/blog/peter-corke-robotics-kinematic-singularities/image-002.png)

## Kinematic Singularities

Manipulator의 end-effector 속도와 joint 속도는 Jacobian을 통해 연결된다.

$$
v_e = J(q)\dot{q}
$$

Singularity를 찾는 것은 manipulator에서 매우 중요하다.

- Singularity는 목표 end-effector motion이 가능한지 판단하는 척도가 된다.
- Singular configuration에서는 inverse kinematics의 해가 존재하지 않거나 불안정해질 수 있다.
- Singularity 근처에서는 task space의 작은 속도가 joint space의 매우 큰 속도를 요구할 수 있다.

### Boundary Singularity

Boundary singularity는 manipulator가 길게 펼쳐진 상태에서 발생한다. 이 경우는 작업 영역의 경계 근처를 피하면 되기 때문에 비교적 단순하게 대응할 수 있다.

### Internal Singularity

주로 문제가 되는 것은 internal singularity다. 이는 reachable workspace 안에서 두 개 이상의 축이 align될 때 발생한다.

Boundary singularity와 달리, internal singularity는 reachable workspace 안의 path를 수행하는 도중에도 발생할 수 있다. 실제 작업 중 더 자주 마주치게 되는 singularity도 이쪽이다.

![boundary and internal singularity](/assets/img/blog/peter-corke-robotics-kinematic-singularities/image-003.png)

## Spherical Wrist vs Non-Spherical Wrist

![spherical wrist vs non-spherical wrist](/assets/img/blog/peter-corke-robotics-kinematic-singularities/image-004.png)

Inverse kinematics를 더 쉽게 풀기 위해 wrist 축의 교차점이 한 점에서 만나도록 설계한 robot 구조를 spherical wrist라고 한다.

Spherical wrist 구조에서는 singularity 문제를 arm과 wrist로 분리해서 계산할 수 있기 때문에 inverse kinematics 해석에 이점이 있다.

## Singularity Decoupling

Singularity decoupling은 spherical wrist 타입의 로봇에서 singularity 문제를 두 부분으로 나누어 해석하는 방식이다.

- Arm singularity
- Wrist singularity

Jacobian을 다음처럼 block matrix로 나누어 생각하자.

$$
J =
\begin{bmatrix}
J_{11} & J_{12} \\
J_{21} & J_{22}
\end{bmatrix}
$$

Spherical wrist 로봇의 마지막 세 joint는 revolute type이므로 $J_{12}$, $J_{22}$를 다음처럼 쓸 수 있다.

$$
J_{12} =
\begin{bmatrix}
z_3 \times (p_e - p_3) &
z_4 \times (p_e - p_4) &
z_5 \times (p_e - p_5)
\end{bmatrix}
$$

$$
J_{22} =
\begin{bmatrix}
z_3 & z_4 & z_5
\end{bmatrix}
$$

Singularity는 mechanical structure에 의해 결정되는 현상이지, 기준 frame 선택에 의해 달라지는 현상이 아니다. 따라서 end-effector를 기준 frame으로 선택해도 된다.

기준 frame을 end-effector로 잡으면 wrist axes가 한 점에서 만나고, 마지막 세 joint에 대한 $p$는 모두 같아진다.

$$
J_{12} =
\begin{bmatrix}
0 & 0 & 0
\end{bmatrix}
$$

따라서 Jacobian은 lower triangular matrix 형태가 된다.

$$
\det(J)=\det(J_{11})\det(J_{22})
$$

Lower triangular matrix의 determinant 계산은 간단해지고, singularity를 arm singularity와 wrist singularity로 분리해서 볼 수 있다.

$$
\det(J_{11}) = 0
\qquad \text{or} \qquad
\det(J_{22}) = 0
$$

## Wrist Singularity

![wrist singularity](/assets/img/blog/peter-corke-robotics-kinematic-singularities/image-005.png)

Unit vector $z_3$, $z_4$, $z_5$가 linearly dependent해지는 순간 wrist singularity가 된다.

$z_3$, $z_4$, $z_5$가 linearly independent하지 않게 되는 대표적인 조건은 $z_3$와 $z_5$가 align되는 경우다. 이때의 joint angle 조건은 다음과 같다.

$$
\theta_5 = 0
\qquad \text{or} \qquad
\theta_5 = \pi
$$

즉, kinematic structure를 고려했을 때 다섯 번째 joint가 $0$ 또는 $\pi$에 있을 때 wrist singularity가 발생한다.

Wrist singularity는 joint space에서는 자연스러운 움직임처럼 보일 수 있지만, reachable workspace 안에서 쉽게 마주칠 수 있는 상황이다.

## Arm Singularity

![arm singularity](/assets/img/blog/peter-corke-robotics-kinematic-singularities/image-006.png)

Arm singularity는 anthropomorphic arm 구조에서 볼 수 있다.

$$
\det(J_p) = -a_2 a_3 s_3(a_2c_2 + a_3c_{23})
$$

이 determinant는 first joint variable에 의존하지 않는다. 또한 $a_2, a_3 \ne 0$이므로 다음 두 경우에 determinant가 $0$이 된다.

첫 번째는

$$
s_3 = 0
$$

인 경우다. 이는

$$
\theta_3 = 0
\qquad \text{or} \qquad
\theta_3 = \pi
$$

에 해당하며, elbow singularity라고 볼 수 있다.

두 번째는

$$
a_2c_2 + a_3c_{23} = 0
$$

인 경우다. 이는 wrist point가 axis $z_0$와 일치하는 상황, 즉

$$
p_x = p_y = 0
$$

인 상황에 해당한다. 이를 shoulder singularity라고 볼 수 있다.

Wrist singularity와 달리 arm singularity는 작업 상황에서 비교적 식별하기 쉽다. 따라서 end-effector trajectory planning 단계에서 적절히 회피하는 방식으로 대응할 수 있다.
