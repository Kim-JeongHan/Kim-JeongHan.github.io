---
layout: post
title: Reinforcement Learning 1 - Markov Decision Process
date: 2026-08-25 00:00:00 +0900
slug: reinforcement-learning-study-log
render_with_liquid: false
use_math: true
categories:
- 공부
- 강화학습
tags:
- reinforcement-learning
---

## 00_RL 기본 구성

- **State**: agent가 가질 수 있는 상태
- **Action**: agent의 행동
- **Reward**: action의 결과로 environment가 agent에게 주는 즉각적인 보상
- **Policy**: 어떤 state에서 수행할 action을 결정하는 장치
- **Agent**: policy에 따라 action을 선택하고 reward를 바탕으로 학습하는 주체
- **Environment**: agent의 action을 받아 다음 state와 reward를 반환하는 외부 세계

강화학습은 다음과 같은 상호작용을 반복한다.

$$
S_t \xrightarrow{A_t} (R_{t+1}, S_{t+1})
$$

따라서 한 번의 경험은 보통 $(S_t, A_t, R_{t+1}, S_{t+1})$로 기록한다.

강화학습에서 실제로 최적화하려는 것은 한 시점의 reward가 아니라 미래 reward까지 포함한 **return**이다.

$$
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots
    = \sum_{k=0}^{\infty} \gamma^k R_{t+1+k}
$$

여기서 $\gamma$는 discount factor이며 $0 \leq \gamma \leq 1$이다. $\gamma$가 작으면 가까운 미래의 reward를 더 중요하게 보고, $\gamma$가 1에 가까우면 먼 미래의 reward도 중요하게 본다.

즉, $G_t$는 time step $t$를 기준으로 이후에 발생하는 모든 reward를 시간 순서와 함께 합친 값이다. $t$에서 $k$ step 뒤에 발생하는 reward에는 $\gamma^k$라는 가중치가 붙는다.

$$
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots
$$

가장 가까운 reward는 큰 가중치로 반영되고, 더 늦게 발생하는 reward일수록 작은 가중치로 반영된다. 따라서 discount factor는 현재와 먼 미래의 reward를 서로 다른 중요도로 더해주는 역할을 한다.

많은 MDP와 강화학습 문제에서 discount factor를 사용하는 이유는 다음과 같다.

- **Infinite return 방지**: reward가 무한히 이어지는 continuing task에서 $0 \leq \gamma < 1$이면, reward가 유한하게 bounded되어 있다는 조건 아래 infinite sum을 수학적으로 수렴시킬 수 있다.
- **미래의 불확실성 반영**: 먼 미래의 reward는 현재 시점에서 예측하기 어렵고 실제로 얻지 못할 가능성도 더 크다. Discounting은 이러한 불확실성을 단순화하여 표현할 수 있다.
- **실용적인 의사결정**: 일반적으로 먼 미래보다 가까운 미래의 reward를 더 중요하게 보는 것이 현실적인 경우가 많다.
- **유한한 episode**: episode가 유한한 horizon에서 종료된다면 infinite sum 문제가 발생하지 않는다. 이런 경우에는 discounting을 사용하지 않고 $\gamma=1$로 두기도 한다.

유한한 episode가 time step $T$에서 끝난다면 return은 다음과 같이 유한합으로 쓸 수 있다.

$$
G_t = \sum_{k=0}^{T-t-1} \gamma^k R_{t+1+k}
$$

### Policy Evaluation과 Policy Improvement

- **Policy evaluation**: policy를 따랐을 때 얻는 return의 기대값을 계산하는 과정
- **Policy improvement**: policy evaluation 결과를 높이는 방향으로 policy를 개선하는 과정

Policy는 state가 주어졌을 때 action을 선택하는 확률분포로 표현할 수 있다.

$$
\pi(a \mid s) = P(A_t = a \mid S_t = s)
$$

즉, policy는 state $s$를 보았을 때 action $a$를 선택할 확률을 알려준다. 하나의 state에서 가능한 모든 action에 대한 확률의 합은 1이다.

$$
\sum_a \pi(a \mid s) = 1
$$

#### Stochastic policy와 deterministic policy

