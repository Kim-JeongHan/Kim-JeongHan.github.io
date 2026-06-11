---
layout: post
title: '[MPC책 공부 - 13] 2장 - 최적 제어의 해는 언제 존재하는가?'
date: 2025-04-01 23:35:57 +0900
slug: mpc-book-13-optimal-control-existence
render_with_liquid: false
use_math: true
categories:
- 공부
- mpc
tags:
- mpc
- optimal-control
- existence
last_modified_at: 2025-04-02 01:21:12 +0900
series: mpc-study
series_order: 13
source:
  provider: tistory
  id: 41
---

본 게시글은 최적제어의 해가 존재하는 조건은 무엇인지, 그렇다면, 해가 집합일 경우 어떻게 처리되는지에 대한 내용을 다루고 있다. 해당 최적제어는 연속이라는 가정에서 출발한다.

### Assumption 2.2: 시스템과 비용의 연속성

다음 함수들은 **모두 연속**이라고 가정한다.

- 시스템 동역학 \( f(x, u) \)
- 단계 비용 함수 \( \ell(x, u) \)
- 종료 비용 함수 \( V_f(x) \)

또한 모두 원점에서 0의 값을 갖는다.

$$
\begin{aligned}
f(0, 0) &= 0 \\
\ell(0, 0) &= 0 \\
V_f(0) &= 0
\end{aligned}
$$

### Assumption 2.3: 제약 집합의 성질

#### 제약 없는 경우를 위한 정의

실제 대다수의 경우는 , 제어 입력에 제약이 존재하지만, 제약이 있는 경우와 제약이 없는 경우를 구분에서 다루기 위해, 추가적으로 제약집합을 사용한다. 이는 제약이 없을 경우에도 상태 집합을 수학적으로 정의하기 위해 사용된다.

- 비용이 어떤 값 \( c \) 이하인 제어 시퀀스 집합

$$
\mathcal{U}_N^{c}(x) := { u \mid V_N(x, u) \le c }
$$

- 이때 문제의 해가 존재하는 상태 집합

$$
\mathcal{X}_N^{c} := { x \mid \mathcal{U}_N^{c}(x) \ne \emptyset }
$$

---

#### 제약 집합의 성질(가정)

- 상태-입력 제약 집합 \( Z \)는 닫힌 집합(closed set)이다.
- 제어 제약이 있다면, \( \mathcal{U}(x) \)는 모든 x에서 compact이고, bounded된 상태 \( X \)에서 uniform하다.
- 종료 집합 \( X_f \subseteq X \)는 compact하다.
- 모든 집합은 원점 \( (0, 0) \)을 포함한다.
- 제약이 없을 경우, 비용 함수 \( V_N(x, u) \)는 coercive이다. 즉, \( |u| \to \infty \)일 때 \( V_N(x, u) \to \infty \)

---

### Proposition 2.4: 최적 제어 해의 존재성

Assumptions 2.2, 2.3을 만족하면 다음이 성립한다.

#### (a) \( V_N(x, u) \)는 \( (x, u) \)에 대해 연속이다.

이는 \( \ell \), \( V_f \)가 연속이고, 시스템 해 \( \phi(k, x, u) \)도 연속이기 때문에 성립한다.

#### (b) 제약 집합 \( \mathcal{U}_N(x) \) 또는 제약이없는 집합\( \mathcal{U}_N^{c}(x) \)은 compact하다.

가정2.3에서 이야기한바와 같다.

#### (c) Weierstrass 정리에 따라 최적 해가 항상 존재한다.

결론이 가장 중요하다.

가정 2.3, 2.3을 만족하면 우리는 최적해가 항상 존재함을 알 수 있다.

---

### 최적 제어 해와 MPC 제어 법칙

주어진 현재 상태 \( x \)에 대해, MPC는 다음 최적화 문제를 푼다

$$
u^0(x) := \arg\min_{u \in \mathcal{U}_N(x)} V_N(x, u)
$$

여기서

- \( V_N(x, u) = \sum_{k=0}^{N-1} \ell(x(k), u(k)) + V_f(x(N)) \)
- \( \mathcal{U}_N(x) \)는 상태와 입력이 제약을 만족하도록 하는 유효한 제어 시퀀스의 집합
- \( u \)는 제어 시퀀스 전체를 의미하고, 해 \( u^0(x) \)도 역시 전체 시퀀스를 의미
- \( u^0(x) = \left( u^0(0; x),\ u^0(1; x),\ \dots,\ u^0(N-1; x) \right) \)

---

- 최적 제어 시퀀스 \( u^0(x) \)를 계산하지만, **실제 시스템에 적용하는 것은 그 중 첫 번째 입력**이다.

즉,

$$
\kappa_N(x) := u^0(0; x)
$$

이것이 실제 로봇이나 시스템에 적용되는 제어 입력이다. 나머지 제어 입력은 사용하지 않고,
다음 시간 스텝에서 상태를 새로 측정한 후, 문제를 다시 풀어 새로운 입력을 얻는다.

이 과정을 함수처럼 표현하면, 다음과 같이 쓸 수 있다:

$$
\kappa_N : x \mapsto u^0(0; x)
$$

즉, 상태 \( x \)가 주어졌을 때, MPC는 해당 상태에서 문제 \( P_N(x) \)를 풀고, 첫 번째 입력을 반환하는 함수로 작동한다. 이 함수 \( \kappa_N(x) \)가 바로 MPC 제어 법칙(control law)이다.

단, 이 함수는 정의역이 제한되어 있다. 제약을 만족하며 문제의 해가 존재하는 상태 \( x \)들로 구성된 집합

$$
x \in X_N := { x \in \mathbb{R}^n \mid \mathcal{U}_N(x) \ne \emptyset }
$$

### 해가 유일한 경우 vs 유일하지 않은 경우

- **해가 유일한 경우**:
  - \( u^0(x) \)는 단일 벡터로 정의됨
  - 제어 법칙 \( \kappa_N(x) = u^0(0; x) \)도 일반적인 함수 형태
- **해가 유일하지 않은 경우**:
  - 최적 입력 시퀀스 \( u^0(x) \)가 여러 개 존재할 수 있음 (즉, argmin이 여러 개)
  - 이때 제어 법칙은 집합 값을 갖는 함수 (set-valued function)이 됨:
  - $$
    \kappa_N(x) := { u^0(0) \mid u^0 \text{ is an optimal solution to } P_N(x) }
    $$
  - 이 경우 MPC는 그 집합에서 하나의 요소를 선택하여 적용한다. 이 선택은 문제 설계나 구현 방식에 따라 달라질 수 있다.
