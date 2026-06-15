---
layout: post
title: '[확률과 통계 14] Continuous RVs - Gaussian Distribution'
date: 2026-01-07 17:47:00 +0900
slug: prob-14-gaussian-distribution
render_with_liquid: false
use_math: true
categories:
- 공부
- 확률과 통계
tags:
- 수업
last_modified_at: 2026-01-08 16:57:00 +0900
series: probability-statistics
series_order: 14
source:
  provider: notion
  id: 2e17c5f7-12ee-805a-8cee-c586a2fe92f6
---

Gaussian distribution, 즉 정규분포는 연속 확률분포 중 가장 많이 쓰이는 분포다. 측정 오차, 잡음, 많은 독립 확률변수의 합이나 평균을 다룰 때 자연스럽게 등장한다.

## Gaussian Distribution

확률변수 $X$가 평균 $\mu$, 분산 $\sigma^2$인 Gaussian 분포를 따르면 다음처럼 쓴다.

$$
X \sim \mathcal{N}(\mu,\sigma^2)
$$

PDF는

$$
f_X(x)
= \frac{1}{\sqrt{2\pi}\sigma}
\exp\left(
-\frac{(x-\mu)^2}{2\sigma^2}
\right),
\qquad -\infty < x < \infty
$$

이다.

여기서 $\mu$는 분포의 중심, $\sigma$는 퍼짐 정도를 나타낸다. 분산은 $\sigma^2$다.

## Main Properties

Gaussian 분포는 평균 $\mu$를 기준으로 대칭이다.

$$
f_X(\mu-a)=f_X(\mu+a)
$$

또한 많은 독립 확률변수의 합이나 평균은 조건이 적절하면 Gaussian 분포에 가까워진다. 이것이 중심극한정리의 핵심 직관이다.

측정값은 실제 값에 여러 작은 오차가 더해진 결과로 볼 수 있다. 그래서 센서 노이즈나 측정 오차를 Gaussian 분포로 모델링하는 경우가 많다.

## CDF

Gaussian 분포의 CDF는 PDF를 적분해서 얻는다.

$$
F_X(x)
= P(X \le x)
= \int_{-\infty}^{x}
\frac{1}{\sqrt{2\pi}\sigma}
\exp\left(
-\frac{(t-\mu)^2}{2\sigma^2}
\right)\,dt
$$

이 적분은 일반적인 초등함수로 닫힌 형태를 만들 수 없기 때문에 표준정규분포표나 계산 함수를 이용한다.

## Standard Normal Distribution

평균이 $0$, 분산이 $1$인 Gaussian 분포를 표준정규분포라고 한다.

$$
Z \sim \mathcal{N}(0,1)
$$

PDF는

$$
\phi(z)
= \frac{1}{\sqrt{2\pi}}e^{-z^2/2}
$$

이고 CDF는

$$
\Phi(x)
= P(Z \le x)
= \int_{-\infty}^{x}
\frac{1}{\sqrt{2\pi}}e^{-z^2/2}\,dz
$$

이다.

표준정규분포는 $0$을 기준으로 대칭이므로

$$
\Phi(-x)=1-\Phi(x)
$$

가 성립한다.

일반 Gaussian 확률변수 $X \sim \mathcal{N}(\mu,\sigma^2)$는 표준화해서 표준정규분포로 바꿀 수 있다.

$$
Z=\frac{X-\mu}{\sigma}
$$

그러면

$$
P(a \le X \le b)
= P\left(
\frac{a-\mu}{\sigma}
\le Z \le
\frac{b-\mu}{\sigma}
\right)
$$

처럼 표준정규분포의 CDF로 확률을 계산할 수 있다.

## Error Function

Gaussian CDF는 error function과도 연결된다.

$$
\operatorname{erf}(z)
= \frac{2}{\sqrt{\pi}}
\int_0^z e^{-x^2}\,dx
$$

상보 오차 함수는

$$
\operatorname{erfc}(x)
= 1-\operatorname{erf}(x)
$$

이다.

표준정규분포 CDF는 error function을 이용해 다음처럼 쓸 수 있다.

$$
\Phi(x)
= \frac{1}{2}
\left[
1+\operatorname{erf}\left(\frac{x}{\sqrt{2}}\right)
\right]
$$

Gaussian 분포는 직접 적분하기 어려운 형태지만, 표준화와 표준정규분포 CDF를 이용하면 실제 확률 계산을 체계적으로 처리할 수 있다.