**Stochastic policy**는 하나의 state에서 여러 action을 확률적으로 선택하는 policy이다. 같은 state를 보더라도 매번 다른 action이 선택될 수 있다.

$$
\pi(a \mid s) = P(A_t=a \mid S_t=s)
$$

반면 **deterministic policy**는 state마다 하나의 action을 정해두고 항상 그 action만 선택한다.

$$
\pi(s) = a
$$

Deterministic policy를 stochastic policy의 특수한 경우로 표현하면 다음과 같다.

$$
\pi(a' \mid s) =
\begin{cases}
1, & a'=\pi(s) \\
0, & a'\neq\pi(s)
\end{cases}
$$

Policy는 현재 state에 필요한 정보가 모두 포함되어 있다는 Markov assumption 아래에서 과거의 trajectory 전체를 직접 고려하지 않는다.

$$
P(A_t=a \mid S_0,A_0,\ldots,S_t=s)
= P(A_t=a \mid S_t=s)
$$

#### Known MDP와 unknown MDP에서의 policy

Known MDP에서는 transition probability $P$와 reward function $R$을 알고 있으므로, value function을 계산한 뒤 optimal policy를 구할 수 있다. 표준적인 유한 MDP에서는 deterministic optimal policy가 존재하며, 이를 $\pi_*$로 나타낸다.

$$
\pi_*(s) \in \arg\max_a Q_*(s,a)
$$

동일한 최댓값을 갖는 action이 여러 개라면 그중 하나를 deterministic하게 골라도 되고, 여러 action을 확률적으로 섞은 stochastic policy도 같은 value를 가질 수 있다.

Unknown MDP에서는 transition과 reward를 처음부터 알 수 없기 때문에, 현재 가장 좋아 보이는 action만 계속 선택하면 아직 충분히 시도하지 않은 action을 발견하지 못할 수 있다. 따라서 **exploration**과 **exploitation**을 함께 고려하는 stochastic policy가 필요하다.

- **Exploitation**: 지금까지의 경험으로 가장 높은 value를 가진 action을 선택하는 것
- **Exploration**: 다른 action도 시도하여 더 좋은 policy나 reward를 발견하는 것

대표적인 방법이 $\epsilon$-greedy policy이다. 확률 $1-\epsilon$으로 현재 가장 좋다고 추정한 action을 선택하고, 확률 $\epsilon$으로 다른 action을 포함한 random action을 선택한다.

$$
\pi_\epsilon(a \mid s) =
\begin{cases}
1-\epsilon + \dfrac{\epsilon}{|A|}, & a \in \arg\max_{a'} Q(s,a') \\
\dfrac{\epsilon}{|A|}, & \text{otherwise}
\end{cases}
$$

$\epsilon$-greedy는 경험이 적은 action을 일부러 선택할 가능성을 남겨두어 exploration을 가능하게 한다. 학습이 진행되면서 $\epsilon$을 점차 줄이면 초기에는 다양한 action을 탐색하고, 이후에는 좋은 action을 더 자주 선택하도록 만들 수 있다.

Policy $\pi$의 state value는 해당 state에서 policy를 계속 따랐을 때의 expected return이다.

$$
V^\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s]
$$

즉, state $s$를 시작 state로 고정한 뒤 policy $\pi$에 따라 action을 선택하면서 만들어지는 여러 trajectory의 return을 생각하고, 그 return들의 expectation을 계산한 값이다.

![State value function $V^\pi(s)$의 여러 trajectory](/assets/img/blog/reinforcement-learning-study-log/v-pi-trajectory.png)

Value function은 Bellman expectation equation을 이용해 다음과 같이 한 단계 reward와 다음 state의 value로 나누어 표현할 수 있다.

$$
V^\pi(s)
= \mathbb{E}_\pi\left[R_{t+1} + \gamma V^\pi(S_{t+1}) \mid S_t = s\right]
$$

Action value는 특정 state에서 특정 action을 먼저 수행한 뒤 policy를 따랐을 때의 expected return이다.

$$
Q^\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t=s, A_t=a]
$$

