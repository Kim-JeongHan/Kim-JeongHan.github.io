---
layout: post
title: Reinforcement Learning 2 - Value Function과 Dynamic Programming
date: 2026-08-25 00:01:00 +0900
slug: deep-reinforcement-learning-summary-2
render_with_liquid: true
use_math: true
categories:
- 공부
- 강화학습
tags:
- reinforcement-learning
---

## 00_Value Function

Policy $\pi$가 정해져 있을 때, 현재 state $s$에서 시작하여 policy $\pi$를 계속 따랐을 때 얻을 수 있는 return의 expectation을 value function이라고 한다. 즉, value function은 현재 state가 얼마나 좋은지를 평가하는 함수이다. state-value function과 action-value function 두 가지가 있다.

### State-value function

State-value function은 state만 고정한 상황에서 이후에 얻을 수 있는 return들의 expectation이다.

$$
V^\pi(s) = \mathbb{E}_\pi[G_t \mid S_t=s]
$$

여기서 $G_t$는 time step $t$ 이후에 얻는 discounted return이다. $V^\pi(s)$가 크다는 것은 state $s$에서 policy $\pi$를 따랐을 때 앞으로 높은 return을 얻을 가능성이 크다는 뜻이다.

![Value function backup diagram](/assets/img/blog/deep-reinforcement-learning-summary-2/backup-diagram-value-functions.png)

#### Backup diagram

Backup diagram은 value function을 계산할 때 현재 state의 value가 이후에 발생할 수 있는 action, reward, next state의 value를 이용해 계산된다는 관계를 보여준다.

1. 현재 state $s$에서 policy $\pi$에 따라 action $a$를 선택한다.
2. action $a$를 수행하면 transition probability에 따라 reward $r$과 next state $s'$가 발생한다.
3. next state에서도 policy $\pi$에 따라 다음 action을 선택하고 trajectory를 이어간다.
4. 가능한 모든 trajectory의 return을 평균내면 현재 state의 value가 된다.

이를 Bellman expectation equation으로 나타내면 다음과 같다.

