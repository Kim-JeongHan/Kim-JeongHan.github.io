---
layout: post
title: '[확률과 통계 15] Solving Problems'
date: 2026-01-08 16:56:00 +0900
slug: prob-15-solving-problems
render_with_liquid: false
use_math: true
categories:
- 공부
- 확률과 통계
tags:
- 수업
last_modified_at: 2026-01-14 16:09:00 +0900
series: probability-statistics
series_order: 15
source:
  provider: notion
  id: 2e27c5f7-12ee-80f7-a40b-fd064a83ff69
---

문제 풀이에서 연속 확률변수의 PDF를 바로 추측하려고 하면 실수하기 쉽다. 먼저 CDF를 구한 뒤, 이를 미분해서 PDF를 얻는 흐름이 안정적이다.

$$
f_X(x)=\frac{dF_X(x)}{dx}
$$

## CDF and PDF

연속 확률변수 $X$에 대해 CDF는 다음과 같이 정의된다.

$$
F_X(x)=P(X \le x)
$$

PDF는 CDF의 미분이다.

$$
f_X(x)=\frac{d}{dx}F_X(x)
$$

따라서 문제를 풀 때는 다음 순서가 좋다.

1. $X \le x$가 의미하는 사건을 해석한다.
2. 그 사건의 확률을 기하학적 비율이나 주어진 분포로 계산한다.
3. CDF $F_X(x)$를 구한다.
4. CDF를 미분해서 PDF $f_X(x)$를 얻는다.

## Example: Uniform Point in a Sphere

반지름이 $R$인 구 내부에서 한 점을 균일하게 선택한다고 하자. 중심으로부터의 거리를 확률변수 $X$라고 두면 $X$는 $0$부터 $R$ 사이의 값을 가진다.

이때 $X \le x$라는 사건은 선택된 점이 반지름 $x$인 작은 구 안에 들어간다는 뜻이다.

균일하게 선택하므로 확률은 부피 비율로 계산할 수 있다.

$$
F_X(x)
= P(X \le x)
= \frac{\frac{4}{3}\pi x^3}{\frac{4}{3}\pi R^3}
= \frac{x^3}{R^3},
\qquad 0 \le x \le R
$$

전체 구간까지 포함하면 CDF는 다음과 같다.

$$
F_X(x)
=
\begin{cases}
0, & x < 0 \\
\dfrac{x^3}{R^3}, & 0 \le x \le R \\
1, & x \ge R
\end{cases}
$$

PDF는 CDF를 미분해서 얻는다.

$$
f_X(x)
=
\begin{cases}
\dfrac{3x^2}{R^3}, & 0 \le x \le R \\
0, & \text{otherwise}
\end{cases}
$$

밀도가 $x$가 커질수록 증가하는 이유는 중심에서 멀어질수록 같은 두께의 구 껍질이 차지하는 부피가 커지기 때문이다.

## Takeaway

연속 확률변수 문제에서 PDF가 바로 보이지 않으면 CDF부터 잡는 것이 좋다. 특히 기하학적 확률 문제에서는 $X \le x$가 나타내는 영역을 먼저 해석하고, 전체 영역 대비 비율을 구한 뒤 미분하면 자연스럽게 PDF가 나온다.
