---
layout: post
title: '[MPC책 공부 - 9] Moving Horizon Estimation'
date: 2025-03-20 23:31:22 +0900
slug: mpc-book-09-moving-horizon-estimation
render_with_liquid: false
use_math: true
categories:
- 공부
- mpc
tags:
- mpc
- moving-horizon-estimation
- state-estimation
last_modified_at: 2025-03-23 22:46:54 +0900
imported_images:
- assets/img/tistory/31/image-001.png
series: mpc-study
series_order: 9
source:
  provider: tistory
  id: 31
---

회사에서 최적제어에 대한 필요성이 점점 생기고 있어, 좀더 빠른속도로 공부해야겠다...

## Moving Horizon Estimation

Moving Horizon Estimation(MHE)은 비선형 시스템 모델을 사용하거나 상태 추정 시 제약 조건을 고려해야 할 때 사용하는 기법이다.
기존의 Kalman 필터(KF)나 Least Squares Estimation(LSE)와 비교하여, MHE는 최근 N개의 측정값만을 사용하여 상태를 추정하는 특징을 갖는다.

![](/assets/img/tistory/31/image-001.png)

## MHE의 필요성

일반적인 Kalman 필터는 선형 시스템에서 최적 상태 추정을 제공하지만, 비선형 시스템이나 제약이 있는 시스템에서는 적용하기 어렵다.

- **비선형 시스템**:
  - Kalman 필터는 선형시스템에서만 사용가능하다. EKF나 UKF가 있지만, 비선형에 따라서 사용불가능한 경우가 존재한다.
- **제약 조건이 있는 경우**:
  - Kalman 필터는 제약을 고려하지 않고 예측하기 때문에, 적절한 예측이 아닐수 있다.

MHE는 이러한 문제를 해결하기 위해 직전 과거 N개의 값만 고려하여 최적화를 수행하는 방법이다.

### MHE에서 사용하는 데이터

MHE는 창이 가득차있는데, 창을 가지고 움직인다고 생각하면 된다.

초기에는 과거의 데이터가 없으므로, 가지고 잇는 초기 데이터를 확장시켜 N개 가지고 있는다고 생각하고 계산한다.

시간이 지나면 과거 N개의 창을 유지한채 새로운 데이터가 들어오면 과거의 데이터를 새로운 데이터로 업데이트하여, 실시간으로 추정한다.

$$ x_N(T) = [x(T-N), x(T-N+1), \dots, x(T)] $$

즉, 시간 \( T \)에서의 상태 추정은 과거 \( N \)개의 측정값을 기반으로 한다.

### MHE 수식의 의미

책에서는 MHE를 optimization Problem로 설명한다.

$$
\begin{aligned} \min_{x_N(T)} \hat{V}_T(x_N(T)) \end{aligned}
$$

여기서 목적 함수는 다음과 같다.

$$
\begin{aligned} \hat{V}_T(x_N(T)) &= \frac{1}{2} \sum_{k=T-N}^{T-1} \| x(k+1) - A x(k) \|^2_{Q^{-1}} + \sum_{k=T-N}^{T} \| y(k) - C x(k) \|^2_{R^{-1}} \end{aligned}
$$

1. **\( \| x(k+1) - A x(k) \|^2_{Q^{-1}} \)**
  - state\( x(k) \)가 **시스템 모델** \( x(k+1) = A x(k) + w(k) \)을 만족하도록 한다.
2. **\( \| y(k) - Cx(k) \|^2_{R^{-1}} \)**
  - 실제 측정된 데이터와 상태 추정값이 유사하도록 한다.

이 최적화 문제를 풀면 최근 \( N \)개의 데이터를 기반으로 한 **optimal state  \( x(T) \)**를 얻을 수 있다.

---

## MHE의 해석

책에서는 MHE를 두가지 방식으로 바라볼 수 있다.

1. MHE를 Least Squares 문제와 유사하게 바라보는 관점(우리가 다룬 관점)
  - 즉, MHE는 Least Squares 문제를 최근 \( N \)개로 제한한 문제와 같다.
2. MHE는 conditional densitiy maximization로 바라보는 관점
