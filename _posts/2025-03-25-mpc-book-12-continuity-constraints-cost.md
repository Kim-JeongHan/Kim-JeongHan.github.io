---
layout: post
title: '[MPC책 공부 - 12] 2장 - 시스템 연속성, 제약, 비용 함수'
date: 2025-03-25 02:07:42 +0900
slug: mpc-book-12-continuity-constraints-cost
render_with_liquid: false
use_math: true
categories:
- 공부
- mpc
tags:
- mpc
- constraints
- cost-function
last_modified_at: 2025-04-02 00:44:00 +0900
series: mpc-study
series_order: 12
source:
  provider: tistory
  id: 35
---

책에서는 이 장 전체에서 다음과 같은 가정을 한다.

*We assume in this chapter that the state \( x \) is known.*

해당 말이 의미하는 바는 다음과 같다.

- 제어 입력을 계산할 때, 현재 시스템의 정확한 상태 \( x(k) \)를 완전히 알고 있다고 가정한다.
- 이 가정 하에서는 관측 오차나 센서 노이즈가 없으며, 제어기는 실제 상태를 완전히 관측 가능한 상황이다.
- 이 가정은 MPC의 기본 구조와 안정성 분석을 단순화하기 위한 것으로, 실제 시스템에서는 상태를 estimate해야 하며, 이때는 observer나 filter가 필요하다.

-> 해당 내용은 3장에서 본격적으로 다루지만, simple한 mpc부터 차근차근 공부해보겠다.

### Proposition) 시스템 해의 연속성

함수 \( f(x, u) \)가 연속이면, 각 정수 \( k \)에 대해 시스템 해 \( \phi(k, x, u) \)는 \( x \)와 \( u \)에 대해 **연속 함수**이다.

즉:

$$
\begin{aligned}
f \text{ continuous} \quad \Rightarrow \quad \phi(k, x, u) \text{ continuous}
\end{aligned}
$$

이는 다음과 같은 의미를 가진다:

- 초기 상태 \( x \)나 제어 입력 시퀀스 \( u \)가 아주 조금만 변해도, 상태 \( x(k) \)는 급격하게 튀지 않고 부드럽게 변화한다.
- 실제 제어기 구현에서 필수적인 **수치적 안정성**과 **연속적인 반응**을 보장하는 기초이다.

### 시스템 제약 조건

시스템에는 아래와 같은 형태의 hard constraint이 존재할 수 있다.

$$
\begin{aligned}
(x(k), u(k)) \in Z \quad \text{for all } k \in \mathbb{I}_{\ge 0}
\end{aligned}
$$

여기서 ZZ는 일반적으로 다음과 같은 다면체(polyhedral) 집합으로 표현된다.

$$
Z = { (x, u) \mid Fx + Eu \le e }
$$

이는 시스템 상태와 입력이 항상 이 영역 Z 안에 있어야 한다는 의미다.

#### 예시: 제어 입력 속도 제한

입력에 대해 다음과 같은 속도 제한(velocity constraint)이 주어질 수 있다:

$$
|u(k) - u(k-1)| \le c
$$

이 제약을 상태 \( z \)를 도입해서 다음과 같이 바꿔 쓸 수 있다:

$$
\begin{aligned}
z^+ &= u \\
z(k) &= u(k-1) \\
|u(k) - z(k)| &\le c
\end{aligned}
$$

즉, 새로운 상태 \( z \)를 통해 속도 제약도 일반적인 상태-입력 제약 \( (x, u) \in Z \) 형태로 표현 가능하다.

### 상태-입력 제약 \( z \)의 구성

\( (x, u) \in Z \)는 다음 두 가지 의미를 포함한다.

#### 입력 제약 (state-dependent control constraint)

어떤 상태 \( x \)에서 가능한 입력 \( u \)는 그 상태에 따라 달라진다:

$$
u \in U(x) := { u \in \mathbb{R}^m \mid (x, u) \in Z }
$$

상태에 의존적인 제약이라 해서, state-dependent control constraints라고 한다.

#### 상태 제약

어떤 상태 \( x \)가 유효한 상태인지 여부는, 그 상태에서 사용할 수 있는 입력이 존재하는지로 결정된다.

$$
x \in X := { x \in \mathbb{R}^n \mid U(x) \ne \emptyset }
$$

### 비용 함수 정의

비용 함수는 다음과 같이 구성된다:

$$
\begin{aligned}
V_N(x, u) := \sum_{k=0}^{N-1} \ell(x(k), u(k)) + V_f(x(N))
\end{aligned}
$$

현재 상태가 \( x \)이고, 현재 시간이 \( i \)라면, 최적제어 문제는 시간 \( i \)에서 시간 \( N+1 \)까지의 구간에 대해 비용을 최소화하는 문제이다.

- \( \ell(x, u) \): stage cost (단계별 비용)
- \( V_f(x(N)) \): terminal cost (종료 상태 비용)

#### 추가 notation

- optimal control sequence:

$$
\begin{aligned}
\mathbf{u}^0(x, i) = \left( u^0(i; (x, i)),\ u^0(i+1; (x, i)),\ \dots,\ u^0(i+N-1; (x, i)) \right)
\end{aligned}
$$

- state sequence:

$$
\begin{aligned}
\mathbf{x}^0(x, i) = \left( x^0(i; (x, i)),\ x^0(i+1; (x, i)),\ \dots,\ x^0(i+N; (x, i)) \right)
\end{aligned}
$$

- 초기 상태 조건 : \( x^0(i; (x, i)) = x \)

MPC에서는 위의 최적 입력 시퀀스 중 **첫 번째 입력만을 실제 시스템에 적용**한다

$$
u^0(i) = u^0(i; (x, i))
$$

#### Time Invariant

- 시스템, 비용 함수 \( \ell(x, u) \), 종료 비용 \( V_f(x) \) 모두 **시간에 무관**하므로, 어떤 시간 \( i \)에서 시작하든, 문제는 항상 **\( P_N(x, 0) \)**과 동일하다.

즉, 다음이 성립한다.

$$
\begin{aligned}
\mathbf{u}^0(x, i) &= \mathbf{u}^0(x, 0) \\
\mathbf{x}^0(x, i) &= \mathbf{x}^0(x, 0)
\end{aligned}
$$
