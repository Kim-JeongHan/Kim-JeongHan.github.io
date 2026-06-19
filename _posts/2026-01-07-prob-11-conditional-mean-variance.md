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
---

Conditional Mean and Variance를 구하는 방식은 discrete와 coutinous에 따라 방식이 나누어진다.<br>discrete한 경우에 Conditional Mean and variance를 구하는 것은 쉽게 나타난다.<br>countinous한 경우에는 $f(x|A)$를 구하는 것의 어려움이 존재한다.<br>이때, CDF와 PDF를 사용해 $f(x|A)$를 표현할수 있다.

---
# 01) **Conditional Mean and Variance**
## 01_Conditional Mean
---
### ☾ 조건부 평균 E\[X\|A\]
- 표본 공간의 조건에 대한 확률변수의 평균
- 조건 A : 확률 변수 X의 축소 또는 제한된 범위를 나타내는 집합
### ☾ 예시
- Tossing a dice : \{1,2,3,4,5,6\}, $P(X=k)$=1/6, k=1,2,3,4,5,6
- $E[X]$=(1+2+3+4+5+6)/6=3.5
- $A=$\{$X>3$\}, $E[X|A]$=\{4,5,6의 평균\} = (4+5+6)/3=5
### ☾ We have to find the conditional probability (discrete RV) or conditional density (continous RV) for $E[X|A]$.
## 02_Conditional Mean & Variance
---
### ☾ A : Condition of X
- Mean
$$
discrete\ RV: E[X|A]= \sum_{x_k\in A}x_kP(x_k|A)\rightarrow P(x_k|A)=\frac{P(x_k \cap A)}{P(A)}=\frac{P(x_k)}{P(A)}
$$

헷갈리면 주사위를 생각해보자. $P(x_k|A)$를 구할때!

$$
countinous\ RV : E[X|A]= \int_{x\in A}xf(x|A)dx \rightarrow f(x|A)=\frac{f(x\cap A)}{f(A)}??
$$
- Variance
$Var[X|A]=E[X^2|A]-E[X|A]^2$
→conditional density function should be found w.r.t the condition A.
## 03_Conditional Density and Mean
---
### ☾ For a countinous RV X, $A=$ \{$X\le a$\}

우리가 구하고 싶은 것 :  $E[X|A]= \int_{x\in A}xf(x|A)dx$
- 조건부 PDF를 구하기 위해서 조건부 CDF를 정의한뒤 미분한다.

![](/assets/img/blog/prob-11-conditional-mean-variance/image-001.png)

$$
f(x|A)=\frac{dF(x|A)}{dx}=\frac{d}{dx}P(X\le x|X\le a)=\frac{d}{dx}\frac{P(X\le x\cap X\le a)}{P(X\le a)}=\begin{cases}
  1) \frac{d}{dx}\frac{P(X\le x)}{F(a)}=\frac{f(x)}{F(a)},\ \ for \ x\le a \\
 2) \frac{d}{dx}\frac{P(X\le a)}{P(X\le a)}=0, \ \ \ \ \ \ for\ x>a
\end{cases}
$$
$$
conclusion :E[X|A]= \int_{x\in A}xf(x|A)dx= \int_{x\le a}x\frac{f(x)}{F(a)}dx=\int_{x\le a}x\frac{f(x)}{P(A)}dx
$$
### ☾ Example 1 : $A=$ \{$X \le1$\}
- grpah
![](/assets/img/blog/prob-11-conditional-mean-variance/image-002.png)
- $a=1$
- $E[X|A]= \int_{x\in A}xf(x|A)dx= \int_{x\le a}x\frac{f(x)}{F(a)}dx=\int_{x\le a}x\frac{f(x)}{P(A)}dx$
- $F(1)=\frac{1}{2}$, $f(x)=x(x\le1)$ → $E[X|A]=\int^1_02x^2dx= \frac{2}{3}$
- $Var[X|A]=E[X^2|A]-X[X|A]^2=\int^1_02x^3dx-\left(\frac{2}{3}\right)^2=\frac{1}{18}$
### ☾ Example 2 : $A=$ \{$a < X \le b$\}
- graph
![](/assets/img/blog/prob-11-conditional-mean-variance/image-003.png)
- $E[X|A]= \int_{x\in A}xf(x|A)dx= \int_{x\le a}x\frac{f(x)}{F(a)}dx=\int_{x\le a}x\frac{f(x)}{P(A)}dx$
- $f(x|A)=\frac{dF(x|A)}{dx}=\frac{d}{dx}P(X\le x | a<X\le b) = \frac{d}{dx}\frac{P(X\le x \ \cap\  a<X\le b)}{P(a<X\le b)}$
![](/assets/img/blog/prob-11-conditional-mean-variance/image-004.png)
1) $=\frac{d}{dx}\frac{P(a<X\le b)}{P(a<X\le b)}=0,\ \ \ x>b$
2) $=\frac{d}{dx}\frac{P(a<X\le x)}{P(a<X\le b)} = \frac{d}{dx}\frac{F(x)-F(a)}{P(a<X\le b)}=\frac{f(x)}{P(a<X\le b)}, \ \ \ \ a<x\le b$
3) $=\frac{d}{dx}\frac{P(\varnothing)}{P(a<X\le b)}=0,\ \ \ x>b$
$conclusion:f(x|A)=\frac{f(x)}{P(A)}$
