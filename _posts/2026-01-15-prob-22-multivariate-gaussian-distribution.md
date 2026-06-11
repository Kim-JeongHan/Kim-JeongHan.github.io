---
layout: post
title: '[확률과 통계 22] Multivariate Gaussian Distribution'
date: 2026-01-15 15:22:50 +0900
slug: prob-22-multivariate-gaussian-distribution
render_with_liquid: false
use_math: true
categories:
- 공부
- 확률과 통계
tags: []
last_modified_at: 2026-01-16 08:24:14 +0900
imported_images:
- assets/img/blog/prob-22-multivariate-gaussian-distribution/image-001.png
- assets/img/blog/prob-22-multivariate-gaussian-distribution/image-002.png
- assets/img/blog/prob-22-multivariate-gaussian-distribution/image-003.png
- assets/img/blog/prob-22-multivariate-gaussian-distribution/image-004.png
- assets/img/blog/prob-22-multivariate-gaussian-distribution/image-005.png
- assets/img/blog/prob-22-multivariate-gaussian-distribution/image-006.png
series: probability-statistics
series_order: 22
source:
  provider: tistory
  id: 88
---

# 01) **Multivariate Gaussian Distribution: Joint, Marginal, Conditional**

## 00_서론

**Multivariate Gaussian Distribution**는 여러 공학 문제에서 불확실성을 벡터 형태로 모델링할 때 가장 자주 쓰이는 분포이며, 평균과 공분산만으로 구조가 정해진다는 점에서 계산이 일관되고 예측 가능하다.

## 01_Bivariate Gaussian과 Joint PDF

### Joint PDF 정의

연속 확률 변수 ${X, Y}$가 **Joint Gaussian**이라면 **Joint PDF** ${f_{XY}(x,y)}$는 다음과 같이 쓸 수 있다.

$$
f_{XY}(x,y)=\frac{1}{2\pi\sigma_x\sigma_y\sqrt{1-\rho^2}}\exp\left(-\frac{1}{2(1-\rho^2)}\left[\frac{(x-\mu_x)^2}{\sigma_x^2}-\frac{2\rho(x-\mu_x)(y-\mu_y)}{\sigma_x\sigma_y}+\frac{(y-\mu_y)^2}{\sigma_y^2}\right]\right)
$$

- ${\mu_x,\mu_y}$는 각 변수의 **Mean**이다.
- ${\sigma_x,\sigma_y}$는 각 변수의 **Standard Deviation**이다.
- ${\rho}$는 **Correlation Coefficient**이며 ${-1\le \rho \le 1}$이다.

또한 이를 Bivariate Gaussian이라고 한다.

### 해석

${f_{XY}(x,y)}$는 점 ${(x,y)}$ 주변의 ${dx,dy}$에서 확률이 어떻게 축적되는지를 나타내는 밀도이며 ${P((X,Y)\in A)=\iint_A f_{XY}(x,y)\,dx\,dy}$로 확률이 계산된다.

지수항의 이차식은 평균 ${( \mu_x,\mu_y)}$로부터의 상대적 거리와 방향성을 동시에 반영하며, ${\rho}$가 0이 아닐 때 교차항 ${(x-\mu_x)(y-\mu_y)}$가 등장하여 두 축이 섞인 형태의 밀도 구조가 만들어진다.

### 기하학적 해석

- ${f_{XY}(x,y)}$의 등밀도 곡선은 ${x\text{-}y}$ 평면에서 **ellipse**가 된다.
- ${\rho=0}$이면 ellipse의 주축이 좌표축과 정렬된다.
- ${\rho\neq 0}$이면 ellipse가 회전하며, 이는 두 변수가 함께 변하는 방향이 존재함을 의미한다.

![](/assets/img/blog/prob-22-multivariate-gaussian-distribution/image-001.png)

## 02_Marginalization과 Uncorrelated, Independent

### Marginalization 정의

연속 확률 변수에서 **Marginal PDF**는 다른 변수를 적분으로 소거하여 얻는다.

