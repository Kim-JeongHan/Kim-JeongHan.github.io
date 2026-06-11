---
layout: post
title: '[MPC책 공부 - 5] Backward Dynamic Programming을 이용한 LQ 최적 제어(Riccati iteration)'
date: 2025-03-13 02:05:10 +0900
slug: mpc-book-05-riccati-iteration
render_with_liquid: false
use_math: true
categories:
- 공부
- mpc
tags:
- mpc
- dynamic-programming
- riccati-iteration
last_modified_at: 2025-03-27 21:19:38 +0900
series: mpc-study
series_order: 5
source:
  provider: tistory
  id: 25
---

### **1. DP를 이용한 최적 제어 문제 설정**

일반적인 **LQ 최적 제어 문제**는 다음과 같이 주어진다.

$$
\begin{align}
V(x(0), u) = \sum_{k=0}^{N-1} \ell(x(k), u(k)) + \ell_N(x(N))
\end{align}
$$

여기서:

- \( \ell(x, u) \)는 **단계별 비용 (Stage Cost)** 로서, 제어 과정에서 상태 및 입력이 발생시키는 비용을 나타냄
- \( \ell_N(x) \)는 **최종 비용 (Terminal Cost)** 로서, 최종 상태에서 발생하는 비용을 나타냄

책에서는 이 비용을 구체적으로 다음과 같이 정의하였다.

$$
\begin{align}
\ell(x, u) &= \frac{1}{2} \left( x^T Q x + u^T R u \right) \\
\ell_N(x) &= \frac{1}{2} x^T P_f x
\end{align}
$$

또한, 시스템의 상태는 다음과 같은 선형 시스템으로 변화한다.

$$
\begin{align}
x(k+1) = A x(k) + B u(k)
\end{align}
$$

여기서 **목표는 최적의 제어 입력 \( u(k) \) 를 찾아 비용 \( V(x(0), u) \) 을 최소화하는 것**이다. 이를 summation을 풀어 식으로 표현하면 다음과 같이 표현된다.

$$
\begin{aligned}
\min_{u(0), x(1), \dots, u(N-2), x(N-1)} & \quad \ell(x(0), u(0)) + \ell(x(1), u(1)) + \dots + \\
& \quad \min_{u(N-1), x(N)} \ell(x(N-1), u(N-1)) + \ell_N(x(N))
\end{aligned}
$$

우리는 앞에서 다루었던 Backward DP를 사용하여, 최적화 할 수 있다.

### **2. Backward DP를 이용한 최적화**

앞의 수식 \( V(x(0), u) = \sum_{k=0}^{N-1} \ell(x(k), u(k)) + \ell_N(x(N)) \) Backward DP를 적용하면

$$
\begin{aligned}
\min_{u(0), x(1), \dots, u(N-2), x(N-1)} & \quad \ell(x(0), u(0)) + \ell(x(1), u(1)) + \dots + \\
& \quad \min_{u(N-1), x(N)} \ell(x(N-1), u(N-1)) + \ell_N(x(N))
\end{aligned}
$$

표현이 가능하고, 마지막 stage인**(\( k = N-1 \))** 의 최적화를 진행한다.

#### 1) 마지막  stage에서의 최적화 (\( k = N-1 \))

last staged의 Cost Function는 다음과 같이 표현된다.

$$
\begin{aligned}
&\min_{u(N-1), x(N)} \quad \ell(x(N-1), u(N-1)) + \ell_N(x(N)) \\
&\text{subject to} \quad x(N) = A x(N-1) + B u(N-1)
\end{aligned}
$$

두 개의 이차함수의 합으로 이루어진 해당 Cost Function을 [관련 글](/blog/2025/mpc-book-04-lq-quadratic-sum-example/)에서 증명한 하나의 이차함수 형태로 재표현한다.
$$\begin{aligned}
\ell(x(N-1), u(N-1)) + \ell_N(x(N))
&= \frac{1}{2} \left( |x(N-1)|_Q^2 + |u(N-1)|_R^2 + |A x(N-1) + B u(N-1)|_{P_f}^2 \right) \\
&= \frac{1}{2} \left( |x(N-1)|_Q^2 + |(u(N-1) - v)|_H^2 + d \right)
\end{aligned}
$$

