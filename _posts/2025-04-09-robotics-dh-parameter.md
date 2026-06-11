---
layout: post
title: '[로봇공학] DH 파라미터 (Denavit–Hartenberg parameter)'
date: 2025-04-09 20:42:18 +0900
slug: robotics-dh-parameter
render_with_liquid: false
use_math: true
categories:
- 공부
- 로봇공학
tags:
- robotics
- kinematics
- dh-parameters
last_modified_at: 2025-05-13 15:32:28 +0900
imported_images:
- assets/img/tistory/43/image-001.png
- assets/img/tistory/43/image-002.png
- assets/img/tistory/43/image-003.png
source:
  provider: tistory
  id: 43
---

가끔 수식이 기억이 안날때가 있어, 찾아보고 싶어 정리한다.

# Denavit–Hartenberg(DH) 파라미터

로봇 Manipulator를 구성하고 동작시키기 위해 가장 먼저 해야 할 일은 각 관절의 위치와 자세를 정확히 정의하는 것이다. 이때 사용하는 대표적인 방법이 Denavit–Hartenberg(DH) 파라미터다.

## 회전 행렬 Rotation Matrix

로봇의 링크가 회전할 때, 우리는 한 좌표계에서 다른 좌표계로 벡터를 변환해야 한다. 이때 사용하는 것이 회전 행렬(Rotation Matrix)이다.

3차원에서 축 기준 회전 행렬은 다음과 같다.

- \( x \)축 회전 \( \theta \)

$$
R_x(\theta) =
\begin{bmatrix}
1 & 0 & 0 \\
0 & \cos\theta & -\sin\theta \\
0 & \sin\theta & \cos\theta
\end{bmatrix}
$$

- \( y \)축 회전 \( \theta \)

$$
R_y(\theta) =
\begin{bmatrix}
\cos\theta & 0 & \sin\theta \\
0 & 1 & 0 \\
-\sin\theta & 0 & \cos\theta
\end{bmatrix}
$$

- \( z \)축 회전 \( \theta \)

$$
R_z(\theta) =
\begin{bmatrix}
\cos\theta & -\sin\theta & 0 \\
\sin\theta & \cos\theta & 0 \\
0 & 0 & 1
\end{bmatrix}
$$

## Homogeneous Transformation Matrix

좌표계는 회전과 이동(translation)의 조합이다. 이를 함께 표현하기 위해 사용하는 것이 Homogeneous Transformation Matrix다.

예를 들어, \( R \)이 회전 행렬이고 \( d \)가 위치 벡터일 때 전체 변환 행렬은

$$
T =
\begin{bmatrix}
R & d \\
0 & 1
\end{bmatrix}
$$

3D 공간의 예

$$
T =
\begin{bmatrix}
r_{11} & r_{12} & r_{13} & d_x \\
r_{21} & r_{22} & r_{23} & d_y \\
r_{31} & r_{32} & r_{33} & d_z \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

## 표준 DH 파라미터(Standard DH Parameter)

DH 파라미터는 각 링크 간의 관계를 네 가지 값으로 정의한다.

- \( \theta_i \): \( x_{i-1} \)축을 기준으로 \( z_{i-1} \)축에서 \( z_i \)축까지의 회전
- \( d_i \): \( z_{i-1} \)축을 따라 \( x_{i-1} \)에서 \( x_i \)까지의 거리
- \( a_i \): \( x_{i} \)축을 따라 \( z_{i-1} \)에서 \( z_i \)까지의 거리
- \( \alpha_i \): \( x_i \)축을 기준으로 \( z_{i-1} \)에서 \( z_i \)까지의 회전

![](/assets/img/tistory/43/image-001.png)

이들을 사용해 각 링크 간 변환 행렬을 다음과 같이 구성할 수 있다.

$$
T^{i+1}_{t-1} =
\begin{bmatrix}
\cos\theta_i & -\sin\theta_i \cos\alpha_i & \sin\theta_i \sin\alpha_i & a_i \cos\theta_i \\
\sin\theta_i & \cos\theta_i \cos\alpha_i & -\cos\theta_i \sin\alpha_i & a_i \sin\theta_i \\
0 & \sin\alpha_i & \cos\alpha_i & d_i \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

이 변환 행렬을 연속적으로 곱하면 로봇의 Base에서 End-effector까지의 전체 포즈를 계산할 수 있다.

---

## Modified DH 파라미터

Modified DH 파라미터는 변환 순서를 조금 다르게 구성해 계산을 단순화하려는 목적에서 등장했다. 차이점은 다음과 같다

<div class="table-responsive tistory-table">
<table>
<tbody>
<tr>
<td>항목</td>
<td>Standard DH</td>
<td>Modified DH</td>
</tr>
<tr>
<td>회전 순서</td>
<td>\( R_z(\theta) \to T_z(d) \to T_x(a) \to R_x(\alpha) \)</td>
<td>\( T_x(a) \to R_x(\alpha) \to T_z(d) \to R_z(\theta) \)</td>
</tr>
<tr>
<td>축 기준</td>
<td>\( z \) 축을 기준으로 관절 회전</td>
<td>\( x \) 축 기준에서 기준 좌표계 이동</td>
</tr>
</tbody>
</table>
</div>

Modified DH parameter

![](/assets/img/tistory/43/image-002.png)
![](/assets/img/tistory/43/image-003.png)
