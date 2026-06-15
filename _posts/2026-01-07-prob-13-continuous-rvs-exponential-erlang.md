---
layout: post
title: '[확률과 통계 13] Continuous RVs - Exponential and Erlang Distributions'
date: 2026-01-07 17:47:00 +0900
slug: prob-13-continuous-rvs-exponential-erlang
render_with_liquid: false
use_math: true
categories:
- 공부
- 확률과 통계
tags:
- 수업
last_modified_at: 2026-01-08 16:55:00 +0900
series: probability-statistics
series_order: 13
source:
  provider: notion
  id: 2e17c5f7-12ee-8077-8b5a-d85af0b12b66
---

연속 확률변수에서 자주 등장하는 분포로 Exponential 분포와 Erlang 분포가 있다. 둘 다 어떤 사건이 발생하기까지의 대기시간을 모델링할 때 많이 사용한다.

## Exponential Distribution

Exponential 분포는 하나의 사건이 발생할 때까지 걸리는 시간을 나타낸다.

$$
X \sim \operatorname{Exponential}(\lambda)
$$

여기서 $\lambda>0$는 발생률이다. PDF는

$$
f_X(x)
=
\begin{cases}
\lambda e^{-\lambda x}, & x \ge 0 \\
0, & x < 0
\end{cases}
$$

이고, CDF는

$$
F_X(x)
= P(X \le x)
= 1-e^{-\lambda x},
\qquad x \ge 0
$$

이다.

따라서 생존함수는

$$
P(X>x)=1-F_X(x)=e^{-\lambda x}
$$

로 쓸 수 있다.

평균과 분산은 다음과 같다.

$$
E[X]=\frac{1}{\lambda}
$$

$$
\operatorname{Var}(X)=\frac{1}{\lambda^2}
$$

## Memoryless Property

Exponential 분포의 중요한 특징은 memoryless property다.

이미 $t$만큼 기다렸다는 조건이 주어져도, 앞으로 $T$만큼 더 기다릴 확률은 처음부터 $T$만큼 기다릴 확률과 같다.

$$
P(X>t+T \mid X>t)=P(X>T)
$$

확인하면

$$
P(X>t+T \mid X>t)
= \frac{P(X>t+T)}{P(X>t)}
= \frac{e^{-\lambda(t+T)}}{e^{-\lambda t}}
= e^{-\lambda T}
= P(X>T)
$$

이다.

즉, Exponential 분포는 이미 기다린 시간이 앞으로의 대기시간 분포에 영향을 주지 않는다.

## Erlang Distribution

Erlang 분포는 여러 개의 독립적인 Exponential 대기시간을 더한 분포다.

사건이 한 번 발생할 때까지의 시간이 Exponential 분포를 따른다면, 사건이 $k$번 발생할 때까지의 전체 대기시간은 Erlang-$k$ 분포를 따른다.

$$
X_k = T_1 + T_2 + \cdots + T_k
$$

여기서 $T_1,\dots,T_k$가 서로 독립이고 같은 $\operatorname{Exponential}(\lambda)$ 분포를 따른다면

$$
X_k \sim \operatorname{Erlang}(k,\lambda)
$$

이다.

Erlang-$k$ 분포의 PDF는

$$
f_{X_k}(x)
=
\begin{cases}
\dfrac{\lambda^k x^{k-1}e^{-\lambda x}}{(k-1)!}, & x \ge 0 \\
0, & x < 0
\end{cases}
$$

이다.

$k=1$이면

$$
f_{X_1}(x)=\lambda e^{-\lambda x}
$$

가 되어 Exponential 분포와 같아진다. 따라서 Exponential 분포는 Erlang 분포의 특수한 경우다.

## Shape of Erlang Distribution

$k$가 커질수록 Erlang 분포는 여러 개의 독립 대기시간을 더한 형태가 된다. 이 때문에 분포의 모양이 점점 한쪽으로 치우친 형태에서 더 대칭적인 형태로 바뀐다.

이는 중심극한정리의 직관과 연결된다. 독립적인 확률변수들을 많이 더하면 합의 분포는 점점 Gaussian 분포에 가까워진다.

정리하면, Exponential 분포는 첫 사건까지의 대기시간을, Erlang 분포는 $k$번째 사건까지의 대기시간을 나타낸다.