여기서는 시작 state $s$뿐 아니라 첫 action $a$까지 고정한다. 그 이후의 action들은 policy $\pi$에 따라 선택되며, stochastic environment와 stochastic policy 때문에 여러 trajectory와 return이 나올 수 있다. 따라서 $Q^\pi(s,a)$는 그 return들의 expectation이다.

![Action value function $Q^\pi(s,a)$의 여러 trajectory](/assets/img/blog/reinforcement-learning-study-log/q-pi-trajectory.png)

두 value function의 차이는 첫 action을 고정했는지 여부이다. State value는 현재 state에서 policy가 선택하는 여러 action을 모두 고려하고, action value는 특정 action을 선택한 뒤의 결과만 평가한다.

$$
V^\pi(s) = \sum_a \pi(a \mid s) Q^\pi(s,a)
$$

Policy improvement의 대표적인 방법은 현재 policy의 action value가 가장 큰 action을 선택하도록 policy를 바꾸는 것이다.

$$
\pi'(s) = \arg\max_a Q^\pi(s,a)
$$

## 01_Stochastic Process

- **Deterministic process**: action을 취하면 의도한 대로 state가 바뀐다. 예를 들어 북쪽으로 가라는 action을 수행하면 100% 확률로 북쪽으로 이동한다.
- **Stochastic process**: 북쪽으로 가라는 action을 수행해도 남쪽으로 갈 수 있다. 원하는 결과가 100% 발생하지 않고 확률에 따라 state가 달라진다.

환경의 transition뿐 아니라 policy 자체도 stochastic할 수 있다. 현실 문제의 불확실성을 표현하거나 exploration을 위해 stochastic policy를 사용하는 경우가 많다. 반대로 시뮬레이션 환경과 일부 알고리즘에서는 deterministic transition 또는 deterministic policy를 사용하기도 한다.

환경의 transition은 다음과 같이 표현할 수 있다.

