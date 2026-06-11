---
layout: post
title: '[확률과 통계 20] Covariance of two RVs'
date: 2026-01-15 10:29:53 +0900
slug: prob-20-covariance-two-rvs
render_with_liquid: false
use_math: true
categories:
- 공부
- 확률과 통계
tags: []
last_modified_at: 2026-01-16 08:24:03 +0900
imported_images:
- assets/img/tistory/87/image-001.png
- assets/img/tistory/87/image-002.png
series: probability-statistics
series_order: 20
source:
  provider: tistory
  id: 87
---

# 01) **Covariance**

## 00_서론

분산 ${\mathrm{Var}(X)}$이 single random variable의 퍼짐 정도를 측정한다면 공분산 ${\mathrm{Cov}(X,Y)}$는 two random variables가 함께 변하는 경향을 정량화한다.

공분산의 핵심 목적은 ${X}$가 평균보다 커지거나 작아질 때 ${Y}$도 같은 방향으로 움직이는지, 반대 방향으로 움직이는지, 혹은 선형적 경향이 거의 없는지를 수식으로 판별하는 데 있다.

## 01_Variance 복습

### 정의

$$
\mathrm{Var}(X)=\mathbb{E}\big[(X-\mu_X)^2\big],\quad \mu_X=\mathbb{E}[X]
$$

변수가 평균으로부터 벗어난 편차의 제곱의 기댓값

- $x,P(x)$평면으로의 해석 : 높은 확률값을 갖는 어떤 random variable의 범위라고 좀더 정확하게 이야기할수 있다.
- $t,x$평면으로의 해석 : 반복적으로 random variable 발생시킬때, 평균값을 기준으로 편차의 크기가 얼마나 큰지로 볼수 있다.

![](/assets/img/tistory/87/image-001.png)

![](/assets/img/tistory/87/image-002.png)

- 물리적, 수학적 : Sinal의 engegy or power
  $x^2(t) \rightarrow \text{power}$, $\frac{1}{T}\int_{0}^{T} x(t), dt \rightarrow \text{Mean of engergy}$

## 02_Covariance 정의와 해석

### 정의

$$
\mathrm{Cov}(X,Y)=\mathbb{E}\big[(X-\mu_X)(Y-\mu_Y)\big] = E[XY] - \mu_X\mu_Y
$$

이 평균 중심점 ${(\mu_X,\mu_Y)}$에서의 두 편차 ${(X-\mu_X)}$와 ${(Y-\mu_Y)}$가 같은 부호로 자주 나타나는지, 반대 부호로 자주 나타나는지를 기대값으로 측정한다.

$(X-\mu_X)(Y-\mu_Y)$는 두 편차가 같은 방향이면 positive, 반대 방향이면 negative가 된다.

이를 통해 X와 Y의 연관성과 경향성을 볼수 있다.(correlation)

### 해석

- $xy,P(x)$ 공간으로의 해석 : 높은 확률값을 갖는 어떤 random variable의 범위라고 좀더 정확하게 이야기할수 있다.
- $t,xy$평면으로의 해석 : 반복적으로 random variable 발생시킬때, 평균값을 기준으로 xy를 곱한 편차의 크기가 얼마나 큰지로 볼수 있다.

공분산의 부호 해석은 다음과 같이 정리된다.

- ${\mathrm{Cov}(X,Y)>0}$ → ${X}$가 평균보다 커질 때 ${Y}$도 평균보다 커지는 경향이 강하다.
- ${\mathrm{Cov}(X,Y)<0}$ → ${X}$가 평균보다 커질 때 ${Y}$는 평균보다 작아지는 경향이 강하다.
- ${\mathrm{Cov}(X,Y)=0}$ → linear relationship 관점에서 무상관(uncorrelated)이다.

## 03_공분산 계산식: discrete → continuous 연결

discrete random variable에서 Joint Distribution이 주어지면 ${P_{XY}(x,y)}$로 공분산을 계산한다.

$$
\mathrm{Cov}(X,Y)=\sum_x\sum_y (x-\mu_X)(y-\mu_Y),P_{XY}(x,y)
$$

연속으로 확장되면 double sum이 double integral로 바뀌고 ${P_{XY}(x,y)}$가 ${f_{XY}(x,y)}$로 바뀐다.

$$
\mathrm{Cov}(X,Y)=\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}(x-\mu_X)(y-\mu_Y),f_{XY}(x,y),dx,dy
$$

계산 효율을 위해 두 경우 모두 다음 형태를 자주 사용한다.

- discrete random variable
  $$
  \mathrm{Cov}(X,Y)=\sum_x\sum_y xyP_{XY}(x,y)-\mu_X\mu_Y
  $$
- continuous random variable
  $$
  \mathrm{Cov}(X,Y)=\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}xyf_{XY}(x,y),dx,dy-\mu_X\mu_Y
  $$