$$
\begin{aligned}
H &= R + B' P_f B \\
v &= - (B' P_f B + R)^{-1} B' P_f A x(N-1) \\
d &= x(N-1)' \left( A' P_f A - A' P_f B (B' P_f B + R)^{-1} B' P_f A \right) x(N-1)
\end{aligned}
$$

구해진 last stage의 cost function의 형태를 고려했을때, \( u(N-1) \)의 대한 최적 입력이 \( v \) 임을 확인 할 수 있다.

> \(|(u(N-1) - v)|_H^2 = 0 \)으로 만든다.

이를 통해, cost function을 N-1 stage의 optimal state \( x(N-1) \) 의 선형함수이다.

모든 x에 대하여, 입력 \( (u, x, V) \) 를 아래와 같이 정의하면, 모든 x에 대하여 아래와 같이 표현할 수 있다.

$$ \begin{aligned} u_{N-1}^{0}(x) &= K(N-1) x \\ x_N^{0}(x) &= (A + B K(N-1)) x \\ V_{N-1}^{0}(x) &= \frac{1}{2} x' \Pi(N-1) x \end{aligned} $$

$$ \begin{aligned} K(N-1) &:= - (B' P_f B + R)^{-1} B' P_f A \\ \Pi(N-1) &:= Q + A' P_f A - A' P_f B (B' P_f B + R)^{-1} B' P_f A \end{aligned} $$

마지막 stage의 대한 optimal cost를 정의했고, DP의 다음단계를 진행 할 수 있다.

#### 2) 이전 단계(\(N-2\), \(N-3\), ..., \(0\))에서의 최적해

이전 stage의 optimal soultion의 문제는 다음과 같다.

$$
\begin{aligned}
&\min_{u(N-2), x(N-1)} \quad \ell(x(N-2), u(N-2)) + V_{N-1}^{0} (x(N-1)) \\
&\text{subject to} \quad x(N-1) = A x(N-2) + B u(N-2)
\end{aligned}
$$

위 문제는 우리가 해결한 last staged의 구조가 동일하며, 동일하게 표현이 가능하다.

$$
\begin{aligned}
u_{N-2}^{0}(x) &= K(N-2) x \\
x_{N-1}^{0}(x) &= (A + B K(N-2)) x \\
V_{N-2}^{0}(x) &= \frac{1}{2} x' \Pi(N-2) x \\
K(N-2) &:= - (B' \Pi(N-1) B + R)^{-1} B' \Pi(N-1) A \\
\Pi(N-2) &:= Q + A' \Pi(N-1) A \\
&\quad - A' \Pi(N-1) B (B' \Pi(N-1) B + R)^{-1} B' \Pi(N-1) A
\end{aligned}
$$

\( \Pi(N-1) \rightarrow \Pi(N-2) \)의 재귀는 backward Riccati iteration으로 알려져 있다.

---

#### Backward Riccati iteration 정의

$$
\begin{aligned}
\Pi(k-1) &= Q + A' \Pi(k) A \\
&\quad - A' \Pi(k) B (B' \Pi(k) B + R)^{-1} B' \Pi(k) A
\quad &&\text{for } k = N, N-1, \dots, 1
\end{aligned}
$$
$$
\text{with terminal condition} \quad \Pi(N) = P_f
$$

---

Optimal Control Policy는 Backward Riccati iteration을 통해, optimal input과 optimal state, optimal cost는 다음과 같다.

$$
\begin{aligned}
u_k^{0}(x) &= K(k) x \quad &&\text{for } k = N-1, N-2, \dots, 0 \\
K(k) &= - (B' \Pi(k+1) B + R)^{-1} B' \Pi(k+1) A \quad &&\text{for } k = N-1, N-2, \dots, 0 \\
x_{k+1}^{0}(x) &= (A + B K(k)) x \quad &&\text{for } k = N-1, N-2, \dots, 0 \\
V_k^{0}(x) &= \frac{1}{2} x^{T} \Pi(k) x \quad &&\text{for } k = N-1, N-2, \dots, 0
\end{aligned}
$$