$$
P(S_{t+1}=s' \mid S_t=s, A_t=a)
$$

Deterministic process에서는 어떤 함수 $f$가 존재하여 다음 state가 항상 정해진다.

$$
S_{t+1} = f(S_t, A_t)
$$

## 02_Markov Property와 Transition

과거의 모든 정보가 현재 state에 요약되어 있어서, 현재 state를 알고 있다면 과거를 추가로 알더라도 미래 state의 조건부 확률이 달라지지 않는 성질이다.

$$
P(S_{t+1} = s' \mid S_t = s)
= P(S_{t+1} = s' \mid S_0 = s_0, S_1 = s_1, \ldots, S_t = s)
$$

강화학습에서는 action까지 포함해 다음과 같이 표현하는 것이 더 일반적이다.

$$
P(S_{t+1}=s', R_{t+1}=r \mid S_t=s, A_t=a)
= P(S_{t+1}=s', R_{t+1}=r \mid S_0,A_0,\ldots,S_t=s,A_t=a)
$$

과거를 모두 저장하지 않아도 되므로 연산량과 메모리를 줄일 수 있다. 이러한 특성 때문에 Markov property를 memoryless property라고도 한다. 단, 현재 state에 필요한 정보가 빠져 있으면 Markov property가 성립하지 않는다. 예를 들어 속도가 중요한 환경에서 위치만 state로 사용하면, 같은 위치라도 속도가 다른 상황을 구분하지 못할 수 있다.

### Transition

Transition probability는 state $s_i$에서 state $s_j$로 이동할 확률이다. Stochastic process에서는 action을 수행해도 다음 state가 하나로 정해지지 않을 수 있기 때문에 transition probability가 필요하다.

$$
P_{ij} := P_{s_i s_j}
= p(s_j \mid s_i)
= P(S_{t+1} = s_j \mid S_t = s_i)
$$

state가 유한하고 $n$개라면 transition probability를 행렬로 표현할 수 있다.

$$
P =
\begin{bmatrix}
P_{11} & P_{12} & \cdots & P_{1n} \\
P_{21} & P_{22} & \cdots & P_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
P_{n1} & P_{n2} & \cdots & P_{nn}
\end{bmatrix}
$$

각 원소는 확률이므로 0 이상이고, 특정 state에서 출발했을 때 어디론가 이동할 확률의 합은 1이다.

$$
P_{ij} \geq 0, \qquad \sum_{j=1}^{n} P_{ij}=1
$$

state 분포를 행벡터 $\mathbf{p}_t$로 표현하면 한 단계 뒤의 분포는 다음과 같이 계산한다.

$$
\mathbf{p}_{t+1} = \mathbf{p}_t P
$$

## 03_Markov Process

Markov process 또는 Markov chain은 다음 두 요소로 구성된다.

- $S$: state들의 집합
- $P$: state 간 transition probability matrix

Reward까지 포함하면 Markov reward process가 된다.

$$
\text{MRP} = (S, P, R, \gamma)
$$

여기서 $R$은 각 state 또는 transition에서 얻는 reward를 나타낸다.

## 04_Markov Decision Process

MDP는 agent가 action을 선택할 수 있는 Markov process이다. MDP의 state가 현재 상황에 필요한 정보를 모두 포함하고 있다면 Markov property가 성립한다.

MDP는 다음 다섯 요소로 구성된다.

$$
\text{MDP} = (S, A, P, R, \gamma)
$$

- $S$: state space, 가능한 모든 state의 집합
- $A$: action space, agent가 선택할 수 있는 action의 집합
- $P$: state transition probability
- $R$: reward function
- $\gamma$: discount factor

### Transition probability

MDP에서는 state뿐 아니라 agent가 선택한 action까지 고려하여 transition probability를 정의한다. State $s$에서 action $a$를 수행했을 때 다음 state $s'$로 이동할 확률은 다음과 같다.

$$
P^a_{ss'}
= p(s' \mid s,a)
= P(S_{t+1}=s' \mid S_t=s,A_t=a)
$$

즉, action $a$가 state $s$에서 state $s'$로 이동하는 결과에 영향을 준다. 각 state-action 쌍에 대해 가능한 다음 state로 이동할 확률의 합은 1이다.

$$
\sum_{s' \in S} P^a_{ss'} = 1
$$

MDP에서 environment model은 주로 transition probability $P$와 reward function $R$을 의미한다. 이 model이 있으면 특정 state에서 action을 수행했을 때 어떤 state로 이동하고 어떤 reward를 받을지 예측할 수 있다.

### Reward function

Reward는 state $s$에서 action을 수행하고 다음 state로 이동할 때 얻는 값이다. Reward가 무엇에 의존하는지에 따라 다음과 같이 여러 형태로 표현할 수 있다.

$$
R_s \qquad\text{(state에만 의존)}
$$

$$
R_s^a \qquad\text{(state와 action에 의존)}
$$

$$
R_{ss'}^a \qquad\text{(state, action, 다음 state에 의존)}
$$

### Reward hypothesis

Agent는 누적 reward의 기대값을 최대화하는 방향으로 학습한다. 강화학습은 다음과 같은 **reward hypothesis**를 기본 가정으로 삼는다.

> 모든 목표는 누적 reward의 기대값을 최대화하는 문제로 표현할 수 있다.

따라서 policy의 목적 함수는 다음과 같이 표현할 수 있다.

$$
J(\pi)
= \mathbb{E}_\pi\left[\sum_{t=0}^{T-1} \gamma^t R_{t+1}\right]
$$

그리고 optimal policy는 이 목적 함수를 가장 크게 만드는 policy이다.

$$
\pi_* \in \arg\max_\pi J(\pi)
$$

### Reward의 종류와 기대값

Reward가 어떤 정보에 의존하는지에 따라 다음과 같이 표현할 수 있다.

$$
R = R(s), \qquad R(s,a), \qquad R(s,a,s')
$$

- $R(s)$: 현재 state $s$에만 의존하는 reward
- $R(s,a)$: 현재 state $s$와 action $a$에 의존하는 reward
- $R(s,a,s')$: 현재 state $s$, action $a$, 다음 state $s'$에 의존하는 reward

MDP에서는 state에서 다음 state로 이동할 때 action이 포함된다. 또한 같은 $(s,a)$에서 출발해도 다음 state나 reward가 확률적으로 달라질 수 있다. 따라서 transition과 reward를 함께 나타내는 joint probability를 사용할 수 있다.

$$
p(s',r \mid s,a)
= P(S_{t+1}=s', R_{t+1}=r \mid S_t=s,A_t=a)
$$

여기서 $r$은 가능한 reward 중 실제로 발생한 값이고, $\mathcal{R}$은 가능한 reward 값들의 집합이다. Reward를 marginalize하면 state transition probability를 얻는다.

$$
p(s' \mid s,a)
= \sum_{r \in \mathcal{R}} p(s',r \mid s,a)
$$

반대로 state-action 쌍에서 얻는 expected reward는 가능한 모든 다음 state와 reward를 고려하여 계산한다.

$$
R_s^a
= r(s,a)
= \mathbb{E}[R_{t+1} \mid S_t=s,A_t=a]
= \sum_{s' \in S}\sum_{r \in \mathcal{R}} r\,p(s',r \mid s,a)
$$

다음 state $s'$까지 알고 있을 때의 expected reward는 다음과 같다. 단, $p(s' \mid s,a)>0$인 경우를 가정한다.

$$
R_{ss'}^a
= r(s,a,s')
= \mathbb{E}[R_{t+1} \mid S_t=s,A_t=a,S_{t+1}=s']
= \frac{\sum_{r \in \mathcal{R}} r\,p(s',r \mid s,a)}{p(s' \mid s,a)}
$$

즉, reward가 stochastic하면 하나의 reward 값만 사용하는 것이 아니라 가능한 reward와 transition의 확률을 모두 고려하여 expected reward를 계산한다.

### Optimal policy

Policy $\pi$ 중에서 모든 state에서 가장 높은 expected return을 만들어내는 policy를 optimal policy라고 하며 $\pi_*$로 표기한다.

$$
\pi_* \in \arg\max_\pi V^\pi(s)
$$

Optimal value function은 다음과 같이 정의한다.

$$
V_*(s) = \max_\pi V^\pi(s)
$$

여기서 중요한 점은 optimal policy가 매 순간 reward가 가장 큰 action만 선택하는 policy는 아니라는 것이다. 현재 reward가 조금 작더라도 장기적으로 더 큰 return을 만들 수 있다면 그 action을 선택할 수 있다.

### Reward 설계에 따른 policy 변화

다음 Grid World 예시에서는 목표 state에 도착하면 $+1$, 위험한 terminal state에 도착하면 $-1$을 받는다. 그 외의 이동에서는 매 step마다 다음과 같은 작은 penalty를 받는다고 하자.

$$
R_{ss'}^a = c
$$

![Step reward에 따른 optimal policy 변화](/assets/img/blog/reinforcement-learning-study-log/reward-design-gridworld.png)

한 episode에서 terminal state에 도착하기 전까지 $N$번 이동하고, 매 이동마다 $c$의 reward를 받는다면 terminal reward를 제외한 return은 다음과 같이 계산된다.

$$
G_0 = c + \gamma c + \gamma^2 c + \cdots + \gamma^{N-1}c
      + \gamma^N R_{\mathrm{terminal}}
$$

$\gamma=1$인 단순한 경우에는 다음과 같다.

$$
G_0 = Nc + R_{\mathrm{terminal}}
$$

- $c=-0.01$: step penalty의 크기가 작으므로 이동 횟수가 늘어나더라도 $-1$ state를 피하는 안전한 경로를 선택한다. **slow but safe**한 policy가 된다.
- $c=-0.4$: 이동 횟수와 위험성을 적절히 절충하는 policy가 된다.
- $c=-2$: 한 번 이동할 때마다 큰 penalty를 받으므로, 위험을 감수하더라도 가능한 한 빨리 끝내는 policy가 된다.

즉, reward의 크기와 구조는 agent가 무엇을 좋은 행동이라고 판단하는지를 결정한다. 따라서 실제 문제에서는 reward를 잘못 설계하면 agent가 의도와 다른 행동을 학습할 수 있으며, 이를 reward design 또는 reward shaping 문제라고 한다.

### Discount factor

$\gamma$는 미래 reward를 현재 시점에서 얼마나 중요하게 반영할지 결정하는 discount factor이다.

$$
0 \leq \gamma \leq 1
$$

일반적으로 continuing task에서는 $\gamma < 1$을 사용하여 먼 미래의 reward를 할인하고 return이 수렴하도록 한다. $\gamma$가 0이면 즉시 받는 reward만 고려하고, 1에 가까울수록 미래 reward를 현재 reward와 비슷한 비중으로 고려한다.

### Model-based와 model-free

- **Model-based**: MDP의 model, 특히 transition probability $P$와 reward function $R$을 알고 있는 경우다. 현재 model을 이용해 미래를 예측하며, 대표적으로 dynamic programming을 사용할 수 있다.
- **Model-free**: MDP의 model을 직접 알지 못하는 경우다. environment와 직접 상호작용하며 얻은 경험으로 value function이나 policy를 학습한다.

따라서 model-based와 model-free의 차이는 agent가 environment의 transition과 reward model을 알고 있는지에 있다. 둘 다 강화학습의 접근법으로 볼 수 있으며, model-free 방법은 model을 명시적으로 만들지 않고 경험에서 바로 policy 또는 value를 학습한다.

### State와 action space의 크기

MDP 이론은 state space $S$와 action space $A$가 finite인지 infinite인지와 관계없이 정의할 수 있다. 다만 기초적인 예제와 dynamic programming에서는 계산을 쉽게 하기 위해 유한한 state와 action을 주로 사용한다. 실제 강화학습에서는 연속적인 위치, 속도, 관절각 등을 다루기 때문에 $S$나 $A$가 infinite인 경우도 많다.

## 05_Notation 정리

| 표기 | 의미 |
| --- | --- |
| $P(X=x)$ 또는 $p(x)$ | random variable $X$가 $x$라는 값을 가질 확률 |
| $\mathbb{E}[X]$ | random variable $X$의 expectation. 이산 random variable이라면 $\mathbb{E}[X]=\sum_x p(x)x$ |
| $\max_a f(a)$ | 집합 안에서 $f(a)$가 가질 수 있는 최댓값 |
| $\arg\max_a f(a)$ | $f(a)$를 최댓값으로 만드는 $a$의 값 |
| $S_t, A_t, R_t$ | time step $t$의 state, action, reward |
| $G_t$ | time step $t$ 이후의 total discounted reward, 즉 return |
| $p(s' \mid s,a)$ | state $s$에서 action $a$를 수행했을 때 state $s'$로 이동할 transition probability |
| $p(s',r \mid s,a)$ | state $s$에서 action $a$를 수행했을 때 state $s'$로 이동하고 reward $r$을 받을 joint probability |
| $\pi$ | policy, state를 action으로 연결하는 decision-making rule |
| $\pi(a \mid s)$ | stochastic policy. state $s$에서 action $a$를 선택할 확률 |
| $\pi(s)$ | deterministic policy. state $s$에서 선택하는 action |
| $v_\pi(s)$ 또는 $V^\pi(s)$ | policy $\pi$를 따를 때 state $s$의 value, 즉 expected return |
| $v_*(s)$ 또는 $V_*(s)$ | optimal policy $\pi_*$를 따를 때 state $s$의 optimal value |
| $q_\pi(s,a)$ 또는 $Q^\pi(s,a)$ | policy $\pi$에서 state $s$에서 action $a$를 수행했을 때의 action value |
| $q_*(s,a)$ 또는 $Q_*(s,a)$ | optimal policy 기준으로 state $s$에서 action $a$를 수행했을 때의 optimal action value |
{: .policy-comparison-table}

Reward의 time index는 교재나 문맥에 따라 다르게 정의될 수 있다. 현재 문서에서는 $A_t$를 수행한 뒤 받는 reward를 $R_{t+1}$로 표기하지만, $R_t$를 $S_{t-1}, A_{t-1}$의 결과로 정의하는 표기법도 사용한다.

## 참고 강의

- [고려대 오승상 강화학습 01 — DRL Introduction](https://www.youtube.com/watch?v=HXIbrL-glpU)
- [고려대 오승상 강화학습 02 — Markov property](https://www.youtube.com/watch?v=EtSNMoM97-k)
- [고려대 오승상 강화학습 03 — Markov Decision Process](https://www.youtube.com/watch?v=S-7lXVpFci4)
- [고려대 오승상 강화학습 04 — Reward and Policy](https://www.youtube.com/watch?v=Mvzu5CwcUpw)
