---
layout: post
title: '[MPC책 공부 - 7] LQR(Linear Quadratic Regulator)의 수렴'
date: 2025-03-18 23:21:20 +0900
slug: mpc-book-07-lqr-convergence
render_with_liquid: false
use_math: true
categories:
- 공부
- mpc
tags:
- mpc
- lqr
- stability
last_modified_at: 2025-03-18 23:52:20 +0900
series: mpc-study
series_order: 7
source:
  provider: tistory
  id: 29
---

오늘은 매일 게시글 올리기로 한 친구가 당일약속 당일취소를 한 기념으로 게시글을 올리려고 한다.ㅋㅋ

책 1.3.5에 나오는 Controllability는 증명 부분이고, 요약하자면, Cayley-Hamilton정리에 의해, \(N\ge n\)일때( \( N \) 은 horizon이고, \( n \)은 state vector 즉, 차원) Controllability하다는 사실을 알고가면 된다.

### 증명하고자 하는 결론

Infinite Horzion LQR 문제는 다음과 같은 Cost function을 최소화하는 문제이다.

$$
\begin{aligned}
V(\mathbf{x}, \mathbf{u}) &= \frac{1}{2} \sum_{k=0}^{\infty} \left( x(k)' Q x(k) + u(k)' R u(k) \right) \\
\text{subject to} \quad & x^+ = A x + B u \\
& x(0) = x
\end{aligned}
$$

- 추가조건

$$ Q > 0, R > 0 $$

이 존재할때, LQR의 optimal control solution은 항상 존재하며, 유일하다. -> 즉 수렴한다.

여기서 두가지를 생각해보면 된다.

1. 해당 조건을 모두 만족하면 cost function은 controllable하다.

2. controllable하며, Infitie horizon임으로, horizon을 계속 늘릴수 있다.

---

## 증명

1. 제어 가능성(Controllability)

\( (A, B) \)가 제어 가능하면, 모든 초기 상태 \( x(0) \) 에 대해서 적절한 입력 \( u(k) \)을 선택하면 유한한 시간 \( n \) 안에 상태를 0으로 만들 수 있다.

2. 이후의 제어 입력을 0으로 설정하면 비용이 0이 된다.

\( x(n) = 0 \) 이후로는 더 이상 제어 입력이 필요하지 않으므로, 이후의 제어 입력을 0으로 설정할 수 있다. 그러면, \( k \geq n \) 에 대한 비용 함수의 항목은 모두 0 이된다.

3. 수렴한다.

책에서는 이러한 선형 시스템에서 Controllability에 대한 개념이 익숙해지는 것이 차후 비선형 시스템을 쉽게 다루게 한다고 한다.

또한 현재 우리가 증명한 방식은 asymptotic Convergence인데, 이는 수렴속도가 매우 느릴수 있다.
차후 이를 보완한 exponential Convergence에 다룰 예정이다.
