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
imported_images:
- assets/img/blog/prob-12-discrete-rvs-bernoulli-binomial/image-001.png
- assets/img/blog/prob-12-discrete-rvs-bernoulli-binomial/image-002.png
series: probability-statistics
series_order: 12
source:
  provider: notion
  id: 2e17c5f7-12ee-806c-8cdc-f140460d06bb
---

Bernoulli Distribution :

---
# 01) **Discrete RVs**
## 01_Summary of Discrete Random Variables
---
### ☾ 전체적인 요약
![](/assets/img/blog/prob-12-discrete-rvs-bernoulli-binomial/image-001.png)
- Bernoulli distribution : success혹은 occurrence를 확률 변수 (RV)로 두고 Independent 하게 iterative trials 한것
- Binomail distribution (몇번시도 했는가?)
- Geometric distribution (1번째 success가 나올때까지)
- Poisson distribution (Time 간격 안에)
## 02_Bernoulli Distribution
---
### ☾ Binary RV of success (or ocuraence)
- Success (or occurrence) → 1 (positive)
- Failure (or no occurrence) → 0 (negative)
$p(success)=p$,   $p(failure)=1-p$
$mean=p$,    $variance=p-p^2$
### ☾ Independent of successive trials
- 시도가 전부 독립적으로 이어진다.
### ☾ Example
- When tossing a coin, $P(Head)$ = $\frac{1}{2}$ → 다시 던지더라도 독립적인 관계임
- When tossing a dice $P(occuring\ 6)=\frac{1}{6}$  → 다시 던지더라도 독립적인 관계
- Accuray rate of pattern recognition system (car number, face ID, …)
- 각각의 사람들의 얼굴 인식 확률(경험적으로 얻은것을 바탕으로)
- All kinds of random phenomena with two opposite aspects → but independent해야함
### ☾ Basic unit trial for various discrete RVs
- of successes( or occurences) from independent iterative trials
- 다른 확률 분포의 기초가 되는 distributions이다. ↔Binomailm Geometric, Poisson distribution
## 03_Binomial Distribution
---
### ☾ X: # of successes (or occurrences) from total n Bernoulli trials
- X: \{0, 1, 2, 3, …, n\}
- parameter : $P(success)$ = $p$, total tirals $n$m
- →$B(n,p)$
$$
P(X=k)= {n \choose k}p^k(1-p)^{n-k}
$$

$$
mean=np,\ variance=np(1-p)
$$

![](/assets/img/blog/prob-12-discrete-rvs-bernoulli-binomial/image-002.png)

### ☾ Ex 1: Tossing a dice 10 times for $P(occuring\ 6)=\frac{1}{6}$
$$
P(X=k)= {10 \choose k}\left(\frac{1}{6}\right)^k\left(\frac{5}{6}\right)^{10-k}
$$
### ☾ Ex 2 : Testing a face recognition system for 100 persons
- $P(correct)=0.95$
$$
P(X=k)= {100 \choose k}0.95^k(0.05)^{100-k}
$$
### ☾ For $n\rightarrow \infty$, Binomial distribution is converged to Gaussian (Normal) distribution.
- n이 커지면 Binomail distribtion은 Gaussian Normal distribution
## 04_**Geometric Distributions**
---
### ☾ 정의 X : Bernoulli trial을 성공이 나올때 까지 반복했을때의 수
- $X:\{1,2,3,\ldots,n,\ldots\}$
- parameter : P(success)=$p$
- $P(X=k)=p(1-p)^{k-1}$<br>1번 성공할때까지 1-p의 의 확률 계속 반복한다.
- $mean=\frac{1}{p}$, $variance=\frac{1-p}{p^2}$
### ☾ Ex1 : 네트워크 서버 접속을 위한 시행
- N번하면 99%확률로 접속을 할수 있었으면 좋겠다.
$P(X\le N)=\sum^N_{k=1}p(1-p)^{k-1}>0.99$
### ☾ Ex2 : 네트워크 패킷이 성공적으로 받았다고 할때
## 05_**Geometric Distributions**
---
### ☾ 정의 X : 주어진 시간 내에 Bernoulli trial이 성공이 발생한 횟수
- $X:\{1,2,3,\ldots,n,\ldots\}$
- 시간 사이에는 전부 독립
- parameter : $\lambda>0$(mean)
- $P(X=k)=\frac{\lambda^ke^{-\lambda}}{k!}$
- $mean=\lambda$, $variance=\lambda$
- $P(x\geq1)=1-P(0)=1-e^{-\lambda}$ → 1회 이상 발생확률
