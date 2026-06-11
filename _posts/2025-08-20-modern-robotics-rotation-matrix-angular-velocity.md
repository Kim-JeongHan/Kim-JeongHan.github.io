---
layout: post
title: '[Modern Robotics] Rotation Matrix와 Angular Velocity의 관계'
date: 2025-08-20 23:59:26 +0900
slug: modern-robotics-rotation-matrix-angular-velocity
render_with_liquid: false
use_math: true
categories:
- 공부
- 로봇공학
tags:
- modern-robotics
- rotation-matrix
- angular-velocity
last_modified_at: 2025-08-24 23:10:10 +0900
imported_images:
- assets/img/tistory/59/image-001.png
series: modern-robotics
series_order: 3
source:
  provider: tistory
  id: 59
---

### Rotation Matrix와 Angular Velocity의 관계

![](/assets/img/tistory/59/image-001.png)

위 그림을 참고하여, 어떤 회전하는 물체에 단위축 $\{ \hat{x}, \hat{y}, \hat{z} \}$으로 구성된 좌표계가 있다고 하자.

각 단위축들을 시간에 따른 변화율을 구해보면 어떤 기준축 $\hat\omega$에 대하여 $\theta$의 변화율로 표현이 가능하다.

이를 다시 표현해보면 다음과 같다.

$$\mathbf{w} = \hat{w} \cdot \dot{\theta}$$

이제 위 $\mathbf{w}$를 Roataion Matrix 형태로 표현하기 위해 우리는 좌표계 기준을 선택해야한다.

1. 고정프레임 기준
2. 바디 프레임 기준

### 고정 프레임 기준

먼저 고정프레임 $\{s\}$ 기준으로 생각해보면 회전행렬을 $R(t)$, 도함수를 $\dot{R}(t)$라고 해보면,

회전행렬의 열벡터($\dot{r}_i$)와 각속도를 고정프레임기준으로 표현한 벡터($\boldsymbol{\omega}_s \in \mathbb{R}^3$)로 쓸수 있다.

$$\dot{r}_i = \boldsymbol{\omega}_s \times r_i, \quad i = 1, 2, 3$$

이 세식을 하나의 행렬식으로 합치면

$$\dot{R} = \begin{bmatrix} \boldsymbol{\omega}_s \times r_1 & \boldsymbol{\omega}_s \times r_2 & \boldsymbol{\omega}_s \times r_3 \end{bmatrix} = \boldsymbol{\omega}_s \times R$$

skw-symmetric matrix로 표현하면 다음과 같다.

$$\dot{R}=\boldsymbol{\omega}_s \times R = [\boldsymbol{\omega}_s] R$$

---

### 참고)skw-symmetric matrix

$$[\boldsymbol{\omega}s] = \begin{bmatrix} 0 & -\omega{s,3} & \omega_{s,2} \\ \omega_{s,3} & 0 & -\omega_{s,1} \\ -\omega_{s,2} & \omega_{s,1} & 0 \end{bmatrix}$$

- 성질 1 : $[x]=[x]^T$
- 성질 2 : $R[\omega]R^T = [R\omega]$

---

앞서 얻었던 $[\omega_s] R = \dot{R}$ → $[\omega_s] = \dot{R} R^{-1}$로 표현이 가능하다.

이제 body 프레임 기준으로 재표현하면, $\omega_s = R_{sb} \omega_b \quad \Rightarrow \quad \omega_b = R_{sb}^{-1} \omega_s = R^T \omega_s$로 표현이 가능하며,이를 skew-symmetric matrix형태로 재표현하면

$$[\omega_b] = [R^T \omega_s] = R^T [\omega_s] R \quad \\ = R^T \dot{R} \quad \\ = R^{-1} \dot{R}$$

로 표현이 가능하다.

### 정리

<div class="table-responsive tistory-table">
<table>
<tbody>
<tr>
<td>항목</td>
<td>수식</td>
</tr>
<tr>
<td>회전 행렬 미분 → 고정 프레임 기준 각속도</td>
<td>$\dot{R} R^{-1} = [\omega_s]$</td>
</tr>
<tr>
<td>회전 행렬 미분 → 바디 프레임 기준 각속도</td>
<td>$R^{-1} \dot{R} = [\omega_b]$</td>
</tr>
</tbody>
</table>
</div>
