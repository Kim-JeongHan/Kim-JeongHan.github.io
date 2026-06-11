---
layout: post
title: '[MPC책 공부 - 11] 외란과 보정 Disturbances and Zero offset'
date: 2025-03-23 23:14:18 +0900
slug: mpc-book-11-disturbances-zero-offset
render_with_liquid: false
use_math: true
categories:
- 공부
- mpc
tags:
- mpc
- disturbance
- offset-free
last_modified_at: 2025-03-24 23:32:10 +0900
imported_images:
- assets/img/blog/mpc-book-11-disturbances-zero-offset/image-001.png
series: mpc-study
series_order: 11
source:
  provider: tistory
  id: 33
---

측정되지 않는 disturbance는 시스템 제어 변수에 영향을 미칠 수 있다. 이러한 문제는  disturbance rejection로 잘알려져 있다.. 이러한 측정되지않은 disturbance가 들어오더라도 시스템 제어 변수에 바로 영향을 미치는 것이 아닌, 점진적으로 영향을 미치도록 nonzero disturbance를 보상하는 시스템을 설계하려고 한다. 이때, 우리는 선택된 제어 변수에 offset을 설정하여 튜닝하는 것이 아닌, zero offset으로 구성하려고자 한다.

해당 문제는 5장에서 중요하게 다룰텐데, 여기서는 간략하게 다루겠다.

외란을 없애는 핵심 방법은 다음 세 가지로 요약됨:

1. 모델링: 외란을 적분형 모델로 가정
2. 상태 추정기(estimator, e.g., Kalman filter)를 확장해서 상태 \( x \) 와 disturbance \( d \)를 함께 추정
3. 보정: 추정된 외란 \( \hat{d} \)를 이용해 steady-state target 계산 문제를 수정하여 오프셋 제거

### Disturbance 모델

외란은 다음과 같은 적분형 모델로 가정된다.

$$ d^+ = d - w_d  $$

이는 외란이 천천이 변하거나, 상수일때 적합한 모델이다.

### 시스템 모델 확장 (Augmented System)

시스템은 disturbance 이 추가된 시스템으로 바뀐다.

$$ \begin{bmatrix} x \\ d \end{bmatrix}^{+} = \underbrace{ \begin{bmatrix} A & B_d \\ 0 & I \end{bmatrix} }_{\tilde{A}} \begin{bmatrix} x \\ d \end{bmatrix} + \underbrace{ \begin{bmatrix} B \\ 0 \end{bmatrix} }_{\tilde{B}} u - w $$

출력은 disturbance가 영향을 미치는 형태로 바뀐다.

$$ y = \begin{bmatrix} C & C_d \end{bmatrix} \begin{bmatrix} x \\ d \end{bmatrix} + v $$

- \( B_d \), \( C_d \)는 외란이 어디로 들어오는지를 나타내는 행렬 (설계자가 선택하여, disturbance의 적분이 어떻게 영향을 미치는 지 자유롭게 선택 가능)
- 이 시스템을 기반으로 Kalman Filter를 만들면, \( x \)와 \( d \)를 동시에 추정할 수 있다.

### Detectability 조건

augmented system이 detectable하려면, 아래 조건이 성립해야한다.

$$ \text{rank} \begin{bmatrix} I - A & -B_d \\ C & C_d \end{bmatrix} = n + n_d $$

즉, augmented system이 detectable한 최대 disturbance \( d \)는 measurement의 수(출력 벡터 \( y \in \mathbb{R}^p \))

를 넘으면 안된다.

$$ n_d \leq p $$

### Steady-State Target Optimization (with disturbance)

disturbance의 추정치 \( \hat{d} \approx d_s \)를 기반으로 steady-state를 계산해야 할 때 식을 \( d^+ = d - w_d \)을 사용하여 다시 정리한다.

**목적함수**

$$ \min_{x_s, u_s} \quad \frac{1}{2} \left( \| u_s - u_{\text{sp}} \|^2_{R_s} + \| C x_s + C_d \hat{d}_s - y_{\text{sp}} \|^2_{Q_s} \right) $$

원래 목표 \( y_{\text{sp}} \)를 달성하기 위해 외란이 영향을 준 만큼 빼주는 보정을 한다.

**제약조건**

$$ \min_{x_s, u_s} \quad \frac{1}{2} \left( \| u_s - u_{\text{sp}} \|^2_{R_s} + \| C x_s + C_d \hat{d}_s - y_{\text{sp}} \|^2_{Q_s} \right) $$

$$ \begin{aligned} E u_s &\leq e \\ F C x_s &\leq f - F C_d \hat{d}_s \end{aligned} $$

<div class="table-responsive tistory-table">
<table>
<tbody>
<tr>
<td> </td>
<td>disturbance 보정 전</td>
<td>disturbance 보정 후</td>
</tr>
<tr>
<td>ouput 오차</td>
<td><span>\( Cx_s - y_{\text{sp}} \)</span></td>
<td><span> \( Cx_s + C_d \hat{d}_s - y_{\text{sp}} \)</span></td>
</tr>
<tr>
<td>dynamic equation</td>
<td><span>\( (I - A)x_s - Bu_s = 0 \)</span></td>
<td><span>\( (I - A)x_s - Bu_s = B_d \hat{d}_s \)</span></td>
</tr>
<tr>
<td>output constraint</td>
<td><span>\( FC x_s \leq f \)</span></td>
<td><span>\( FC x_s \leq f - FC_d \hat{d}_s \)</span></td>
</tr>
<tr>
<td>tracking target</td>
<td><span>\( HC x_s = r_{\text{sp}} \)</span></td>
<td><span>\( HC x_s = r_{\text{sp}} - HC_d \hat{d}_s \)</span></td>
</tr>
</tbody>
</table>
</div>

위 MPC 알고리즘에 의해 제어되는 system은 아래와 같은 그림으로 보여질 수 있다.

![](/assets/img/blog/mpc-book-11-disturbances-zero-offset/image-001.png)

추가적으로 정리하자면,

1. estimator는 augmented model을 사용해야한다.
2. estimator의 measurements의 수(출력 벡터 \( y \in \mathbb{R}^p \))는 disturbance의 차원가 같다.
3. 2번의 조건에 의해서 estimator의 detectability를 만족해야한다.
4. 위세가지의 조건을 만족하면서, ouput\( y(k) \)이 수렴하여, steady state\( y_s \)에 도달했다면, closed-loop system은 stable하며, constraints는 작동되지 않는다.즉, 제약조건 안에서 zero-offset 제어가 되고 있다는 말을 의미한다.

해당 문제를 예제와 함께 설명하고 싶지만, 이건 능력부족으로 인해... 차후에 미루겠다...
