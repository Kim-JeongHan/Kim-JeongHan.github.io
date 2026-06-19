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
---

---
# 01) **Continuous RVs**
## 01_**Exponential distribution**
---

### 정의
Exponential distribution은 **0 이상인 연속 확률 변수**를 다루는 분포이다.
- $X=\{x|x\ge 0\}$, $pdf: f(x)=\lambda e^{-\lambda x},\lambda>0$
- parameter : $\lambda>0$
- $mean=\frac{1}{\lambda},\ \ variaance=\frac{1}{\lambda^2}$

Geometric random variable의 연속형 버전으로 볼수 있으며, 평균이  $\frac{1}{p}$인 점에서 매우 유사하다.

**주 사용처**
- 시스템의 수명(lifetime)
- 이벤트 간 시간 간격(time interval)

![](/assets/img/blog/prob-13-continuous-rvs-exponential-erlang/image-001.png)

### **예시 1 : Lifetime (Survival Analysis)**
Exponential distribution은 **시스템이 고장 나기까지 걸리는 시간**을 모델링할 때 자주 사용된다.
예를 들어 방사성 동위원소의 붕괴 시간이나 장비의 고장 시간 등이 이에 해당한다.

- $cdf :P(x\le t)=\int^t_0\lambda e^{-\lambda x}=1-e^{-\lambda t}$
이는 **시간 **$t$**까지 시스템이 고장 날 확률**을 의미한다.
반대로,
- $P(X > t) = e^{-\lambda t}$
는 **시간 **$t$**까지 정상 동작할 확률**이다.

![](/assets/img/blog/prob-13-continuous-rvs-exponential-erlang/image-002.png)

### 예시2 : Memoryless property of Exponential distribution
Exponential distribution의 가장 중요한 성질은 **memoryless property**이다.
조건은 다음과 같다.
- 이미 $t$ 시간 동안 생존했을 때
- 앞으로 추가로 $T$ 시간 이상 더 생존할 확률
이를 수식으로 계산하면,
$$
\begin{aligned}P(X > t + T \mid X > t)&= \frac{P(X > t + T \cap X > t)}{P(X > t)} \\&= \frac{P(X > t + T)}{P(X > t)}= \frac{1 - F(t + T)}{1 - F(t)} \\&= \frac{1 - (1 - e^{-\lambda (t+T)})}{1 - (1 - e^{-\lambda t})} = \frac{e^{-\lambda (t+T)}}{e^{-\lambda t}} = e^{-\lambda T} \\&= 1 - F(T) = P(X > T)\end{aligned}
$$
최종 결과에서 **ttt가 완전히 사라진다**는 점이 핵심이다.
즉,
- 과거에 얼마나 오래 생존했는지는 중요하지 않다
- 현재 시점부터의 미래 생존 확률은 항상 동일하다
이 때문에 Exponential distribution은 **기억을 갖지 않는(memoryless) 분포**라고 불린다.

참고사항 : $\begin{aligned}
\text{cdf: }\quad
P(X \le t)
&= F(t) \\
&= \int_{0}^{t} \lambda e^{-\lambda x}\, dx \\
&= 1 - e^{-\lambda t}
\end{aligned}$