$$
f_X(x)=\int_{-\infty}^{\infty} f_{XY}(x,y)\,dy,\qquad f_Y(y)=\int_{-\infty}^{\infty} f_{XY}(x,y)\,dx
$$

### **Joint가 Gaussain이면 marginal 도 Gaussian 의 증명**

증명의 목표는 ${f_Y(y)}$를 계산했을 때 결과가 ${\mathcal{N}(\mu_y,\sigma_y^2)}$의 형태로 정리됨을 보이는 것이다.

$$
\begin{aligned}f_Y(y)&= \int_{-\infty}^{\infty} f_{XY}(x,y)\, dx \\&= \int_{-\infty}^{\infty}\frac{1}{2\pi \sigma_X \sigma_Y \sqrt{1-\rho^2}}\exp\left[-\frac{1}{2(1-\rho^2)}\left(\frac{(x-\mu_X)^2}{\sigma_X^2}- \frac{2\rho(x-\mu_X)(y-\mu_Y)}{\sigma_X\sigma_Y}+ \frac{(y-\mu_Y)^2}{\sigma_Y^2}\right)\right] dx\end{aligned}
$$

1. 변수치환
   $$
   \begin{aligned}X = \frac{x-\mu_X}{\sigma_X}, Y = \frac{y-\mu_Y}{\sigma_Y}\end{aligned}
   $$
2. 지수항을 표준화 변수로 정리한다.
   $$
   \frac{(x-\mu_x)^2}{\sigma_x^2}-\frac{2\rho(x-\mu_x)(y-\mu_y)}{\sigma_x\sigma_y}+\frac{(y-\mu_y)^2}{\sigma_y^2}
   = X'^2-2\rho X'Y'+Y'^2
   $$
3. 완전제곱식으로 변형한다.
   $$
   \begin{aligned}X'^2 - 2\rho X'Y' + Y'^2&= (X' - \rho Y')^2 + (1-\rho^2)Y'^2\end{aligned}
   $$
