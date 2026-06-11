---
layout: post
title: '[MPC책 공부 -3] LQ문제에서 Cost Function 유도'
date: 2025-03-12 23:52:44 +0900
slug: mpc-book-03-lq-cost-function
render_with_liquid: false
use_math: true
categories:
- 공부
- mpc
tags:
- mpc
- lq
- cost-function
last_modified_at: 2025-03-17 10:03:14 +0900
series: mpc-study
series_order: 3
source:
  provider: tistory
  id: 23
---

### **Cost Function \( V(x(0), u) \)의 유도 과정**

LQ 문제에서 사용되는 Cost Function:

$$
\begin{align}
V(x(0), u) = \frac{1}{2} \sum_{k=0}^{N-1} \left( x(k)^T Q x(k) + u(k)^T R u(k) \right) + \frac{1}{2} x(N)^T P_f x(N)
\end{align}
$$

이 수식은 **최적 제어 문제**에서 시스템이 원하는 목표 상태(보통 원점)로 이동하면서, 입력 사용을 최소화하도록 유도하는 목적 함수를 나타낸다. 이를 유도하기 위해 다음과 같은 단계가 필요하다.

### **1. 기본적인 최적화 문제 설정**

주어진 시스템의 선형 상태공간 모델은 다음과 같다.

$$
\begin{align}
x(k+1) &= A x(k) + B u(k)
\end{align}
$$

LQ 문제에서는 이 시스템을 제어하여 특정 목표 상태로 이동시키는 것이 목표이다.

### **2. Cost Function 구성**

Cost Function는 두 가지 주요 항목으로 구성된다.

1. **Stage Cost**: 상태 및 입력의 크기를 최소화
   $$
   J_k = \frac{1}{2} \left( x(k)^T Q x(k) + u(k)^T R u(k) \right)
   $$
2. **Terminal Cost**: 마지막 상태 \( x(N) \)에 대한 추가적인 패널티
   $$
   J_N = \frac{1}{2} x(N)^T P_f x(N)
   $$
  - \( P_f \): 최종 상태에 대한 가중치 행렬 (시스템이 목표 상태에 더 가깝게 수렴하도록 유도)

최적화의 목표는 **모든 시간 단계에서의 Cost를 합산한 값**을 최소화하는 것이다.

### **3. 전체 Cost Function 정리**

위의 Cost를 모든 시간 단계에 대해 합산하면 다음과 같이 정리된다.

$$
\begin{align}
V(x(0), u) = \sum_{k=0}^{N-1} J_k + J_N
\end{align}
$$

이를 전개하면:

$$
\begin{align}
V(x(0), u) = \frac{1}{2} \sum_{k=0}^{N-1} \left( x(k)^T Q x(k) + u(k)^T R u(k) \right) + \frac{1}{2} x(N)^T P_f x(N)
\end{align}
$$

이 함수는 **상태 및 입력이 원점으로 수렴하도록 제어 입력을 결정하는 Cost Function**이며, 최적의 \( u(k) \)를 찾는 것이 LQ 최적 제어 문제의 핵심이다.

### **5. 정리**

**Cost Function \( V(x(0), u) \)의 의미**

- 상태가 원점에서 멀어질수록 cost이 증가
- 입력 크기가 클수록 cost이 증가
- 최종 상태를 고려하여 \( P_f \)를 설정

**Cost Function의 유도 과정**

1. 시스템 모델을 기반으로 상태 및 입력을 정의
2. 각 시간 단계에서 cost를 정의 (\( Q \) 및 \( R \)을 사용)
3. 전체 cost를 합산하여 최적화 문제를 설정