$$
V^\pi(s)
= \sum_a \pi(a \mid s)
  \sum_{s',r} p(s',r \mid s,a)
  \left[r + \gamma V^\pi(s')\right]
$$

### Action-value function

Action-value function은 state와 첫 action까지 고정한 상황에서 이후에 얻을 수 있는 return들의 expectation이다.

$$
Q^\pi(s,a)
= \mathbb{E}_\pi[G_t \mid S_t=s,A_t=a]
$$

State-value function과 달리 첫 action $a$까지 정해져 있다. 첫 action을 수행한 이후에는 policy $\pi$에 따라 action을 선택한다.

두 함수의 차이는 다음과 같다.

- $V^\pi(s)$: state $s$에서 policy $\pi$가 선택할 수 있는 여러 action을 고려한 평균적인 value
- $Q^\pi(s,a)$: state $s$에서 특정 action $a$를 수행했을 때의 value

Policy가 stochastic하면 같은 state에서 여러 action이 확률적으로 선택될 수 있기 때문에 state value는 action value들의 weighted sum으로 표현된다.

$$
V^\pi(s) = \sum_a \pi(a \mid s) Q^\pi(s,a)
$$

만약 policy가 deterministic하여 $a=\pi(s)$를 항상 선택한다면 다음과 같이 단순해진다.

$$
V^\pi(s) = Q^\pi(s,\pi(s))
$$

#### Action-value function을 사용하는 이유

Action-value function을 알고 있으면 각 state에서 어떤 action이 더 좋은지 직접 비교할 수 있다.

$$
\pi_*(s) \in \arg\max_a Q_*(s,a)
$$

따라서 policy를 정하기에는 $Q$ function이 편리하다. 반면 모든 state-action pair에 대한 값을 저장하고 계산해야 하므로 state-value function보다 계산량과 메모리 사용량이 커질 수 있다.

기초적인 dynamic programming에서는 policy를 평가할 때 state-value function $V$를 중심으로 설명하는 경우가 많다. 다만 dynamic programming이 반드시 $Q$ function을 사용할 수 없다는 뜻은 아니며, 문제의 표현과 구현에 따라 $Q$ function을 사용할 수도 있다. Model-free reinforcement learning에서는 environment에서 얻은 random sample을 이용하여 $Q$ function을 직접 추정하는 방법도 많이 사용한다.

### Advantage function

Advantage function은 특정 action $a$가 해당 state에서 policy가 평균적으로 선택하는 action보다 얼마나 좋은지 또는 나쁜지를 나타낸다.

$$
A_\pi(s,a) = Q^\pi(s,a) - V^\pi(s)
$$

- $A_\pi(s,a)>0$: action $a$가 해당 state에서 평균적인 action보다 좋다.
- $A_\pi(s,a)<0$: action $a$가 평균적인 action보다 나쁘다.
- $A_\pi(s,a)=0$: action $a$가 평균적인 action과 같은 value를 가진다.

따라서 advantage function은 absolute value인 $Q^\pi(s,a)$보다 action의 상대적인 좋고 나쁨을 알려준다.

$$
Q^\pi(s,a) = V^\pi(s) + A_\pi(s,a)
$$

Policy에 따른 action의 평균 advantage는 0이 된다.

$$
\sum_a \pi(a \mid s) A_\pi(s,a) = 0
$$

## 01_RL 수학 기초

### Law of total probability

서로 겹치지 않고 전체 sample space를 이루는 사건들의 집합 $\{B_n\}$이 있을 때, 사건 $A$가 발생할 확률은 각 경우에서 $A$가 발생할 조건부 확률을 이용해 계산할 수 있다.

$$
P(A) = \sum_n P(A \mid B_n)P(B_n)
$$

이를 여러 가능한 상태나 사건으로 나누어 전체 확률을 계산한다고 생각할 수 있다. 강화학습에서는 next state나 reward가 여러 가지로 나뉘는 stochastic environment의 확률을 합칠 때 이와 같은 marginalization을 사용한다.

### Law of total expectation

확률변수 $Y$가 가질 수 있는 값에 대해 조건부 expectation을 평균내면 원래 random variable의 expectation을 얻을 수 있다.

$$
\mathbb{E}[X]
= \sum_y \mathbb{E}[X \mid Y=y]P(Y=y)
$$

어떤 조건 $Z=z$가 주어진 상황에서도 같은 방식으로 정리할 수 있다.

$$
\mathbb{E}[X \mid Z=z]
= \sum_y \mathbb{E}[X \mid Y=y,Z=z]P(Y=y \mid Z=z)
$$

이산 random variable의 expectation은 가능한 값과 그 값이 나올 확률을 곱해 모두 더한 값이다.

$$
\mathbb{E}[X] = \sum_x xP(X=x)
$$

조건부 expectation도 조건부 확률을 이용해 같은 방식으로 계산한다.

$$
\mathbb{E}[X \mid Z=z]
= \sum_x xP(X=x \mid Z=z)
$$

### Law of large numbers

많은 독립적인 시행을 반복하면 그 결과의 평균은 expected value에 가까워지고, 시행 횟수가 증가할수록 점점 더 가까워진다.

$X_1,\ldots,X_n$이 서로 independent하고 동일한 분포를 따르는 i.i.d. random samples라면 sample mean은 다음과 같이 정의된다.

$$
\overline{X}_n = \frac{1}{n}\sum_{i=1}^{n}X_i
$$

Law of large numbers에 의해 다음 관계가 성립한다.

$$
\overline{X}_n \xrightarrow[n\to\infty]{} \mathbb{E}[X]
$$

즉, random sample을 많이 모으면 sample mean으로 실제 expectation을 근사할 수 있다. 강화학습에서는 같은 policy로 여러 episode를 실행하고 얻은 return을 평균내어 value function이나 expected return을 추정할 때 이 성질을 이용한다.

## 02_Bellman Equation

Bellman equation은 현재 state의 value를 즉시 받는 reward와 다음 state의 value로 나누어 표현하는 식이다. Value function의 정의에서 출발하여 law of total probability와 law of total expectation을 적용하면 유도할 수 있다.

핵심은 episode가 끝날 때까지 모든 reward를 더해야 알 수 있는 return $G_t$를 직접 사용하지 않고, 한 단계 뒤에 받는 reward와 다음 state의 value로 표현하는 것이다.

$$
G_t = R_{t+1} + \gamma G_{t+1}
$$

이를 expectation 관점에서 정리하면 다음과 같다.

$$
v_\pi(s)
= \mathbb{E}_\pi
\left[R_{t+1}+\gamma v_\pi(S_{t+1}) \mid S_t=s\right]
$$

즉, Bellman expectation equation은 return을 완전히 새롭게 정의하는 것이 아니라, Markov property와 expectation을 이용해 같은 value를 **one-step reward + discounted next value**의 형태로 바꾸어 표현한 것이다. 이 표현 덕분에 episode가 끝날 때까지 기다리지 않고도 value를 재귀적으로 계산하거나 갱신할 수 있다.

### State-value function의 Bellman equation

먼저 state-value function의 정의는 다음과 같다. 강의의 $v_\pi(s)$는 앞에서 사용한 $V^\pi(s)$와 같은 의미이다.

$$
v_\pi(s) = \mathbb{E}_\pi[G_t \mid S_t=s]
$$

Policy $\pi$에 따라 첫 action $a$가 선택될 수 있으므로, 가능한 action에 대해 나누면 다음과 같다.

$$
\begin{aligned}
v_\pi(s)
&= \sum_a \mathbb{E}_\pi[G_t \mid S_t=s,A_t=a]
   P(A_t=a \mid S_t=s) \\
&= \sum_a \pi(a \mid s)q_\pi(s,a)
\end{aligned}
$$

Return의 재귀적 관계

$$
G_t = R_{t+1} + \gamma G_{t+1}
$$

를 적용하면 다음과 같다.

$$
v_\pi(s)
= \sum_a \pi(a \mid s)
  \mathbb{E}_\pi
  \left[R_{t+1}+\gamma G_{t+1}
  \mid S_t=s,A_t=a\right]
$$

다음 state $s'$와 reward $r$이 여러 가지로 발생할 수 있으므로, law of total expectation을 적용해 가능한 $s'$와 $r$에 대해 다시 나눈다.

$$
\begin{aligned}
v_\pi(s)
&= \sum_a \pi(a \mid s)\sum_{s',r}
   p(s',r \mid s,a) \\
&\quad\cdot
\mathbb{E}_\pi
\left[R_{t+1}+\gamma G_{t+1}
\mid S_t=s,A_t=a,S_{t+1}=s',R_{t+1}=r\right]
\end{aligned}
$$

MDP의 Markov property에 의해 현재의 $S_t,A_t$에 대한 과거 정보는 다음 state 이후의 return을 계산할 때 추가로 필요하지 않다. 또한 $R_{t+1}=r$, $S_{t+1}=s'$가 주어졌으므로 위 식은 다음처럼 정리된다.

$$
\begin{aligned}
v_\pi(s)
&= \sum_a \pi(a \mid s)\sum_{s',r}
   p(s',r \mid s,a)
   \left[r+\gamma v_\pi(s')\right]
\end{aligned}
$$

이 식이 **Bellman expectation equation for state-value function**이다. 앞에서 정의한 expected reward와 transition probability를 사용하면 다음과 같은 형태로도 쓸 수 있다.

$$
v_\pi(s)
= \sum_a \pi(a \mid s)
  \left[R_s^a + \gamma\sum_{s'}P^a_{ss'}v_\pi(s')\right]
$$

또는 한 단계의 reward와 다음 state value의 expectation으로 간단히 표현할 수 있다.

$$
v_\pi(s)
= \mathbb{E}_\pi
\left[R_{t+1}+\gamma v_\pi(S_{t+1}) \mid S_t=s\right]
$$

### Action-value function의 Bellman equation

State-value function의 관계를 확인했으므로, 이제 state $s$와 첫 action $a$까지 고정한 action-value function을 정리한다.

$$
q_\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t=s,A_t=a]
$$

첫 action 이후에는 next state $s'$에서 policy $\pi$에 따라 다음 action $a'$를 선택한다. 따라서 action-value function은 다음과 같이 전개된다.

$$
\begin{aligned}
q_\pi(s,a)
&= \sum_{s',r}p(s',r \mid s,a)
   \left[r+\gamma\sum_{a'}\pi(a' \mid s')q_\pi(s',a')\right]
\end{aligned}
$$

이는 다음과 같이 한 단계 reward와 next action-value의 expectation으로 표현할 수도 있다.

$$
q_\pi(s,a)
= \mathbb{E}_\pi
\left[R_{t+1}+\gamma q_\pi(S_{t+1},A_{t+1})
\mid S_t=s,A_t=a\right]
$$

### Diagram을 사용한 Bellman equation 유도

위 식은 그림의 왼쪽에서 오른쪽으로 단계적으로 유도할 수 있다. 먼저 state $s$의 value는 policy가 선택할 수 있는 action value의 weighted sum이다.

![Bellman equation의 value function 유도 흐름](/assets/img/blog/deep-reinforcement-learning-summary-2/bellman-equation-derivation.png)

$$
v_\pi(s) = \sum_a \pi(a \mid s)q_\pi(s,a)
$$

다음으로 state $s$에서 action $a$를 수행했을 때의 action value는, 현재 받는 expected reward와 next state의 state value로 나뉜다.

$$
q_\pi(s,a)
= R_s^a + \gamma\sum_{s'}P^a_{ss'}v_\pi(s')
$$

첫 번째 식에 두 번째 식을 대입하면 state-value function의 Bellman expectation equation을 얻는다.

$$
\begin{aligned}
v_\pi(s)
&= \sum_a \pi(a \mid s)q_\pi(s,a) \\
&= \sum_a \pi(a \mid s)
   \left[R_s^a + \gamma\sum_{s'}P^a_{ss'}v_\pi(s')\right]
\end{aligned}
$$

반대로 action-value function에서는 next state $s'$에 도착한 뒤 policy $\pi$에 따라 next action $a'$를 선택한다. 따라서 next state의 value를 다시 action value의 weighted sum으로 바꿀 수 있다.

$$
v_\pi(s') = \sum_{a'}\pi(a' \mid s')q_\pi(s',a')
$$

이를 action-value equation에 대입하면 다음 식을 얻는다.

$$
q_\pi(s,a)
= R_s^a
  + \gamma\sum_{s'}P^a_{ss'}
    \sum_{a'}\pi(a' \mid s')q_\pi(s',a')
$$

정리하면 다음과 같은 흐름이다.

$$
v_\pi(s)
\rightarrow q_\pi(s,a)
\rightarrow \left(R_s^a + \gamma\sum_{s'}P^a_{ss'}v_\pi(s')\right)
$$

State value는 policy에 따른 action 선택을 평균낸 값이고, action value는 transition probability와 expected reward를 거쳐 next state의 value로 연결된다. 이것이 그림에서 왼쪽의 value function이 오른쪽의 reward와 transition probability를 포함한 Bellman equation으로 확장되는 과정이다.

정리하면 Bellman equation은 한 시점의 value를 즉시 reward와 미래 value의 합으로 표현한다. 이 재귀적 구조를 이용하면 전체 episode가 끝날 때까지 기다리지 않고도 value를 계산하거나 갱신할 수 있다.

## 03_Optimal Value와 Bellman Optimality Equation

여러 policy의 value function을 비교했을 때, 각 state에서 가장 큰 value를 만들어내는 value function을 optimal value function이라고 한다.

### Optimal state-value function

Optimal state-value function은 가능한 모든 policy의 state-value function 중 최댓값이다.

$$
v_*(s) = \max_\pi v_\pi(s)
$$

즉, state $s$에서 시작했을 때 선택할 수 있는 policy 중 가장 높은 expected return을 얻도록 하는 policy의 value이다.

### Optimal action-value function

Optimal action-value function은 state $s$에서 action $a$를 먼저 수행한 뒤, 그 이후에 가장 좋은 policy를 따랐을 때의 action value이다.

$$
q_*(s,a) = \max_\pi q_\pi(s,a)
$$

Optimal action-value function을 알고 있다면 각 state에서 다음과 같이 optimal action을 선택할 수 있다.

$$
\pi_*(s) \in \arg\max_a q_*(s,a)
$$

따라서 optimal policy를 찾는 것은 각 state에서 $q_*(s,a)$를 최대로 만드는 action을 찾는 문제로 볼 수 있다. Deterministic optimal policy는 다음과 같이 표현된다.

$$
\pi_*(a \mid s) =
\begin{cases}
1, & a \in \arg\max_{a'}q_*(s,a') \\
0, & \text{otherwise}
\end{cases}
$$

최댓값을 갖는 action이 하나라면 그 action을 항상 선택한다. 최댓값을 갖는 action이 여러 개라면 그중 하나를 정해 deterministic하게 선택해도 optimal policy가 된다. 따라서 표준적인 유한 action MDP에서는 deterministic optimal policy가 항상 하나 이상 존재한다.

### Policy의 비교

두 policy를 모든 state에서 비교하여, policy $\pi'$가 policy $\pi$보다 항상 좋거나 같은 경우 다음과 같이 정의한다.

$$
\pi' \geq \pi
\quad\Longleftrightarrow\quad
v_{\pi'}(s) \geq v_\pi(s) \quad \text{for all } s \in S
$$

Policy의 우열은 특정 state 하나에서만 비교하는 것이 아니라, 모든 state에서 value가 같거나 큰지를 기준으로 판단한다. 또한 state마다 가장 좋은 action은 달라질 수 있으므로, optimal policy는 각 state에 맞는 action을 선택하는 하나의 policy 함수로 정의된다.

### Optimal policy에 대한 정리

표준적인 MDP에서는 다음과 같은 optimal policy가 존재한다.

- 모든 policy $\pi$보다 좋거나 같은 optimal policy $\pi_*$가 존재한다.
- 모든 optimal policy는 optimal state-value function을 달성한다.

$$
v_{\pi_*}(s) = v_*(s)
$$

- 모든 optimal policy는 optimal action-value function도 달성한다.

$$
q_{\pi_*}(s,a) = q_*(s,a)
$$

동일한 최댓값을 갖는 action이 여러 개라면 optimal policy가 하나만 존재할 필요는 없다. 서로 다른 action을 선택하더라도 모든 state에서 동일한 optimal value를 만들면 모두 optimal policy가 될 수 있다.

### Bellman optimality equation

Bellman expectation equation은 policy $\pi$가 정해졌을 때 policy가 선택하는 action들의 value를 확률적으로 평균내는 식이었다. Optimal value function에서는 여러 policy 중 가장 좋은 action을 선택하므로, action에 대한 weighted sum 대신 $\max$를 사용한다.

먼저 optimal state-value function과 optimal action-value function의 관계는 다음과 같다.

$$
v_*(s) = \max_a q_*(s,a)
$$

Optimal action-value function은 현재 action을 고정하고, transition 이후에는 optimal policy를 따랐을 때의 value이다.

$$
q_*(s,a)
= R_s^a + \gamma\sum_{s'}P^a_{ss'}v_*(s')
$$

따라서 state-value function은 다음과 같이 표현된다.

$$
v_*(s)
= \max_a\left[R_s^a + \gamma\sum_{s'}P^a_{ss'}v_*(s')\right]
$$

Reward와 next state를 함께 표현하는 joint probability를 사용하면 다음과 같은 Bellman optimality equation이 된다.

$$
v_*(s)
= \max_a\sum_{s',r}p(s',r \mid s,a)
\left[r+\gamma v_*(s')\right]
$$

Action-value function의 Bellman optimality equation은 다음과 같다.

$$
q_*(s,a)
= \sum_{s',r}p(s',r \mid s,a)
\left[r+\gamma\max_{a'}q_*(s',a')\right]
$$

![Bellman optimality equation의 backup diagram](/assets/img/blog/deep-reinforcement-learning-summary-2/bellman-optimality-backup-diagram.png)

Bellman expectation equation과 비교하면 다음과 같은 차이가 있다.

- policy $\pi$에 따른 action 확률의 weighted sum 대신 $\max_a$를 사용한다.
- policy에 대한 value인 $v_\pi, q_\pi$ 대신 optimal value인 $v_*, q_*$를 사용한다.
- 평균적인 policy의 성능이 아니라 가능한 action 중 가장 높은 value를 주는 action을 선택한다.

#### Model이 필요한 이유

Bellman optimality equation을 표에 있는 모든 state와 action에 대해 정확하게 계산하려면 transition probability $P$와 reward function $R$을 알아야 한다. 예를 들어 다음 계산에는 $P^a_{ss'}$가 필요하다.

$$
q_*(s,a) = R_s^a + \gamma\sum_{s'}P^a_{ss'}v_*(s')
$$

따라서 이 식을 직접 계산하는 dynamic programming은 model-based 방법이다. 다만 optimal value function이나 optimal policy가 model-based 방법에서만 존재한다는 뜻은 아니다. Model-free reinforcement learning은 $P$와 $R$을 명시적으로 알지 못해도 environment에서 얻은 sample $(s,a,r,s')$을 사용해 $v_*$나  $q_*$를 추정한다.

## 04_Dynamic Programming

Dynamic Programming(DP)은 복잡한 문제를 여러 개의 작은 sub-problem으로 나누어 해결하는 방법이다. 작은 문제의 해를 저장하고 재사용하여 같은 계산을 반복하지 않는 것이 핵심이다.

![Elements of Dynamic Programming](/assets/img/blog/deep-reinforcement-learning-summary-2/dynamic-programming-elements.png)

DP의 주요 요소는 다음과 같다.

- **Substructure**: complex problem을 여러 sub-problem으로 분해한다.
- **Table structure**: sub-problem의 정답을 table에 저장하고 필요할 때 재사용한다.
- **Bottom-up computation**: 작은 sub-problem의 정답을 결합하여 더 큰 sub-problem을 순서대로 해결한다.

DP가 효과적으로 적용되려면 보통 다음 두 성질이 필요하다.

- **Optimal substructure**: 전체 문제의 optimal solution이 sub-problem의 optimal solution들로 구성된다.
- **Overlapping sub-problems**: 동일한 sub-problem이 여러 번 반복해서 등장하므로, 한 번 계산한 정답을 재사용할 수 있다.

MDP는 Bellman equation을 통해 현재 state의 문제를 next state의 더 작은 문제로 재귀적으로 분해할 수 있다. 또한 동일한 state의 value가 여러 계산 경로에서 반복해서 필요하므로 table에 저장해 재사용할 수 있다.

### Sequential decision problem의 해결 방법

Sequential decision problem은 environment model을 알고 있는지 여부에 따라 대표적으로 model-based와 model-free 방법으로 나눌 수 있다.

![Agent와 Environment의 상호작용](/assets/img/blog/deep-reinforcement-learning-summary-2/agent-environment-loop.png)

| 방법 | Environment model | 계산 방식 | 대표적인 접근 |
| --- | --- | --- | --- |
| Model-based | transition probability와 reward function을 알고 있음 | model을 사용해 미래를 예측하고 planning | Dynamic Programming |
| Model-free | transition probability와 reward function을 모름 | environment sample에서 직접 value나 policy를 학습 | Monte Carlo, TD learning, Q-learning |

Model-based DP의 주요 한계는 다음과 같다.

1. **계산 복잡도**: 모든 state-action-next state 조합을 계산해야 한다.
2. **차원의 저주**: state와 action의 차원 또는 개수가 커지면 table 크기와 계산량이 급격히 증가한다.
3. **완전한 model 필요**: transition probability $P$와 reward function $R$을 미리 알고 있어야 한다.

Model-free RL은 model을 명시적으로 만들지 않는 대신 실제 environment와 상호작용하며 sample을 얻는다. 따라서 model을 알 수 없는 문제에 적용할 수 있지만, sample의 수가 충분히 필요하고 stochasticity 때문에 추정값의 분산이 생길 수 있다.

### Dynamic Programming과 Reinforcement Learning의 비교

DP와 RL은 모두 Bellman optimality equation을 바탕으로 optimal policy를 찾는 방법으로 볼 수 있다. 이를 적용하려면 state가 Markov property를 만족해야 하며, MDP를 state, action, reward, transition으로 표현할 수 있어야 한다.

#### Dynamic Programming

- **Model-based**: transition probability $P$와 reward function $R$을 알고 있어야 한다.
- **Full backup**: 가능한 모든 next state와 reward의 확률을 사용하여 expectation을 계산한다.
- **전체 table update**: 한 iteration에서 모든 state의 value를 update하는 방식으로 계산한다.
- **적용 범위**: state와 action의 수가 중간 정도인 tabular 문제에서 효율적이다.
- **Value table 사용**: $Q(s,a)$를 직접 저장하면 state-action pair마다 값을 저장해야 하므로, 메모리를 줄이기 위해 보통 $V(s)$를 사용한다.

$$
|\mathcal{S}| \ll |\mathcal{S}|\,|\mathcal{A}|
$$

다만 state와 action의 크기가 커지면 table의 크기와 full backup 계산량이 급격히 증가한다. 이를 차원의 저주라고 하며, 큰 문제에서는 DP를 직접 적용하기 어렵다.

#### Reinforcement Learning

- **Model-free**: transition probability와 reward function을 미리 알 필요가 없다.
- **Sample backup**: 모든 가능한 transition을 계산하는 대신 실제 environment에서 얻은 sample $(s,a,r,s')$을 사용한다.
- **근사 update**: 한 번의 sample로 value를 update하므로, 전체 expectation을 정확하게 계산하는 것이 아니라 Bellman equation의 해를 sample을 통해 근사한다.
- **큰 문제에 대한 적용**: neural network나 function approximation을 사용하면 거대한 table을 직접 저장하지 않고 value 또는 policy를 근사할 수 있다.

Sample backup의 예로 TD-style update를 들면 다음과 같다.

$$
V(s) \leftarrow V(s)
+ \alpha\left[r+\gamma V(s')-V(s)\right]
$$

DP가 model의 모든 가능한 결과를 사용하는 full backup이라면, RL은 실제로 관측된 일부 결과를 사용하는 sample backup이다. 따라서 RL은 model을 알 수 없는 문제와 큰 상태 공간에 더 유연하지만, sample noise와 function approximation 오차가 생길 수 있다. 차원의 저주를 완전히 없애는 것은 아니며, sample-based learning과 function approximation으로 그 영향을 완화하는 방식이다.

#### Backup 방식의 비교

DP와 model-free RL은 value를 update할 때 서로 다른 종류의 backup을 사용한다.

![Dynamic Programming, Monte Carlo, Temporal Difference backup 비교](/assets/img/blog/deep-reinforcement-learning-summary-2/backup-methods-comparison.png)

그림에서 위쪽 DP는 현재 state에서 가능한 모든 branch를 펼쳐 expectation을 계산하는 **full backup**이다. 가운데 Monte Carlo는 실제로 선택된 하나의 trajectory를 episode 끝까지 따라간 뒤 전체 return을 이용하는 **sample multi-step backup**이다. 아래쪽 TD는 실제 trajectory에서 한 step만 관측하고, 다음 state의 value estimate를 이용하는 **sample one-step backup**이다.

##### Dynamic Programming: full backup

DP는 model을 알고 있으므로 가능한 모든 next state와 reward를 고려하여 expectation을 계산한다.

$$
V(S_t) \leftarrow
\mathbb{E}_\pi\left[R_{t+1}+\gamma V(S_{t+1})\right]
$$

즉, 하나의 sample만 사용하는 것이 아니라 transition probability가 알려주는 모든 branch를 한 번에 backup한다.

##### Monte Carlo와 Temporal Difference

- **Monte Carlo**: episode를 끝까지 실행해 얻은 실제 return을 사용하는 sample multi-step backup이다. Episode가 끝난 뒤 update할 수 있으며 bootstrapping을 사용하지 않는다.
- **Temporal Difference**: 한 step 뒤의 reward와 next state의 value estimate를 사용하는 sample one-step backup이다. Episode가 끝나기 전에도 update할 수 있으며 bootstrapping을 사용한다.

두 방법의 구체적인 update 식과 알고리즘은 이후 Monte Carlo와 Temporal Difference 단원에서 자세히 다룬다.

| 방법 | Model 필요 여부 | Backup | Episode 종료 필요 | Bootstrapping |
| --- | --- | --- | --- | --- |
| Dynamic Programming | 필요 | 모든 branch를 사용하는 full backup | 아니오 | 다음 value function 사용 |
| Monte Carlo | 불필요 | 실제 trajectory 전체를 사용하는 sample multi-step backup | 예 | 아니오 |
| Temporal Difference | 불필요 | 한 step sample을 사용하는 sample one-step backup | 아니오 | 예 |

따라서 DP는 정확한 model이 있을 때 expectation을 이용해 전체 branch를 계산하고, Monte Carlo와 TD는 sample data만으로 value를 추정한다. Monte Carlo는 실제 episode return을 사용하고, TD는 아직 완전히 계산되지 않은 next-state value를 이용해 더 빠르게 update한다.

## 05_Value Iteration

Value Iteration은 Bellman optimality equation을 반복적인 update rule로 바꾸어 optimal state-value function을 구하는 방법이다.

$$
V_{k+1}(s)
\leftarrow \max_a\sum_{s',r}p(s',r \mid s,a)
\left[r+\gamma V_k(s')\right]
$$

여기서 $V_k$는 $k$번째 iteration에서의 value table이다. 반복을 계속하면 적절한 조건 아래에서 다음과 같이 optimal value function으로 수렴한다.

$$
V_k(s) \longrightarrow V_*(s)
$$

### Value Iteration의 절차

1. 모든 state에 대해 $V_0(s)$를 초기화한다. 보통 0으로 초기화하지만 임의의 값으로 초기화할 수도 있다. Terminal state의 value는 보통 0으로 둔다.
2. 현재 value table을 사용해 모든 state의 값을 반복적으로 update한다.
3. 값의 변화량이 충분히 작아지면 반복을 종료한다.
4. 수렴한 value table을 이용해 one-step lookahead로 policy를 추출한다.

수렴 여부는 다음과 같은 최대 변화량으로 확인할 수 있다.

$$
\Delta = \max_{s\in S}\left|V_{k+1}(s)-V_k(s)\right|
$$

$$
\Delta < \epsilon
$$

### Synchronous backup과 asynchronous backup

**Synchronous backup**은 모든 state에 대한 새로운 값 $V_{k+1}(s)$를 계산할 때 오직 이전 table $V_k$만 사용하는 방식이다. 모든 state의 update를 끝낸 뒤 새로운 table을 한 번에 교체한다.

$$
V_{k+1}(s)
= \max_a\sum_{s',r}p(s',r \mid s,a)
\left[r+\gamma V_k(s')\right]
\quad \text{for all }s\in S
$$
Policy evaluation에서는 최댓값 대신 고정된 policy를 사용한다.

$$
V_{k+1}(s)
= \sum_{s',r}p(s',r \mid s,\pi(s))
\left[r+\gamma V_k(s')\right]
$$

- update 순서에 영향을 받지 않는다.
- 여러 state의 계산을 병렬로 처리하기 쉽다.
- $V_k$와 $V_{k+1}$ 두 table이 필요할 수 있다.

**Asynchronous backup**은 state 하나 또는 일부 state를 계산한 직후 같은 table에 바로 반영하는 방식이다. 이후 state를 update할 때 이미 갱신된 최신 값을 사용할 수 있다.

- 별도의 새 table 없이 in-place update가 가능하다.
- 중요한 state를 먼저 update하는 등 유연한 순서를 사용할 수 있다.
- update 순서에 따라 중간 과정이 달라진다.
- discounted finite MDP에서 모든 state가 충분히 자주 update되면 optimal value로 수렴할 수 있다.

즉, synchronous 방식은 한 iteration의 기준 시점을 명확히 유지하고, asynchronous 방식은 최신 정보를 즉시 재사용하여 실용적인 계산을 할 수 있다는 차이가 있다.

### Optimal policy 추출

Value Iteration이 $V_*$에 수렴한 뒤에는 각 state에서 one-step lookahead를 수행하여 optimal policy를 구한다.

$$
\pi_*(s)
= \arg\max_a\sum_{s',r}p(s',r \mid s,a)
\left[r+\gamma V_*(s')\right]
$$

아직 완전히 수렴하지 않은 근사 value $V$를 사용하면 다음과 같이 근사 policy를 구할 수 있다.

$$
\hat\pi(s)
= \arg\max_a\sum_{s',r}p(s',r \mid s,a)
\left[r+\gamma V(s')\right]
$$

Value Iteration의 핵심 알고리즘은 다음과 같이 요약할 수 있다.

{% capture value_iteration_algorithm %}
$$
\begin{array}{l}
\textbf{Initialize } V(s)\in\mathbb{R}\text{ arbitrarily for all }s\in\mathcal{S},\text{ except }V(\text{terminal})=0 \\
\textbf{Repeat} \\
\quad\quad \Delta \leftarrow 0 \\
\quad\quad \textbf{For each }s\in\mathcal{S}\textbf{:} \\
\quad\quad\quad\quad v \leftarrow V(s) \\
\quad\quad\quad\quad V(s) \leftarrow \max_a\sum_{s',r}p(s',r\mid s,a)\left[r+\gamma V(s')\right] \\
\quad\quad\quad\quad \Delta \leftarrow \max\left(\Delta,\lvert v-V(s)\rvert\right) \\
\textbf{Until }\Delta<\epsilon \\
\textbf{Output }\pi(s)=\operatorname*{arg\,max}_a\sum_{s',r}p(s',r\mid s,a)\left[r+\gamma V(s')\right]
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Algorithm 1. Value Iteration" label="algorithm:value-iteration" math=value_iteration_algorithm %}

### Value Iteration의 계산량과 한계

유한한 state space와 action space에서 모든 state $s$, action $a$, next state $s'$를 순회하면 한 번의 sweep에 대략 다음 계산량이 필요하다.

$$
\mathcal{O}(|S|^2|A|)
$$

reward가 여러 값으로 확률적으로 발생하여 $r$까지 모두 합산해야 한다면 계산량은 다음처럼 표현할 수 있다.

$$
\mathcal{O}(|S||A||S'||\mathcal{R}|)
$$

또한 $\Delta<\epsilon$이 될 때까지 여러 번 sweep해야 하므로 전체 계산량은 iteration 횟수에 비례해 증가한다. State나 action의 수가 커지면 table을 저장하는 것 자체가 어려워지는 차원의 저주가 발생한다.

Value Iteration은 value table $V$를 중심으로 계산하고 policy는 마지막에 one-step lookahead로 추출한다. 따라서 value가 수렴하기 전까지 policy를 명시적으로 유지하거나 개선하지 않는다. 또한 $Q$ function을 사용하면 action을 직접 비교할 수 있지만, $Q(s,a)$는 모든 state-action pair를 저장해야 하므로 $V(s)$보다 table의 크기가 커진다. 그래서 tabular DP에서는 보통 $V$ table을 사용해 메모리와 계산량을 줄인다.

이러한 Value Iteration의 한계를 보완하고 policy를 직접 평가·개선하는 방법으로 Policy Iteration을 사용할 수 있다.

## 06_Policy Iteration

Policy Iteration은 **policy evaluation**과 **policy improvement**를 번갈아 수행하여 optimal policy를 찾는 방법이다.

![Policy Iteration의 policy와 value 변화](/assets/img/blog/deep-reinforcement-learning-summary-2/policy-iteration-cycle.png)

Value Iteration은 매 value update에서 모든 action 중 최댓값을 바로 선택한다. 반면 Policy Iteration은 하나의 policy를 먼저 고정하여 평가한 뒤, 그 value를 이용해 policy를 개선한다.

### Policy Evaluation

현재 policy $\pi$를 고정하고, 그 policy를 따랐을 때의 state-value function $V^\pi$를 계산한다. 보통 policy iteration에서는 각 state에서 하나의 action을 선택하는 deterministic policy를 사용한다.

$$
V^\pi(s)
= \sum_{s',r}p(s',r \mid s,\pi(s))
\left[r+\gamma V^\pi(s')\right]
$$

Policy가 state $s$에서 선택하는 action이 이미 $\pi(s)$로 정해져 있으므로, Bellman expectation equation에서 action에 대한 summation이 사라진다. Value iteration처럼 모든 action을 비교하는 대신 policy가 선택한 하나의 action만 평가한다.

반복적인 policy evaluation은 다음과 같이 수행한다.

$$
V_{k+1}(s)
\leftarrow \sum_{s',r}p(s',r \mid s,\pi(s))
\left[r+\gamma V_k(s')\right]
$$

절차는 다음과 같다.

1. 모든 state의 value를 $V_0(s)=0$ 또는 임의의 값으로 초기화한다.
2. 고정된 policy $\pi$를 사용해 모든 state의 value를 반복적으로 update한다.
3. $V_{k+1}$과 $V_k$의 차이가 충분히 작아질 때까지 반복한다.

Policy evaluation이 수렴하면 $V^\pi$를 얻는다. 한 번의 sweep만 비교하면 Value Iteration보다 계산량이 작을 수 있지만, Policy Iteration은 각 policy마다 evaluation을 반복해야 하므로 전체 계산 시간이 항상 더 짧다고 말할 수는 없다.

### Policy Improvement

현재 policy의 value function $V^\pi$를 이용해 각 state에서 더 좋은 action을 선택하는 새로운 policy $\pi'$를 만든다.

$$
\begin{aligned}
\pi'(s)
&= \arg\max_a q_\pi(s,a) \\
&= \arg\max_a\sum_{s',r}p(s',r \mid s,a)
\left[r+\gamma V^\pi(s')\right]
\end{aligned}
$$

이때 $\pi'(s)$는 현재 $V^\pi$를 기준으로 한 one-step lookahead의 결과이다. Value Iteration에서는 $V_*$가 수렴한 뒤 policy를 추출하지만, Policy Iteration에서는 매 evaluation이 끝날 때마다 policy를 직접 개선한다.

새 policy가 모든 state에서 기존 policy와 같다면 policy가 stable하다고 판단하고 종료한다.

$$
\pi'(s)=\pi(s) \quad \text{for all }s\in S
$$

여기서 표기에 주의해야 한다. 엄밀하게 $\pi'(s)=\pi(s)$는 모든 state에서 두 policy가 같은 action을 선택한다는 **policy 자체의 동일성**을 뜻한다. 반면 Policy Improvement Theorem에서 더 이상 성능이 좋아지지 않았다는 의미는 다음과 같은 **value의 동일성**으로 표현하는 것이 정확하다.

$$
v_{\pi'}(s)=v_\pi(s) \quad \text{for all }s\in S
$$

서로 다른 action을 선택하더라도 action들의 value가 같은 경우에는 두 policy가 동일한 value를 만들 수 있다. 따라서 강의나 문맥에서 $\pi'=\pi$라고 간단히 표현한 부분이 policy 자체가 같다는 뜻인지, 모든 state에서 value가 같아 더 이상 개선되지 않는다는 뜻인지 구분해서 해석해야 한다. 구현에서는 보통 $\pi'(s)=\pi(s)$를 직접 비교하여 policy가 stable한지 확인한다.

이 경우 현재 policy는 optimal policy이다. 반대로 하나라도 더 좋은 action이 있으면 $\pi\leftarrow\pi'$로 바꾸고 다시 policy evaluation을 수행한다.

### Policy Improvement Theorem

Policy improvement가 실제로 policy를 더 좋게 만드는지 다음 정리로 확인할 수 있다.

두 policy $\pi$와 $\pi'$가 있고, 모든 state에서 다음 조건을 만족한다고 하자.

$$
q_\pi(s,\pi'(s)) \geq v_\pi(s)
\quad \text{for all }s\in S
$$

그러면 새로운 policy $\pi'$는 기존 policy $\pi$보다 좋거나 같다.

$$
v_{\pi'}(s) \geq v_\pi(s)
\quad \text{for all }s\in S
$$

#### 증명

조건에 의해 다음 부등식이 성립한다.

$$
\begin{aligned}
v_\pi(s)
&\leq q_\pi(s,\pi'(s)) \\
&= \mathbb{E}_{\pi'}
\left[R_{t+1}+\gamma v_\pi(S_{t+1})
\mid S_t=s\right]
\end{aligned}
$$

다음 state에서도 같은 policy improvement 조건을 적용하면 다음과 같이 한 단계씩 확장할 수 있다.

$$
\begin{aligned}
v_\pi(s)
&\leq \mathbb{E}_{\pi'}
\left[R_{t+1}+\gamma R_{t+2}
      +\gamma^2v_\pi(S_{t+2})
      \mid S_t=s\right] \\
&\leq \mathbb{E}_{\pi'}
\left[R_{t+1}+\gamma R_{t+2}+\gamma^2R_{t+3}+\cdots
      \mid S_t=s\right] \\
&= v_{\pi'}(s)
\end{aligned}
$$

즉, $\pi'$는 첫 action뿐 아니라 이후 state에서도 계속 더 좋은 action을 선택하므로, 전체 return의 expectation도 감소하지 않는다. 이 정리에 의해 Policy Iteration을 반복하면 policy value가 단조롭게 증가한다.

유한한 MDP에서 deterministic policy의 개수는 유한하므로, policy improvement가 더 이상 일어나지 않는 stable policy에 도달하면 그 policy는 optimal policy $\pi_*$이다.

#### Policy Iteration의 수렴 흐름

Policy Iteration은 다음 순서를 반복한다.

$$
\pi_0
\rightarrow V^{\pi_0}
\rightarrow \pi_1
\rightarrow V^{\pi_1}
\rightarrow \cdots
\rightarrow \pi_*
\rightarrow V_*
$$

![Policy Iteration의 evaluation과 improvement 반복](/assets/img/blog/deep-reinforcement-learning-summary-2/policy-iteration-convergence.png)

각 policy에 대해 먼저 policy evaluation을 수행해 $V^\pi$를 계산하고, 그 value를 이용해 greedy policy로 policy improvement를 수행한다. 이 과정을 반복하면 policy의 value는 감소하지 않고 점점 좋아진다.

#### Stable policy가 optimal policy인 이유

새로운 greedy policy $\pi'$가 기존 policy $\pi$보다 좋거나 같지만 더 이상 좋아지지 않는 상황을 생각해 보자.

$$
v_{\pi'}(s)=v_\pi(s) \quad \text{for all }s\in S
$$

Policy improvement의 정의에 의해 $\pi'$는 $V^\pi$에 대해 greedy하므로 다음이 성립한다.

$$
\begin{aligned}
v_{\pi'}(s)
&= v_\pi(s) \\
&= \max_a\sum_{s',r}p(s',r \mid s,a)
\left[r+\gamma v_\pi(s')\right] \\
&= \max_a\sum_{s',r}p(s',r \mid s,a)
\left[r+\gamma v_{\pi'}(s')\right]
\end{aligned}
$$

즉, $v_{\pi'}$가 Bellman optimality equation을 만족한다. Discounted finite MDP에서 Bellman optimality equation의 해는 유일하므로,

$$
v_{\pi'}(s)=v_*(s)
$$

가 되고 $\pi'$는 optimal policy가 된다. 따라서 policy improvement를 반복하다가 더 이상 value가 증가하지 않는 stable policy에 도달하면, 그 policy는 곧 $\pi_*$이다.

#### Policy Iteration 알고리즘

Policy Iteration은 다음과 같이 policy evaluation과 policy improvement를 반복한다.

{% capture policy_iteration_algorithm %}
$$
\begin{array}{l}
\textbf{Initialize }V(s)\in\mathbb{R}\text{ and }\pi(s)\in\mathcal{A}(s)\text{ arbitrarily for all }s\in\mathcal{S} \\
\textbf{Policy Evaluation:} \\
\quad\quad \textbf{Repeat} \\
\quad\quad\quad\quad \Delta\leftarrow 0 \\
\quad\quad\quad\quad \textbf{For each }s\in\mathcal{S}\textbf{:} \\
\quad\quad\quad\quad\quad\quad v\leftarrow V(s) \\
\quad\quad\quad\quad\quad\quad V(s)\leftarrow\sum_{s',r}p(s',r\mid s,\pi(s))\left[r+\gamma V(s')\right] \\
\quad\quad\quad\quad\quad\quad \Delta\leftarrow\max\left(\Delta,\lvert v-V(s)\rvert\right) \\
\quad\quad\textbf{Until }\Delta<\epsilon \\
\textbf{Policy Improvement:} \\
\quad\quad \textit{policy-stable}\leftarrow\text{true} \\
\quad\quad \textbf{For each }s\in\mathcal{S}\textbf{:} \\
\quad\quad\quad\quad \textit{old-action}\leftarrow\pi(s) \\
\quad\quad\quad\quad \pi(s)\leftarrow\operatorname*{arg\,max}_a\sum_{s',r}p(s',r\mid s,a)\left[r+\gamma V(s')\right] \\
\quad\quad\quad\quad \textbf{If }\textit{old-action}\neq\pi(s)\textbf{ then policy-stable}\leftarrow\text{false} \\
\textbf{If policy-stable, return }V\approx v_*\text{ and }\pi\approx\pi_*;\textbf{ otherwise go to Policy Evaluation}
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Algorithm 2. Policy Iteration" label="algorithm:policy-iteration" math=policy_iteration_algorithm %}

##### Policy evaluation update

Policy evaluation에서는 현재 policy $\pi$가 state $s$에서 선택하는 action $\pi(s)$가 이미 정해져 있다. 따라서 모든 action을 대상으로 최댓값을 계산하지 않고, 해당 action 하나만 사용한다.

$$
V_{k+1}(s)
\leftarrow \sum_{s',r}p(s',r \mid s,\pi(s))
\left[r+\gamma V_k(s')\right]
$$

이 점에서 Value Iteration의 다음 update와 차이가 있다.

$$
V_{k+1}(s)
\leftarrow \max_a\sum_{s',r}p(s',r \mid s,a)
\left[r+\gamma V_k(s')\right]
$$

Value Iteration은 매 update마다 모든 action을 비교하지만, Policy Iteration의 policy evaluation은 현재 policy가 정한 action 하나만 평가한다.

##### Policy improvement update

Policy evaluation이 끝나면 현재 value $V^\pi$를 사용해 각 state에서 가장 좋은 action을 선택하도록 policy를 바꾼다.

$$
\pi(s)\leftarrow \arg\max_a\sum_{s',r}p(s',r \mid s,a)
\left[r+\gamma V^\pi(s')\right]
$$

Policy improvement 전의 action을 $\text{old-action}$으로 저장해 두고, policy improvement 후 action이 바뀌었는지 확인한다.

$$
\text{old-action} \neq \pi(s)
\quad\Longrightarrow\quad
\text{policy-stable}=\text{false}
$$

모든 state에서 action이 바뀌지 않았다면 policy가 stable하므로 반복을 즉시 종료하고 현재 $V$와 $\pi$를 반환한다.

##### Value Iteration과 비교한 장점

- Policy evaluation에서는 $\max_a$를 계산하지 않고 $a=\pi(s)$ 하나만 사용하므로 한 번의 backup이 단순하다.
- Policy improvement가 끝난 뒤 policy가 stable한지 검사하므로, policy가 더 이상 바뀌지 않으면 즉시 종료할 수 있다.
- Value Iteration처럼 value의 수치적 변화만 계속 확인하는 대신, policy 자체가 안정되었는지를 종료 조건으로 사용할 수 있다.

다만 Policy Iteration은 각 policy마다 policy evaluation을 수렴할 때까지 반복해야 한다. 따라서 한 번의 update는 Value Iteration보다 저렴할 수 있지만, 전체 계산 시간이 항상 더 짧은 것은 아니다.

## 07_Value Iteration 구현

다음 GridWorld 환경에서 Value Iteration을 직접 구현하는 문제이다.

![Value Iteration 구현 문제](/assets/img/blog/deep-reinforcement-learning-summary-2/value-iteration-exercise.png)

### 정답 예시

![Value Iteration 구현 결과](/assets/img/blog/deep-reinforcement-learning-summary-2/value-iteration-solution.png)

## 참고 강의

- [고려대 오승상 강화학습 05 — Bellman equation 1](https://www.youtube.com/watch?v=Z8RZbcg96Qk)
- [고려대 오승상 강화학습 06 — Bellman equation 2](https://www.youtube.com/watch?v=WoJoB1D69cA)
- [고려대 오승상 강화학습 07 — Dynamic Programming](https://www.youtube.com/watch?v=4i_ycR6uCdQ)
- [고려대 오승상 강화학습 08 — Value Iteration](https://www.youtube.com/watch?v=rC6xkxS_myY)
- [고려대 오승상 강화학습 09 — Policy Iteration](https://www.youtube.com/watch?v=6GhwCE43oFk)