## 04_Uncorrelated와 Independent의 관계

### Uncorrelated

uncorrelated은 공분산이 0인 경우로 정의된다.

$$
\mathrm{Cov}(X,Y)=0\ \Longleftrightarrow\ \mathbb{E}[XY]=\mathbb{E}[X]\mathbb{E}[Y]
$$

### Independent

Independent은 Joint Distribution이 Marginal Distribution의 곱이 되는 좀더 강한 조건이다.

- continuous random variable: ${f_{XY}(x,y)=f_X(x)f_Y(y)}$
- discrete random variable: ${P_{XY}(x,y)=P_X(x)P_Y(y)}$

### 관계

$$
\begin{aligned}E[XY]&= \iint xy, f_{XY}(x, y), dx, dy \&= \iint xy, f_X(x), f_Y(y), dx, dy \&= \mu_X \mu_Y\end{aligned}
$$

독립이면 항상 무상관이 성립한다.

정리하면 다음 방향만 일반적으로 성립한다.

- Independence → Uncorrelated
- Uncorrelated ⇏ Independence

## 05_예제 1: discrete random variable

### 문제 정의

- 실험: 공정한 동전을 3회 던진다.
- random variable: ${X}$는 1회차가 앞면이면 1, 뒷면이면 0이고 ${Y}$는 3회 중 앞면의 총 횟수이다.
- 목표: ${\mathrm{Cov}(X,Y)}$를 계산한다.

### 모델링

- ${X\in{0,1}}$, ${Y\in{0,1,2,3}}$

### 수식 전개

1. ${\mathbb{E}[X]=0\cdot\frac12+1\cdot\frac12=\frac12}$
2. ${\mathbb{E}[Y]=3\cdot\frac12=\frac32}$
3. ${\mathbb{E}[XY]=\sum_x\sum_y xy,P_{XY}(x,y)}$에서 ${x=1}$인 항만 남으므로 ${\mathbb{E}[XY]=1}$
4. ${\mathrm{Cov}(X,Y)=\mathbb{E}[XY]-\mathbb{E}[X]\mathbb{E}[Y]=1-\frac12\cdot\frac32=\frac14}$

### 결과 해석

${\mathrm{Cov}(X,Y)=\frac14>0}$이므로 1회차가 앞면인 경우 ${Y}$가 커지는 방향의 선형 경향이 있다.

## 06_예제 2: continuous random variable

### 문제 정의

- Joint PDF: ${f_{XY}(x,y)=2e^{-x}e^{-y}}$
- 조건: ${0\le x\le y<\infty}$
- 목표: ${\mathrm{Cov}(X,Y)}$를 계산한다.

### 모델링

- Support ${0\le x\le y}$는 1사분면에서 직선 ${y=x}$ 위쪽 영역이며 ${Y}$가 ${X}$보다 작아질 수 없도록 제약한다.

### 수식 전개

1. Marginal PDF
   $$
   f_Y(y)=\int_0^{y}2e^{-x}e^{-y},dx=2e^{-y}(1-e^{-y}),\quad y\ge0
   $$
   $$
   f_X(x)=\int_x^{\infty}2e^{-x}e^{-y},dy=2e^{-2x},\quad x\ge0
   $$
2. 기대값
   $$
   \mathbb{E}[Y]=\int_0^{\infty}y,2e^{-y}(1-e^{-y}),dy=\frac32
   $$
   $$
   \mathbb{E}[X]=\int_0^{\infty}x,2e^{-2x},dx=\frac12
   $$
3. 결합 기대값
   $$
   \mathbb{E}[XY]=\int_0^{\infty}\int_x^{\infty}xy,2e^{-x}e^{-y},dy,dx=1
   $$
4. 공분산
   $$
   \mathrm{Cov}(X,Y)=\mathbb{E}[XY]-\mathbb{E}[X]\mathbb{E}[Y]=1-\frac12\cdot\frac32=\frac14
   $$

### 결과 해석

${\mathrm{Cov}(X,Y)=\frac14>0}$는 ${y\ge x}$라는 Support 제약과 일관되며 ${X}$가 커질수록 ${Y}$도 함께 커지는 방향의 선형 경향이 생긴다.

## 07_정리

공분산은 선형적 관계의 방향성을 제공하지만 값의 크기는 단위와 스케일에 직접 의존하므로 서로 다른 변수 쌍의 관계 강도를 공분산만으로 비교하기는 어렵다.

이 한계를 해결하기 위해 공분산을 표준편차로 정규화한 Correlation Coefficient를 정의한다.

$$
\rho_{XY}=\frac{\mathrm{Cov}(X,Y)}{\sigma_X\sigma_Y},\quad \sigma_X=\sqrt{\mathrm{Var}(X)},\ \sigma_Y=\sqrt{\mathrm{Var}(Y)}
$$
