---
layout: post
title: '[확률과 통계 11] Conditional Mean and Variance'
date: 2026-01-07 17:47:00 +0900
slug: prob-11-conditional-mean-variance
render_with_liquid: false
use_math: true
categories:
- 공부
- 확률과 통계
tags:
- 수업
last_modified_at: 2026-01-08 16:55:00 +0900
series: probability-statistics
series_order: 11
source:
  provider: notion
  id: 2e17c5f7-12ee-80f5-b477-fbb21473b71f
---

확률변수의 평균과 분산은 조건을 걸었을 때도 같은 방식으로 정의할 수 있다. 다만 전체 표본공간이 아니라 조건 $A$가 일어난 세계에서의 확률분포를 먼저 다시 잡아야 한다.

이산형에서는 조건부 확률을 쓰고, 연속형에서는 조건부 CDF와 PDF를 만든 뒤 평균과 분산을 계산한다.

## Conditional Mean

확률변수 $X$와 사건 $A$가 있을 때 조건부 평균은 다음처럼 쓴다.

$$
E[X \mid A]
$$

예를 들어 주사위를 한 번 던져 나온 눈을 $X$라고 하자.

$$
X \in \{1,2,3,4,5,6\}, \qquad P(X=k)=\frac{1}{6}
$$

이때 단순 평균은 전체 경우를 기준으로 계산하지만, 어떤 조건 $A$가 주어지면 $A$ 안에서의 확률만 다시 정규화해서 평균을 계산해야 한다.

## Conditional Mean and Variance

조건 $A$가 주어졌을 때의 평균과 분산은 다음과 같다.

이산형 확률변수에서는

$$
E[X \mid A] = \sum_x x P(X=x \mid A)
$$

$$
\operatorname{Var}(X \mid A)
= E[X^2 \mid A] - E[X \mid A]^2
$$

연속형 확률변수에서는 조건부 밀도함수 $f_{X \mid A}(x)$를 이용한다.

$$
E[X \mid A] = \int_{-\infty}^{\infty} x f_{X \mid A}(x)\,dx
$$

$$
\operatorname{Var}(X \mid A)
= \int_{-\infty}^{\infty} x^2 f_{X \mid A}(x)\,dx
- E[X \mid A]^2
$$

핵심은 조건부 평균 자체보다 조건부 확률분포를 먼저 구하는 것이다.

## Conditional Density

연속형 확률변수 $X$에 대해 사건 $A=\{X \le a\}$를 생각하자. 이때 조건부 CDF는

$$
F_{X \mid A}(x)
= P(X \le x \mid X \le a)
$$

이고, 조건부 PDF는 이를 미분해서 얻는다.

$$
f_{X \mid A}(x)
=
\begin{cases}
\dfrac{f_X(x)}{F_X(a)}, & x \le a \\
0, & x > a
\end{cases}
$$

따라서 조건부 평균은

$$
E[X \mid A]
= \int_{-\infty}^{a} x \frac{f_X(x)}{F_X(a)}\,dx
$$

가 된다.

## Example: $A=\{X \le 1\}$

만약 $F_X(1)=\frac{1}{2}$이고, $0 \le x \le 1$에서 $f_X(x)=x$라면 조건부 밀도는

$$
f_{X \mid A}(x)=2x, \qquad 0 \le x \le 1
$$

이다.

그러면 조건부 평균은

$$
E[X \mid A]
= \int_0^1 x \cdot 2x\,dx
= \int_0^1 2x^2\,dx
= \frac{2}{3}
$$

이고,

$$
E[X^2 \mid A]
= \int_0^1 x^2 \cdot 2x\,dx
= \int_0^1 2x^3\,dx
= \frac{1}{2}
$$

이므로 조건부 분산은

$$
\operatorname{Var}(X \mid A)
= \frac{1}{2} - \left(\frac{2}{3}\right)^2
= \frac{1}{18}
$$

이다.

## Interval Condition

사건이 $A=\{a < X \le b\}$처럼 구간으로 주어지면, 조건부 밀도는 구간 안에서만 원래 밀도를 정규화한 형태가 된다.

$$
f_{X \mid A}(x)
=
\begin{cases}
\dfrac{f_X(x)}{F_X(b)-F_X(a)}, & a < x \le b \\
0, & \text{otherwise}
\end{cases}
$$

따라서

$$
E[X \mid A]
= \int_a^b x \frac{f_X(x)}{F_X(b)-F_X(a)}\,dx
$$

로 계산한다.

조건부 평균과 조건부 분산은 결국 조건에 의해 잘린 영역에서 확률분포를 다시 만든 뒤, 그 분포의 평균과 분산을 구하는 문제다.
