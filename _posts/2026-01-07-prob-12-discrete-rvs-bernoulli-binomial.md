---
layout: post
title: '[확률과 통계 12] Discrete RVs (Part 1) - Bernoulli and Binomial Distributions'
date: 2026-01-07 17:47:00 +0900
slug: prob-12-discrete-rvs-bernoulli-binomial
render_with_liquid: false
use_math: true
categories:
- 공부
- 확률과 통계
tags:
- 수업
last_modified_at: 2026-01-08 16:55:00 +0900
series: probability-statistics
series_order: 12
source:
  provider: notion
  id: 2e17c5f7-12ee-806c-8cdc-f140460d06bb
---

대표적인 이산 확률분포로 Bernoulli, Binomial, Geometric, Poisson 분포가 있다. 모두 성공과 실패, 시행 횟수, 사건 발생 횟수처럼 셀 수 있는 값을 다룬다.

## Bernoulli Distribution

Bernoulli 시행은 결과가 두 가지뿐인 실험이다. 보통 성공을 $1$, 실패를 $0$으로 둔다.

$$
X =
\begin{cases}
1, & \text{success} \\
0, & \text{failure}
\end{cases}
$$

성공 확률을 $p$라고 하면

$$
P(X=1)=p, \qquad P(X=0)=1-p
$$

이다. 이를 $X \sim \operatorname{Bernoulli}(p)$라고 쓴다.

평균은

$$
E[X] = 1 \cdot p + 0 \cdot (1-p)=p
$$

이고,

$$
E[X^2] = 1^2 \cdot p + 0^2 \cdot (1-p)=p
$$

이므로 분산은

$$
\operatorname{Var}(X)
= E[X^2]-E[X]^2
= p-p^2
= p(1-p)
$$

이다.

동전 던지기에서 앞면을 성공으로 두거나, 주사위에서 특정 눈이 나오는 사건을 성공으로 두면 Bernoulli 시행으로 볼 수 있다.

## Binomial Distribution

Binomial 분포는 독립적인 Bernoulli 시행을 $n$번 반복했을 때 성공 횟수 $X$의 분포다.

$$
X \sim \operatorname{Binomial}(n,p)
$$

$n$번 중 정확히 $k$번 성공할 확률은

$$
P(X=k)
= {n \choose k}p^k(1-p)^{n-k},
\qquad k=0,1,\dots,n
$$

이다.

여기서 ${n \choose k}$는 성공이 들어갈 위치를 고르는 경우의 수다. 각 경우는 성공 $k$번과 실패 $n-k$번을 포함하므로 확률이 $p^k(1-p)^{n-k}$가 된다.

Binomial 분포의 평균과 분산은 다음과 같다.

$$
E[X]=np
$$

$$
\operatorname{Var}(X)=np(1-p)
$$

즉, 성공 확률이 같은 독립 시행을 많이 반복하면 성공 횟수의 기대값은 시행 횟수와 성공 확률의 곱이다.

## Geometric Distribution

Geometric 분포는 첫 번째 성공이 나올 때까지 필요한 시행 횟수를 나타낸다.

$$
X \sim \operatorname{Geometric}(p)
$$

첫 성공이 $k$번째 시행에서 일어나려면 앞의 $k-1$번은 모두 실패하고, 마지막 $k$번째 시행에서 성공해야 한다.

$$
P(X=k)=p(1-p)^{k-1},
\qquad k=1,2,\dots
$$

평균과 분산은

$$
E[X]=\frac{1}{p}
$$

$$
\operatorname{Var}(X)=\frac{1-p}{p^2}
$$

이다.

예를 들어 서버 연결이 성공할 때까지 재시도하는 횟수, 혹은 어떤 실험에서 처음 성공이 나올 때까지 필요한 반복 횟수를 모델링할 수 있다.

## Poisson Distribution

Poisson 분포는 일정한 시간이나 공간 구간 안에서 사건이 몇 번 발생하는지를 나타낼 때 사용한다.

$$
X \sim \operatorname{Poisson}(\lambda)
$$

여기서 $\lambda$는 해당 구간에서의 평균 발생 횟수다. 확률질량함수는

$$
P(X=k)=\frac{\lambda^k e^{-\lambda}}{k!},
\qquad k=0,1,2,\dots
$$

이다.

Poisson 분포는 평균과 분산이 모두 $\lambda$다.

$$
E[X]=\lambda
$$

$$
\operatorname{Var}(X)=\lambda
$$

사건이 적어도 한 번 발생할 확률은 여집합을 이용해 계산할 수 있다.

$$
P(X \ge 1)
= 1-P(X=0)
= 1-e^{-\lambda}
$$

Bernoulli와 Binomial은 고정된 시행 안에서 성공 횟수를 세고, Geometric은 첫 성공까지의 시행 횟수를 세며, Poisson은 구간 안의 발생 횟수를 센다는 점에서 구분된다.