4. 적분을 분리 가능한 형태로 바꾼다.
   $$
   \begin{aligned}f_Y(y)&= \int_{-\infty}^{\infty}\frac{1}{2\pi \sigma_X \sigma_Y \sqrt{1-\rho^2}}\exp\left[-\frac{(X'-\rho Y')^2}{2(1-\rho^2)}\right]\exp\left[-\frac{Y'^2}{2}\right]\, dx\end{aligned}
   $$
5. ${X'}$에 대한 항만 적분으로 소거하고, ${y}$에 대한 항은 적분 밖으로 꺼낸다.
   $$
   f_Y(y)=\frac{1}{2\pi\sigma_y\sqrt{1-\rho^2}}\exp\left(-\frac{Y'^2}{2}\right)\int_{-\infty}^{\infty}\exp\left(-\frac{(X'-\rho Y')^2}{2(1-\rho^2)}\right)dX'
   $$
6. 표준 가우시안 적분으로 치환한다.
   ${U=\frac{X'-\rho Y'}{\sqrt{1-\rho^2}}}$로 두면 ${dX'=\sqrt{1-\rho^2}\,dU}$이고 적분 구간은 ${-\infty}$에서 ${\infty}$로 그대로 유지된다.
   $$
   \int_{-\infty}^{\infty}\exp\left(-\frac{(X'-\rho Y')^2}{2(1-\rho^2)}\right)dX'
   =\sqrt{1-\rho^2}\int_{-\infty}^{\infty}e^{-U^2/2}\,dU
   =\sqrt{1-\rho^2}\sqrt{2\pi}
   $$
7. 상수를 정리하여 최종 형태를 얻는다.
   $$ f_Y(y)=\frac{\sqrt{1-\rho^2}\sqrt{2\pi}}{2\pi\sigma_y\sqrt{1-\rho^2}}\exp\left(-\frac{1}{2}\left(\frac{y-\mu_y}{\sigma_y}\right)^2\right)
   = \frac{1}{\sqrt{2\pi}\sigma_y}\exp\left(-\frac{1}{2}\left(\frac{y-\mu_y}{\sigma_y}\right)^2\right) $$

→ ${f_Y(y)}$는 평균 ${\mu_y}$, 분산 ${\sigma_y^2}$인 1차원 가우시안 **Marginal PDF**이며, 적분은 ${x}$를 소거하여 ${y}$에 대한 지수항만 남기는 과정으로 해석된다.

같은 계산을 ${y}$에 대해 적분하면 ${f_X(x)=\frac{1}{\sqrt{2\pi}\sigma_x}\exp\left(-\frac{1}{2}\left(\frac{x-\mu_x}{\sigma_x}\right)^2\right)}$가 얻어지며, 따라서 **Marginals are Gaussian**이 성립한다.

${(X,Y)}$가 **Joint Gaussian**이면 ${f_X(x)}$와 ${f_Y(y)}$는 각각 1차원 가우시안이 된다.

$$
X\sim \mathcal{N}(\mu_x,\sigma_x^2),\qquad Y\sim \mathcal{N}(\mu_y,\sigma_y^2)
$$

### Uncorrelated implies Independent in Joint Gaussian

일반적으로 **Uncorrelated** ${Cov(X,Y)=0}$만으로 **Independent**를 보장할 수는 없지만, **Joint Gaussian**에서는 이 결론이 성립한다.

- **Uncorrelated**는 ${Cov(X,Y)=0}$ 또는 ${\rho=0}$을 의미한다.
- **Independent**는 ${f_{XY}(x,y)=f_X(x)f_Y(y)}$를 의미한다.

two variable 가우시안의 **Joint PDF**에서 ${\rho=0}$을 대입하면 교차항이 사라지고 지수항이 ${x}$만의 항과 ${y}$만의 항으로 분리되어 ${f_{XY}(x,y)=f_X(x)f_Y(y)}$ 꼴이 된다.

## 03_타원 등고선, 회전 각도 ${\theta}$, 그리고 ${\rho}$의 기하학

two variable 가우시안의 등밀도 곡선은 지수부의 이차형식인 타원으로 주어지며, 교차항이 존재하면 타원은 회전된 좌표계에서 축 정렬 형태가 된다.

- ${\rho=0}$이면 교차항이 사라지고 타원 축이 ${x,y}$축과 정렬되며, 이때 두 변수는 uncorrelated가 된다.

![](/assets/img/blog/prob-22-multivariate-gaussian-distribution/image-002.png)

- ${\rho\neq 0}$이면 교차항이 존재하고 타원은 어떤 각도 ${\theta}$만큼 회전된 축을 갖는다.

![](/assets/img/blog/prob-22-multivariate-gaussian-distribution/image-003.png)

회전 변환은 다음과 같이 정의한다.

$$
\begin{aligned}
\begin{bmatrix}x' \ y'\end{bmatrix}
=
\begin{bmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{bmatrix}
\begin{bmatrix}x \ y\end{bmatrix}
\end{aligned}
$$

이 회전은 공분산 행렬을 대각화(diagonalize)하는 동작과 동일하며, 회전된 좌표계에서는 교차항이 제거되어 uncorrelated한 두 축 성분을 얻게 된다.

결합 가우시안에서는 uncorrelated가 independent를 의미하므로, 회전된 좌표계에서 ${x'}$와 ${y'}$는 independent한 가우시안으로 분리된다.

### ${\theta}$ 공식의 유도

공분산 행렬을 다음과 같이 둔다.

$$
\begin{aligned}
\mathbf{C}=
\begin{bmatrix}
\sigma_X^2 & \rho\sigma_X\sigma_Y \\
\rho\sigma_X\sigma_Y & \sigma_Y^2
\end{bmatrix}
\end{aligned}
$$

회전 행렬을 ${\mathbf{R}(\theta)}$라 하면, 회전된 좌표계의 공분산은 ${\mathbf{C}'=\mathbf{R}^\top\mathbf{C}\mathbf{R}}$이고, 대각화를 위해서는 ${\mathbf{C}'}$의 비대각 원소가 0이어야 한다.

$$
\begin{aligned}
(\mathbf{C}'){12}&=(\sigma_X^2-\sigma_Y^2)\sin\theta\cos\theta+\rho\sigma_X\sigma_Y(\cos^2\theta-\sin^2\theta)\end{aligned}
$$

*삼각함수 항등식 ${\sin2\theta=2\sin\theta\cos\theta}$, ${\cos2\theta=\cos^2\theta-\sin^2\theta}$를 사용하면 다음과 같이 정리된다.*

$$
\begin{aligned}(\mathbf{C}'){12}=0\quad\Rightarrow\quad\frac{\sigma_X^2-\sigma_Y^2}{2}\sin2\theta+\rho\sigma_X\sigma_Y\cos2\theta=0\quad\Rightarrow\quad\tan2\theta=\frac{2\rho\sigma_X\sigma_Y}{\sigma_X^2-\sigma_Y^2}\end{aligned}
$$

따라서 회전 각도는 다음과 같이 쓸 수 있다.

$$
\begin{aligned}\theta= \frac{1}{2}\tan^{-1}\left(\frac{2\rho,\sigma_X \sigma_Y}{\sigma_X^2 - \sigma_Y^2}\right)\end{aligned}
$$

→${\theta}$는 데이터 구름의 주축 방향의 각도를 나타내며, ${\rho}$가 커질수록 타원은 대각선 방향으로 더 강하게 기울어진다.

## 04_샘플로부터 ${\rho}$를 역으로 추정하는 방법과 한계

![](/assets/img/blog/prob-22-multivariate-gaussian-distribution/image-004.png)

데이터만 존재하고 분포 파라미터를 모르는 상황에서는 샘플 평균과 샘플 공분산을 이용해 ${\rho}$를 추정할 수 있으며, 이 값은 정밀하지는 않지만 가우시안 모델을 역으로 맞추는 출발점이 된다.

- 문제 정의: 관측 데이터 ${{(x_i,y_i)}_{i=1}^N}$만 주어졌을 때 ${\rho}$를 추정하고, 필요하면 ${\theta}$까지 계산한다.
- 모델링: 데이터를 이변수 가우시안에서 생성된 샘플로 가정하고, 2차 통계량으로 파라미터를 근사한다.
  $$
  \begin{aligned}
  \bar{x}&=\frac{1}{N}\sum_{i=1}^N x_i,\quad
  \bar{y}=\frac{1}{N}\sum_{i=1}^N y_i \\
  s_X^2&=\frac{1}{N-1}\sum_{i=1}^N (x_i-\bar{x})^2,\quad
  s_Y^2=\frac{1}{N-1}\sum_{i=1}^N (y_i-\bar{y})^2 \\
  s_{XY}&=\frac{1}{N-1}\sum_{i=1}^N (x_i-\bar{x})(y_i-\bar{y}) \\
  \hat{\rho}&=\frac{s_{XY}}{s_X s_Y}
  \end{aligned}
  $$
- 샘플 기반 추정량은 다음과 같이 정의한다.
- 결과 해석: ${\hat{\rho}}$는 샘플의 선형 관계를 정규화해 요약한 값이며, ${N}$이 충분히 크고 데이터가 가우시안에 가까울수록 ${\rho}$를 더 안정적으로 근사한다.
- 확장: ${\hat{\rho}}$, ${s_X}$, ${s_Y}$를 ${\theta}$ 공식에 대입하면 타원 주축 각도를 데이터로부터 역으로 계산할 수 있다.→ ${\theta}$는 데이터로부터 ${\rho}$를 추정하고 그 추정된 구조를 해석하는 도구이다.
- $$
  \begin{aligned}
  \hat{\theta}= \frac{1}{2}\tan^{-1}\left(\frac{2\hat{\rho},s_X s_Y}{s_X^2 - s_Y^2}\right)
  \end{aligned}
  $$

## 05_Bivariate Gaussian의 condiational pdf

### Conditional PDF 정의

연속 확률 변수에서 **Conditional Probability**는 확률 대신 밀도로 정의되며, **Conditional PDF**는 다음 비율로 정의된다.

$$
f_{X|Y}(x|y)=\frac{f_{XY}(x,y)}{f_Y(y)},\qquad f_Y(y)>0
$$

이 식은 ${y}$가 주어졌을 때 ${x}$ 방향으로 남아있는 density를 ${f_Y(y)}$로 정규화한 결과로 해석된다.

![](/assets/img/blog/prob-22-multivariate-gaussian-distribution/image-005.png)

### Conditionals are Gaussian

**Joint Gaussian**에서는 조건부도 가우시안이 된다.

$$
X|Y=y \sim \mathcal{N}\left(\mu_X+\rho\frac{\sigma_X}{\sigma_Y}(Y-\mu_Y),\ \sigma_X^2(1-\rho^2)\right)
$$

- conditional 평균은 $mu_x+\rho\frac{\sigma_x}{\sigma_y}(y-\mu_y)$로 이는 $y$에 대한 **linear function**이다.
- conditional 분산은 ${y}$에 의존하지 않는 상수이며 ${0\le 1-\rho^2\le 1}$이므로 원래 분산보다 크지 않다.

→ ${\lvert  \rho  \rvert}$가 클수록 관측 ${y}$가 ${x}$의 불확실성을 더 크게 줄이며, ${\lvert \rho \rvert\to 1}$이면 cnditional 분산이 0으로 수렴한다.

![](/assets/img/blog/prob-22-multivariate-gaussian-distribution/image-006.png)

### 증명

$$ \begin{aligned}f(x \mid y)&= \frac{f_{XY}(x, y)} {f_Y(y)} \\
&\Rightarrow\;
\frac{
\displaystyle
\frac{1}{2\pi \sigma_X \sigma_Y \sqrt{1-\rho^2}}
\exp\left[
-\frac{1}{2(1-\rho^2)}
\left(
\frac{(x-\mu_X)^2}{\sigma_X^2}
- \frac{2\rho (x-\mu_X)(y-\mu_Y)}{\sigma_X \sigma_Y}
+ \frac{(y-\mu_Y)^2}{\sigma_Y^2}
\right)
\right]
}{
\displaystyle
\frac{1}{\sqrt{2\pi}\,\sigma_Y}
\exp\left(
-\frac{(y-\mu_Y)^2}{2\sigma_Y^2}
\right)
}
\\
&\Rightarrow\;
\frac{1}{\sqrt{2\pi}\,\sigma_X \sqrt{1-\rho^2}}
\exp\left[
-\frac{1}{2(1-\rho^2)}
\left(
\frac{(x-\mu_X)^2}{\sigma_X^2}
- \frac{2\rho (x-\mu_X)(y-\mu_Y)}{\sigma_X \sigma_Y}
+ \rho^2 \frac{(y-\mu_Y)^2}{\sigma_Y^2}
\right)
\right] \\
&\Rightarrow\;
\frac{1}{\sqrt{2\pi}\,\sigma_X \sqrt{1-\rho^2}}
\exp\left[
-\frac{1}{2(1-\rho^2)}
\left(
\frac{x-\mu_X}{\sigma_X}
- \rho\,\frac{y-\mu_Y}{\sigma_Y}
\right)^2
\right]
\end{aligned}
$$

## 06_n차원 Multivariate Gaussian의 벡터-행렬 표현

### Random Vector와 Joint PDF

n차원 **Random Vector** ${\mathbf{x}\in\mathbb{R}^n}$에 대해 평균 벡터 ${\boldsymbol{\mu}}$와 공분산 행렬 ${\mathbf{\Sigma}}$를 사용하면 **Joint PDF**는 다음과 같다.

$$
f(\mathbf{x})=\frac{1}{(2\pi)^{n/2}|\mathbf{\Sigma}|^{1/2}}\exp\left(-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathsf{T}}\mathbf{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right)
$$

- ${\lvert \mathbf{\Sigma} \rvert}$는 분포의 전체 부피 스케일을 결정하는 정규화 항이다.

$$
\begin{aligned}\mathbf{\mathbf{\Sigma}}&=\begin{bmatrix}\sigma_{11} & \sigma_{12} & \cdots & \sigma_{1n} \\\vdots      & \vdots      & \ddots & \vdots      \\\sigma_{n1} & \sigma_{n2} & \cdots & \sigma_{nn}\end{bmatrix}, \quad \sigma_{ij}= \operatorname{Cov}(X_i, X_j)= \rho_{ij}\, \sigma_i \sigma_j\end{aligned}
$$

- ${(\mathbf{x}-\boldsymbol{\mu})^{\mathsf{T}}\mathbf{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})}$는 **Mahalanobis distance**의 제곱이며, 평균으로부터의 통계적 거리를 나타낸다.

### 공분산 행렬의 의미

- 대각 성분 ${\Sigma_{ii}}$는 각 성분의 **Variance**이다.
- 비대각 성분 ${\Sigma_{ij}}$는 성분 간 **Covariance**이며 선형적 결합 구조를 인코딩한다.
- ${\mathbf{\Sigma}}$의 고유벡터는 등밀도 타원의 방향을, 고유값은 각 방향의 퍼짐을 결정한다.

### Marginalization과 Conditional의 일반 공식

벡터를 두 블록으로 분할하여 ${\mathbf{x}=\begin{bmatrix}\mathbf{x}a\ \mathbf{x}b\end{bmatrix}}$*, ${\boldsymbol{\mu}=\begin{bmatrix}\boldsymbol{\mu}a\ \boldsymbol{\mu}b\end{bmatrix}}$, ${\mathbf{\Sigma}=\begin{bmatrix}\mathbf{\Sigma}{aa}&\mathbf{\Sigma}{ab}\ \mathbf{\Sigma}{ba}&\mathbf{\Sigma}{bb}\end{bmatrix}}$*로 둔다.

- **Marginal PDF**는 가우시안이다.

$$
\mathbf{x}a \sim \mathcal{N}(\boldsymbol{\mu}a,\mathbf{\Sigma}{aa}),\qquad \mathbf{x}b \sim \mathcal{N}(\boldsymbol{\mu}b,\mathbf{\Sigma}{bb})
$$

- **Conditional Probability**도 가우시안이며 평균과 공분산은 다음과 같이 정리된다.

$$
\mathbf{x}a|\mathbf{x}b=\mathbf{b}\sim \mathcal{N}\left(\boldsymbol{\mu}a+\mathbf{\Sigma}{ab}\mathbf{\Sigma}{bb}^{-1}(\mathbf{b}-\boldsymbol{\mu}b),\ \mathbf{\Sigma}{aa}-\mathbf{\Sigma}{ab}\mathbf{\Sigma}{bb}^{-1}\mathbf{\Sigma}{ba}\right)
$$

여기서 ${\mathbf{\Sigma}{ab}\mathbf{\Sigma}{bb}^{-1}(\mathbf{b}-\boldsymbol{\mu}b)}$*는 관측 ${\mathbf{b}}$가 평균을 얼마나 이동시키는지 나타내는 선형 보정항 이며, ${\mathbf{\Sigma}{aa}-\mathbf{\Sigma}{ab}\mathbf{\Sigma}{bb}^{-1}\mathbf{\Sigma}_{ba}}$*는 관측으로 인해 줄어든 불확실성을 나타내는 조건부 공분산이다.

→ **Marginalization**은 적분으로 변수를 제거하고, **Conditional Probability**는 관측된 블록을 기준으로 남은 블록의 평균과 분산을 재배치한다.

## 07_정리

- **Marginals are Gaussian**는 다변수 가우시안에서 일부 변수만 남겨도 동일한 형태의 가우시안이 유지된다.
- **Conditionals are Gaussian**는 관측 정보가 들어왔을 때 남은 변수의 불확실성이 이차 선형 구조로 업데이트된다.
- **Uncorrelated implies Independent**는 **Joint Gaussian**이라는 가정 아래에서 공분산이 0이면 Independent하기에 Joint구조가 완전히 분리된곱으로 바뀔수 있다.

[https://www.youtube.com/watch?v=](https://www.youtube.com/watch?v=)[cCZ9GH8ekrI](https://www.youtube.com/watch?v=cCZ9GH8ekrI)