### 예시3 : Exponential Distribution과 Poisson Distribution의 관계
Poisson 분포와 Exponential 분포는 **서로 깊게 연결**되어 있다.<br>먼저 Poisson 분포를 가정한다.
- 단위 시간당 평균 발생 횟수: $\lambda$
- 시간 구간 $t$ 동안의 평균 발생 횟수: $\lambda t$
이때,
$$
\begin{aligned}P(X = k)&= \frac{(\lambda t)^k e^{-\lambda t}}{k!},\quad \text{for a time interval } t\end{aligned}
$$
이제 **시간 **$t$** 동안 이벤트가 최소 한 번 발생할 확률**을 보면,
$$
\begin{aligned}P(X \ge 1)&= 1 - P(0) \&= 1 - e^{-\lambda t}\end{aligned}
$$
이 결과는 Exponential distribution의 CDF와 정확히 동일하다.
$$
\int_{0}^{t} \lambda e^{-\lambda x} dx= 1 - e^{-\lambda t}
$$
### 핵심 정리
- **Poisson distribution**<br>→ 일정 시간 $t$ 동안 **이벤트가 몇 번 발생했는가**
- **Exponential distribution**<br>→ **이벤트와 이벤트 사이의 시간 간격**은 얼마나 되는가
즉,
- 이벤트 개수를 확률 변수로 보면 Poisson
- 이벤트 사이의 시간 간격을 확률 변수로 보면 Exponential
![](/assets/img/blog/prob-13-continuous-rvs-exponential-erlang/image-003.png)
랜덤하게 발생하는 이벤트의 **시간 간격을 분포로 표현할 때**, Exponential distribution이 가장 자연스럽고 적합한 모델이다.

# 02) Erlang-K Distribution
Erlang–K distribution은 **연속적으로 발생하는 이벤트들 사이의 시간 간격을 누적해서 본 분포**이다.
- $X_k$ : $k$개의 연속된 이벤트가 발생할 때까지 걸리는 전체 시간
- 각 시간 간격 $T_i$는 서로 **독립(independent)** 이고 **동일한 분포(iid)** 를 따르며 모두 **Exponential distribution**을 따른다
즉
$$
\begin{aligned}
X &= T_1 + T_2 + \cdots + T_k, \quad
(T_i : \text{Exponential distribution})
\end{aligned}

$$
![](/assets/img/blog/prob-13-continuous-rvs-exponential-erlang/image-004.png)
### Exponential distribution과의 관계
- Erlang–K distribution은 **Exponential distribution의 일반화된 형태**이다
- 특히, Elgng-K의 k가 1인 특수한 케이스라고 볼수 있다.
- pdf of erlang-k : $\begin{aligned}
X &= T_1 + T_2 + \cdots + T_k, \quad
(T_i : \text{Exponential distribution})
\end{aligned}$<br>→ (k-1) times convolution of pdf of identical expoentail distributiion과 같다
**수학적 정의 (PDF)**
Erlang–K 분포의 확률 밀도 함수는 다음과 같다.
$$
f_{X_k}(x)
= \frac{\lambda^{k} x^{k-1} e^{-\lambda x}}{(k-1)!},
\quad x \ge 0
$$
이 결과는 다음과 같은 해석을 가진다.
- $k$개의 동일한 Exponential 분포를 **합(convolution)** 한 결과
- 즉,**Exponential PDF를 (k−1)번 convolution 한 것과 동일하다.**
<table header-row="true" header-column="true">
<colgroup>
<col width="236.328125">
<col width="296.3333333333333">
<col width="296.3333333333333">
</colgroup>
<tr>
<td></td>
<td>exponential</td>
<td>erlang-k</td>
</tr>
<tr>
<td>pdf</td>
<td>$\lambda e^{-\lambda x}$</td>
<td>$\frac{\lambda^{k} x^{k-1} e^{-\lambda x}}{(k-1)!}$</td>
</tr>
<tr>
<td>mean, var</td>
<td>maen= $\frac{1}{\lambda}$, var=$\frac{1}{\lambda^2}$</td>
<td>maen= $\frac{k}{\lambda}$, var=$\frac{k}{\lambda^2}$</td>
</tr>
</table>
### Erlang-k의 직관적 이해
- $k$가 커질수록 분포는 점점 **대칭적**이 되고, 분산 대비 평균이 커지며 **Gaussian distribution에 수렴**한다
이는 **중심극한정리(CLT)**의 직접적인 결과이다.
> 여러 개의 독립적인 동일 분포 확률 변수를 더하면 그 합은 점점 정규분포에 가까워진다
![](/assets/img/blog/prob-13-continuous-rvs-exponential-erlang/image-005.png)
