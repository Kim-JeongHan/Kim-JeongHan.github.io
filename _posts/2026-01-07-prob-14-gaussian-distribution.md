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
imported_images:
- assets/img/blog/prob-14-gaussian-distribution/image-001.png
- assets/img/blog/prob-14-gaussian-distribution/image-002.png
- assets/img/blog/prob-14-gaussian-distribution/image-003.png
- assets/img/blog/prob-14-gaussian-distribution/image-004.png
- assets/img/blog/prob-14-gaussian-distribution/image-005.png
series: probability-statistics
series_order: 14
source:
  provider: notion
  id: 2e17c5f7-12ee-805a-8cee-c586a2fe92f6
---

---
# 01) Gaussian (Normal) Distribution
## 01_Gaussian** distribution의 확률적 특징**
---
Gaussian distribution은 **노이즈가 많거나, 많은 시행의 결과를 근사 **할 때 가장 자주 등장하는 연속 확률분포이다. 특히 여러 독립적인 요인의 합으로 생성된 확률변수는 정규분포로 잘 근사된다.
### 기본 정의
- $\begin{aligned}X = \{\, x \mid -\infty < x < \infty \,\}\end{aligned}$
- $\mu$ : mean, $\sigma$ : standard deviation
- Notation :  $X \sim \mathcal{N}(\mu, \sigma^2)$
- PDF : $\begin{aligned}
f(x)
&= \frac{1}{\sqrt{2\pi}\,\sigma}
\exp\left(
-\frac{(x-\mu)^2}{2\sigma^2}
\right)
\end{aligned}$
![](/assets/img/blog/prob-14-gaussian-distribution/image-001.png)

**Gaussian Distribution의 주요 특징 (3가지)**
1. PDF는 항상 평균 $\mu$를 기준으로 좌우 대칭이다.
2. Large sample의 Approximate distribution
- Binomial distribution
- 동전 던지기에서 $n \to \infty$
- Erlang–K distribution
- $k \to \infty$

**Central Limit Theorem (CLT)**
서로 독립이고 동일한 분포(iid)를 따르는 확률변수 $n$개의 합은 $n$이 커질수록 정규분포에 수렴한다.

1.  Additive noise의 분포
- 여러 독립적인 잡음 성분이 더해진 신호의 noise는 Gaussian distribution으로 모델링하는 것이 합리적이다.
![](/assets/img/blog/prob-14-gaussian-distribution/image-002.png)
### Estimation 관점에서의 Gaussian Distribution
Gaussian distribution은 **추정(estimation)과 예측(prediction)** 관점에서 매우 이상적인 분포이다.
- unimodal(단봉) 분포
- mode = mean = median
- 발생 가능성이 가장 높은 값이 평균과 일치
- 최적 추정 성질
- **MMSE (Minimum Mean Square Error)**<br>→ 최적 추정값은 **mean**
- **Maximum Likelihood (ML) estimation**<br>→ 최적 추정값은 **mode (= mean)**
즉, 신호 처리에서 수행하는 **노이즈 제거, 필터링, 평균화** 과정은 본질적으로 Gaussian 확률 모델에 기반한 확률적 추정 문제이다.

### CDF of Gaussian distribution
Gaussian distribution의 누적 분포 함수는 다음과 같다.
$$
\begin{aligned}P(X \le x)&= \int_{-\infty}^{x}\frac{1}{\sqrt{2\pi},\sigma}\exp\left(-\frac{(X-\mu)^2}{2\sigma^2}\right)dX\end{aligned}
$$
변수 치환을 적용하면
$$
\begin{aligned}z &= \frac{X-\mu}{\sigma}, \qquad dz = \frac{1}{\sigma}dX\end{aligned}
$$
$$
\begin{aligned}P(X \le x)&= \int_{-\infty}^{\frac{x-\mu}{\sigma}}\frac{1}{\sqrt{2\pi}}\exp\left(-\frac{1}{2}z^2\right) dz\end{aligned}
$$
여기서
- $Z = \dfrac{X-\mu}{\sigma}$
- $Z \sim \mathcal{N}(0,1)$ : **Standard Normal Distribution**
즉,
$$
\begin{aligned}P(X \le x)&= \int_{-\infty}^{x}\frac{1}{\sqrt{2\pi},\sigma}\exp\left(-\frac{(X-\mu)^2}{2\sigma^2}\right) dX\end{aligned}
$$
### Standard Normal Distribution
표준 정규분포의 CDF는 다음과 같이 정의된다.
$$
\begin{aligned}\Phi(x)&= P(Z \le x) \\&= \int_{-\infty}^{x}\frac{1}{\sqrt{2\pi}}\exp\left(-\frac{1}{2}z^2\right)dz\end{aligned}
$$
$$
\Phi(-x) = 1 - \Phi(x)
$$
![](/assets/img/blog/prob-14-gaussian-distribution/image-003.png)
이를 이용해 **신뢰구간(confidence interval)** 을 다음과 같이 해석할 수 있다.<br>
![](/assets/img/blog/prob-14-gaussian-distribution/image-004.png)
## Error Function : erf(x)
Gaussian CDF를 계산하기 위해 정의된 **또 다른 형태의 함수**이다.
<table header-row="true">
<tr>
<td>Item</td>
<td>Standard Normal Distribution</td>
<td>Error Function</td>
</tr>
<tr>
<td>Transform (substitution)</td>
<td>$Z = \dfrac{X - \mu}{\sigma}$</td>
<td>$Y = \dfrac{X - \mu}{\sqrt{2}\sigma}$</td>
</tr>
<tr>
<td>CDF</td>
<td>$\Phi(x) = \displaystyle \int_{-\infty}^{x} \dfrac{1}{\sqrt{2\pi}} e^{-\frac{1}{2}z^2}dz$</td>
<td>$\operatorname{erf}(x) = \displaystyle \frac{2}{\sqrt{\pi}} \int_{0}^{x} e^{-y^2}dy$</td>
</tr>
</table>
$$
\begin{aligned}\operatorname{erf}(z)&= \frac{2}{\sqrt{\pi}}\int_{0}^{z}e^{-x^2}\, dx\end{aligned}
$$
적분 구간이 $(-\infty, x)$가 아니라 $(0,x)$이어 확률계산에 용이하다.
$$
\begin{aligned}\operatorname{erfc}(x)&= 1 - \operatorname{erf}(x)\end{aligned}
$$
![](/assets/img/blog/prob-14-gaussian-distribution/image-005.png)
