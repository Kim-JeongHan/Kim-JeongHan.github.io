---
layout: post
title: Deep Reinforcement Learning 요약 3
date: 2026-08-26 00:02:00 +0900
slug: deep-reinforcement-learning-summary-3
render_with_liquid: true
use_math: true
categories:
- 공부
- 강화학습
tags:
- reinforcement-learning
---

## Dynamic Programming과 Reinforcement Learning의 비교

Dynamic Programming(DP)과 Reinforcement Learning(RL)은 모두 Bellman equation을 이용해 value function과 optimal policy를 찾는다. 하지만 value를 계산할 때 environment model을 사용하는지, 모든 가능한 branch를 계산하는지, 실제 sample 하나를 사용하는지에서 차이가 난다.

## Bellman expectation equation의 두 가지 표현

State-value function은 time step $t$ 이후에 얻는 return $G_t$의 expectation으로 정의된다.

$$
v_\pi(s) = \mathbb{E}_\pi[G_t \mid S_t=s]
$$

Return의 재귀 관계를 사용하면 같은 value를 즉시 reward와 next state의 value로 표현할 수 있다.

$$
v_\pi(s)
= \mathbb{E}_\pi
\left[R_{t+1}+\gamma v_\pi(S_{t+1})
\mid S_t=s\right]
$$

첫 번째 식은 episode가 끝날 때까지 얻은 전체 return $G_t$를 사용한다. 두 번째 식은 한 step 뒤의 reward $R_{t+1}$와 next state value $v_\pi(S_{t+1})$를 사용한다.

두 식은 서로 다른 value를 정의하는 것이 아니라, Bellman equation에 의해 같은 value를 두 가지 방식으로 표현한 것이다.

## Backup 방식

![Dynamic Programming, Monte Carlo, Temporal Difference backup 비교](/assets/img/blog/deep-reinforcement-learning-summary-3/dp-mc-td-backup-comparison.png)

### Dynamic Programming: full backup

DP는 transition probability와 reward function을 알고 있는 model-based 방법이다. 가능한 모든 next state와 reward의 branch를 고려하여 expectation을 계산한다.

$$
V(S_t) \leftarrow
\mathbb{E}_\pi
\left[R_{t+1}+\gamma V(S_{t+1})\right]
$$

따라서 DP는 특정 episode 하나만 선택하는 것이 아니라, model이 알려주는 모든 가능한 결과를 사용한다. 모든 branch를 계산해야 하므로 full backup이라고 한다.

Return $G_t$를 직접 계산하려면 가능한 episode가 끝날 때까지의 모든 경로를 고려해야 하므로 계산량이 매우 커질 수 있다. DP는 이를 한 step reward와 next value를 이용하는 Bellman equation 형태로 바꾸어 계산한다.

### Monte Carlo: sample multi-step backup

Monte Carlo(MC)는 model을 알지 못해도 실제 environment와 상호작용하여 얻은 하나의 episode sample을 사용할 수 있다. Episode가 끝난 뒤 실제 return $G_t$를 이용해 value를 update한다.

$$
V(S_t) \leftarrow V(S_t)
+ \alpha\left[G_t-V(S_t)\right]
$$

전체 episode의 reward를 사용하므로 sample multi-step backup이라고 한다. 실제 sample 하나를 사용하기 때문에 모든 가능한 branch를 계산할 필요는 없지만, episode가 끝나야 return을 계산할 수 있다.

### Temporal Difference: sample one-step backup

Temporal Difference(TD)는 하나의 sample에서 한 step 뒤에 관측한 reward와 next state의 현재 value estimate를 사용한다.

$$
V(S_t) \leftarrow V(S_t)
+ \alpha\left[R_{t+1}+\gamma V(S_{t+1})-V(S_t)\right]
$$

TD는 한 step만 사용하는 sample backup이므로 episode가 끝나기 전에도 value를 update할 수 있다. 또한 $V(S_{t+1})$라는 현재 추정값을 target에 사용하므로 bootstrapping을 수행한다.

## DP, MC, TD의 차이

| 방법 | Model | Target | Backup | Episode 종료 |
| --- | --- | --- | --- | --- |
| Dynamic Programming | 필요 | $\mathbb{E}[R_{t+1}+\gamma V(S_{t+1})]$ | 모든 branch를 사용하는 full backup | 불필요 |
| Monte Carlo | 불필요 | $G_t$ | 실제 episode의 sample multi-step backup | 필요 |
| Temporal Difference | 불필요 | $R_{t+1}+\gamma V(S_{t+1})$ | 실제 sample one-step backup | 불필요 |

정리하면 DP는 model을 이용해 Bellman expectation을 정확하게 계산하고, MC와 TD는 sample을 이용해 value를 근사한다. MC는 전체 return $G_t$를 사용하고, TD는 한 step reward와 next value를 사용한다. 따라서 DP와 TD는 비슷한 one-step target을 사용하지만, DP는 모든 가능한 branch를 계산하고 TD는 관측된 sample 하나만 사용한다.

## DP와 RL에서 policy를 개선하는 방법

DP에서는 transition probability와 reward function을 알고 있으므로, state $s$에서 각 action을 수행했을 때의 expected value를 모두 계산할 수 있다. 따라서 state-value function $V^\pi$를 사용해 다음과 같이 policy를 개선할 수 있다.

$$
\pi'(s)
= \arg\max_a\sum_{s',r}p(s',r \mid s,a)
\left[r+\gamma V^\pi(s')\right]
$$

위 식의 summation은 transition probability $p(s',r\mid s,a)$를 이용해 가능한 모든 next state와 reward를 평균내는 과정이다. 이 값은 action-value function과 같으므로 다음처럼 쓸 수도 있다.

$$
\pi'(s) = \arg\max_a q_\pi(s,a)
$$

DP는 $Q$를 계산할 수 있지만, 모든 state-action pair에 대한 값을 저장하면 계산량과 메모리 사용량이 커진다. 그래서 tabular DP에서는 $V(s)$를 저장하고, policy improvement를 수행할 때 필요한 순간에 model을 이용해 one-step lookahead를 계산하는 경우가 많다.

반면 model-free RL에서는 transition probability $p(s',r\mid s,a)$를 알지 못한다. 따라서 DP처럼 가능한 모든 next state와 reward에 대한 summation을 직접 계산할 수 없다. Q-based RL에서는 sample data를 이용해 action-value function $Q(s,a)$를 직접 학습하고, 학습된 Q값을 비교해 policy를 정한다.

$$
\pi'(s) = \arg\max_a Q(s,a)
$$

정리하면 다음과 같다.

- **DP**: $P$와 $R$을 알고 있으므로 $V^\pi$와 model을 이용해 $q_\pi(s,a)$를 계산한 뒤 policy를 개선한다.
- **Q-based RL**: $P$를 모르므로 $Q(s,a)$를 sample로 직접 추정하고, 가장 큰 Q값을 갖는 action을 선택한다.

다만 model-free RL이 반드시 Q function만 사용해야 하는 것은 아니다. Policy Gradient처럼 policy를 직접 학습하거나, Actor-Critic처럼 policy와 value function을 함께 학습하는 방법도 있다. 여기서는 discrete action을 Q값으로 비교하는 Q-based RL의 경우를 다룬다.

## Generalized Policy Iteration (GPI)

Generalized Policy Iteration(GPI)은 Policy Iteration을 더 일반화한 관점이다. GPI 자체는 model-based와 model-free 모두에 적용할 수 있으며, 다음 두 과정이 서로 영향을 주고받으며 반복되는 구조로 이해할 수 있다.

- **Policy Evaluation**: 현재 policy가 얼마나 좋은지 value function 또는 action-value function으로 평가한다.
- **Policy Improvement**: 현재 value function이나 Q function을 기준으로 더 좋은 action을 선택하도록 policy를 개선한다.

Policy Iteration에서는 policy evaluation을 충분히 수행하여 $V^\pi$를 구한 뒤 policy improvement를 수행한다. 반면 GPI에서는 value function을 정확하게 수렴시킬 때까지 기다리지 않고, 근사된 value를 이용해 policy를 조금씩 개선할 수 있다.

Model-based GPI의 예인 DP에서는 model을 알고 있으므로 full backup을 사용해 policy evaluation을 비교적 정확하게 수행한다.

$$
V^\pi(s) \leftarrow
\mathbb{E}_\pi\left[R_{t+1}+\gamma V^\pi(S_{t+1})\right]
$$

Model-free RL에서 사용하는 GPI는 sample backup으로 value function을 근사적으로 평가하고, 그 결과를 이용해 policy를 개선한다.

$$
V(s) \leftarrow V(s)
+ \alpha\left[\text{sample target}-V(s)\right]
$$

그 후 현재의 근사 value 또는 Q function을 사용해 policy improvement를 수행한다.

![Generalized Policy Iteration의 policy evaluation과 policy improvement](/assets/img/blog/deep-reinforcement-learning-summary-3/generalized-policy-iteration.png)

그림에서 위쪽의 $Q=q_\pi$는 policy evaluation이 현재 policy의 value를 추정하는 과정이고, 아래쪽의 $\pi=\text{greedy}(Q)$는 현재 Q function을 기준으로 policy를 개선하는 과정이다. 두 과정은 한쪽이 완전히 끝난 뒤에만 시작되는 것이 아니라 서로를 반복적으로 보완한다.

이론적으로 policy evaluation과 policy improvement가 모두 안정화되면 다음 두 조건이 동시에 만족된다.

1. 현재 value function은 현재 policy의 value를 올바르게 나타낸다.
2. 현재 policy는 그 value function에 대해 greedy하다.

그러면 value function은 Bellman optimality equation을 만족하고, policy는 optimal policy가 된다.

$$
v_*(s)
= \max_a\sum_{s',r}p(s',r \mid s,a)
\left[r+\gamma v_*(s')\right]
$$

따라서 많은 RL 알고리즘은 서로 다른 형태의 policy evaluation과 policy improvement를 번갈아 수행하는 GPI의 관점으로 설명할 수 있다. 다만 sample noise, 함수 근사, 유한한 학습 시간 등이 있으면 실제 학습에서는 정확한 optimal policy가 아니라 근사 optimal policy에 수렴할 수 있다.

## Monte Carlo method (MC)

Monte Carlo method는 tabular updating을 사용하는 model-free 방법이다. Environment의 transition model을 알지 못하므로 실제로 실행한 episode에서 얻은 sample return을 이용해 value function이나 Q function을 update한다.

MC는 episode가 끝난 뒤 전체 return $G_t$를 계산해야 하므로, 기본적으로 episodic task에서 사용한다.

### Episode-by-episode GPI

MC의 policy iteration은 episode-by-episode GPI의 형태로 이해할 수 있다.

1. 현재 policy $\pi$로 하나의 episode를 실행한다.
2. episode에서 얻은 return을 사용해 policy evaluation을 수행한다.
3. 업데이트된 $V$ 또는 $Q$를 기준으로 policy improvement를 수행한다.
4. 개선된 policy로 다음 episode를 실행하고 같은 과정을 반복한다.

즉, policy evaluation과 policy improvement가 모든 model의 branch를 대상으로 정확하게 수행되는 것이 아니라, 매 episode에서 얻은 sample을 통해 번갈아 근사된다. 이러한 구조가 episode-by-episode GPI이다.

### MC prediction (Policy Evaluation)

MC policy evaluation의 목표는 고정된 policy $\pi$의 action-value function을 학습하는 것이다.

$$
q_\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t=s,A_t=a]
$$

하지만 model-free RL에서는 이 expectation을 직접 계산하기 어렵다. 따라서 policy $\pi$로 실제 episode를 여러 번 실행하고, 각 episode에서 얻은 return의 **empirical mean**으로 $q_\pi(s,a)$를 근사한다.

$$
Q(s,a) \approx q_\pi(s,a)
$$

여기서 $q_\pi(s,a)$는 실제 expected action value이고, $Q(s,a)$는 sample data로 학습하는 추정값이다.

#### First-visit MC와 Every-visit MC

하나의 episode에서 같은 state-action pair $(s,a)$가 여러 번 등장할 수 있다.

- **First-visit MC**: 한 episode에서 $(s,a)$가 처음 등장했을 때의 return만 사용한다.
- **Every-visit MC**: 한 episode에서 $(s,a)$가 등장할 때마다 각 return을 모두 사용한다.

여러 episode에서 얻은 return을 모아 count와 total return을 관리하면 다음과 같이 empirical mean을 계산할 수 있다.

$$
n(s,a) \leftarrow n(s,a)+1
$$

$$
S(s,a) \leftarrow S(s,a)+G_t
$$

$$
Q(s,a) = \frac{S(s,a)}{n(s,a)}
$$

고정된 policy와 stationary environment에서 충분한 sample이 주어지고 필요한 state-action pair가 반복해서 방문되면, law of large numbers에 의해 empirical mean은 expected value $q_\pi(s,a)$에 수렴한다.

#### Incremental mean

모든 return을 저장하지 않고 평균을 online으로 update하기 위해 incremental mean을 사용할 수 있다. $k$개의 sample 평균을 $\mu_k$라고 하면,

$$
\begin{aligned}
\mu_k
&= \frac{1}{k}\sum_{i=1}^{k}x_i \\
&= \mu_{k-1}+\frac{1}{k}\left(x_k-\mu_{k-1}\right)
\end{aligned}
$$

이다. 새로운 sample $x_k$와 이전 평균 $\mu_{k-1}$만 사용하므로 과거의 모든 sample을 다시 저장하거나 합산할 필요가 없다.

이를 MC action-value update에 적용하면 다음과 같다. $n(s,a)$를 먼저 증가시킨 뒤의 count를 사용한다.

$$
n(S_t,A_t) \leftarrow n(S_t,A_t)+1
$$

$$
Q(S_t,A_t) \leftarrow Q(S_t,A_t)
+ \frac{1}{n(S_t,A_t)}
\left[G_t-Q(S_t,A_t)\right]
$$

#### Constant-$\alpha$ MC update

방문 횟수에 따라 step size가 $1/n(s,a)$로 줄어드는 대신, 고정된 learning rate $\alpha$를 사용할 수도 있다.

$$
Q(S_t,A_t) \leftarrow Q(S_t,A_t)
+ \alpha\left[G_t-Q(S_t,A_t)\right]
$$

고정된 $\alpha$를 사용하면 최근 episode의 return이 더 큰 비중으로 반영된다. 과거 sample의 영향은 반복 update를 거치면서 지수적으로 감소하므로, environment가 변하는 non-stationary 문제에 더 빠르게 적응할 수 있다.

### MC와 Markov property

MC는 Bellman equation처럼 현재 state에서 next state value를 이용해 target을 재귀적으로 만들지 않는다. 실제 episode에서 얻은 전체 return $G_t$를 사용하므로, **return prediction 자체는 Markov property가 완벽하게 성립하지 않아도 수행할 수 있다**.

다만 현재 관측값이 서로 다른 과거 상황을 구분하지 못하는 state aliasing이 있다면, 같은 state에 여러 상황의 return을 평균내게 된다. 이 경우 value estimate가 유용할 수는 있지만, 해당 관측값만으로 최적 policy를 보장할 수는 없다. 따라서 MC가 Markov property의 영향을 전혀 받지 않는다는 뜻은 아니며, Bellman 기반 방법보다 Markov 가정에 덜 직접적으로 의존한다는 의미로 이해하는 것이 정확하다.

### No bootstrapping과 bootstrapping

MC는 episode가 끝난 뒤 실제로 얻은 전체 return $G_t$를 target으로 사용한다.

$$
V(S_t) \leftarrow V(S_t)
+ \alpha\left[G_t-V(S_t)\right]
$$

여기서 $G_t$는 앞으로 받을 실제 reward들을 모두 합친 값이며, 현재 value estimate를 target의 일부로 사용하지 않는다. 이를 **no bootstrapping**이라고 한다.

반면 bootstrapping은 다음 state의 value estimate처럼 이미 현재 table이나 function approximator가 가지고 있는 추정값을 target에 포함하는 것이다.

$$
V(S_t) \leftarrow V(S_t)
+ \alpha\left[R_{t+1}+\gamma V(S_{t+1})-V(S_t)\right]
$$

Q-learning이나 SARSA에서는 다음과 같이 next state-action의 Q estimate를 사용할 수도 있다.

$$
Q(S_t,A_t) \leftarrow Q(S_t,A_t)
+ \alpha\left[R_{t+1}+\gamma Q(S_{t+1},A_{t+1})-Q(S_t,A_t)\right]
$$

정리하면 MC는 실제 미래 return $G_t$를 끝까지 기다려 update하는 no-bootstrapping 방법이고, TD 계열은 바로 다음 reward와 next value estimate를 이용해 update하는 bootstrapping 방법이다.

### Episodic task와 continuing task

- **Episodic task**: terminal state가 존재하며 episode가 유한한 시간 안에 종료되는 task이다. MC처럼 episode 전체의 return을 계산하는 방법을 적용하기 쉽다.
- **Continuing task**: terminal state가 없고 task가 계속 이어지는 task이다. 이론적으로 infinite horizon을 가지므로 episode 전체의 return을 바로 계산할 수 없다.

강의나 자료에 따라 continuing task를 continuous task라고 부르기도 하지만, 시간이나 action이 연속적이라는 뜻의 continuous와는 구분해야 한다. Continuing task에서는 TD처럼 episode가 끝나지 않아도 update할 수 있는 방법이 더 자연스럽다.

## MC Control: $\epsilon$-greedy policy improvement

MC policy evaluation으로 $Q(s,a)$를 추정한 뒤에는, 이 Q값을 이용해 policy를 개선할 수 있다. 이때 현재까지의 경험에서 가장 좋은 action만 선택하면 새로운 action을 시도할 기회를 잃을 수 있으므로 exploitation과 exploration을 함께 고려한다.

- **Exploitation**: 지금까지의 경험에서 가장 높은 Q값을 가진 action을 선택한다.
- **Exploration**: 아직 충분히 시도하지 않은 action도 선택하여 더 좋은 action을 발견할 기회를 만든다.

### $\epsilon$-greedy policy

가능한 action의 개수를 $m=|\mathcal{A}(s)|$라고 하자. $\epsilon$-greedy policy는 확률 $1-\epsilon$으로 greedy action을 선택하고, 확률 $\epsilon$으로 action을 uniform random하게 선택한다.

$$
\pi'(a \mid s) =
\begin{cases}
1-\epsilon+\dfrac{\epsilon}{m},
& a=\displaystyle\arg\max_{a'}Q^\pi(s,a') \\
\dfrac{\epsilon}{m},
& \text{otherwise}
\end{cases}
$$

Random action을 선택하는 과정에서 greedy action이 다시 선택될 수도 있기 때문에 greedy action의 최종 확률은 $1-\epsilon+\epsilon/m$이 된다. 나머지 $m-1$개 action은 각각 $\epsilon/m$의 확률을 가진다.

### $\epsilon$-greedy policy improvement

현재 policy $\pi$가 각 action을 최소 $\epsilon/m$의 확률로 선택하는 $\epsilon$-soft policy라고 하자. 새로운 policy $\pi'$는 $Q^\pi$에 대해 greedy한 action을 더 자주 선택한다.

새 policy에서 선택하는 action의 expected action value는 다음과 같다.

$$
\begin{aligned}
q_\pi(s,\pi'(s))
&= \sum_a\pi'(a\mid s)q_\pi(s,a) \\
&= \frac{\epsilon}{m}\sum_a q_\pi(s,a)
  +(1-\epsilon)\max_a q_\pi(s,a)
\end{aligned}
$$

Greedy action은 모든 action 중 Q값이 가장 크므로 다음 부등식이 성립한다.

$$
\begin{aligned}
q_\pi(s,\pi'(s))
&\geq \frac{\epsilon}{m}\sum_a q_\pi(s,a) \\
&\quad +(1-\epsilon)
\sum_a\frac{\pi(a\mid s)-\epsilon/m}{1-\epsilon}
q_\pi(s,a) \\
&= \sum_a\pi(a\mid s)q_\pi(s,a) \\
&= v_\pi(s)
\end{aligned}
$$

마지막 등식에서는 $\pi$에 따른 state value의 정의를 사용했다. 또한 $\pi$가 $\epsilon$-soft이므로 다음 가중치의 합은 1이다.

$$
\sum_a\frac{\pi(a\mid s)-\epsilon/m}{1-\epsilon}=1
$$

따라서 Policy Improvement Theorem에 의해

$$
v_{\pi'}(s)\geq v_\pi(s)\quad\text{for all }s\in\mathcal{S}
$$

가 성립한다. 즉, $\epsilon$-greedy policy improvement는 exploration을 유지하면서도 기존 policy보다 나쁘지 않은 policy를 만든다. MC Control은 MC sample로 $Q^\pi$를 평가한 뒤 이 $\epsilon$-greedy policy improvement를 반복하는 방식이다.

## GLIE MC Control

MC Control의 learning policy가 optimal policy로 수렴하기 위해서는 **GLIE(Greedy in the Limit with Infinite Exploration)** 조건을 만족시키는 것이 중요하다.

GLIE는 다음 두 조건을 의미한다.

1. **Infinite exploration**: 모든 state-action pair가 무한히 자주 방문되어야 한다.

$$
\lim_{k\to\infty}n_k(s,a)=\infty
\quad\text{for all }(s,a)
$$

단순히 episode의 개수가 무한하다는 것만으로는 충분하지 않다. 특정 state-action pair가 계속 선택되지 않는다면 그 pair의 Q값은 충분히 학습되지 않는다.

2. **Greedy in the limit**: 학습이 진행될수록 policy가 Q값이 가장 큰 action을 선택하는 greedy policy에 가까워져야 한다.

$$
\lim_{k\to\infty}\pi_k(a\mid s)=1
\quad\text{if }a\in\arg\max_{a'}Q_k(s,a')
$$

$\epsilon_k$-greedy policy를 사용한다면 보통 다음 조건을 만족하도록 $\epsilon_k$를 설정한다.

$$
\epsilon_k\to 0
$$

예를 들어 다음과 같이 둘 수 있다.

$$
\epsilon_k=\frac{1}{k},
\qquad
\pi_k\leftarrow\epsilon_k\text{-greedy}(Q_k)
$$

이 경우 학습 초반에는 $\epsilon_k$가 비교적 커서 exploration을 수행하고, 학습이 진행될수록 $\epsilon_k$가 작아져 greedy action을 더 자주 선택한다. 동시에 $\sum_k\epsilon_k=\infty$인 조건을 만족하면 exploration이 충분히 오래 지속될 수 있다.

MC Control에서 사용하는 sample-average update는 다음과 같다.

$$
n(S_t,A_t)\leftarrow n(S_t,A_t)+1
$$

$$
Q(S_t,A_t)\leftarrow Q(S_t,A_t)
+\frac{1}{n(S_t,A_t)}
\left[G_t-Q(S_t,A_t)\right]
$$

유한한 MDP, bounded reward, 충분한 방문 횟수, 적절한 sample-average 조건 등을 가정하면 GLIE MC Control은 다음과 같이 수렴한다.

$$
Q_k(s,a)\longrightarrow q_*(s,a)
$$

따라서 최종 policy는 $q_*(s,a)$가 가장 큰 action을 선택하는 optimal policy로 수렴한다.

## MC Control algorithm

MC Control은 episode를 생성하고, episode의 return으로 $Q$를 평가한 뒤, $\epsilon$-greedy policy improvement를 수행한다.

{% capture mc_control_algorithm %}
$$
\begin{array}{l}
\textbf{Initialize }Q(s,a)\text{ arbitrarily for all }s\in\mathcal{S},a\in\mathcal{A}(s),\text{ except }Q(\text{terminal},\cdot)=0 \\
\quad\quad \textit{Returns}(s,a)\leftarrow\text{empty list} \\
\quad\quad \pi\leftarrow\text{arbitrary }\epsilon\text{-soft policy} \\
\textbf{Repeat forever for each episode:} \\
\quad\quad \textbf{Generate an episode using }\pi:\quad S_0,A_0,R_1,\ldots,S_{T-1},A_{T-1},R_T \\
\quad\quad G\leftarrow0 \\
\quad\quad \textbf{For }t=T-1,T-2,\ldots,0\textbf{:} \\
\quad\quad\quad\quad G\leftarrow\gamma G+R_{t+1} \\
\quad\quad\quad\quad \textbf{If }(S_t,A_t)\text{ is the first visit in this episode:} \\
\quad\quad\quad\quad\quad\quad \textit{Returns}(S_t,A_t)\leftarrow\textit{Returns}(S_t,A_t)\cup\{G\} \\
\quad\quad\quad\quad\quad\quad Q(S_t,A_t)\leftarrow\operatorname{average}(\textit{Returns}(S_t,A_t)) \\
\quad\quad \textbf{For each }S_t\text{ in the episode:} \\
\quad\quad\quad\quad A^*\leftarrow\operatorname*{arg\,max}_a Q(S_t,a) \\
\quad\quad\quad\quad \textbf{For each }a\in\mathcal{A}(S_t)\textbf{:} \\
\quad\quad\quad\quad\quad\quad \pi(a\mid S_t)\leftarrow
\begin{cases}
1-\epsilon+\dfrac{\epsilon}{|\mathcal{A}(S_t)|}, & a=A^* \\
\dfrac{\epsilon}{|\mathcal{A}(S_t)|}, & \text{otherwise}
\end{cases}
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Algorithm 1. Monte Carlo Control" label="algorithm:monte-carlo-control" math=mc_control_algorithm %}

알고리즘에서 episode를 뒤에서부터 순회하며 $G$를 계산하고, 각 state-action pair의 $Q$를 update하는 부분이 **MC policy evaluation**이다. 이후 현재 $Q$가 가장 큰 action을 greedy action으로 정하고 $\epsilon$-greedy 확률을 다시 설정하는 부분이 **policy improvement**이다.

Return의 평균은 두 가지 방식 중 하나를 선택해 계산할 수 있다.

- **Sample-average incremental update**:

$$
Q(S_t,A_t)\leftarrow Q(S_t,A_t)
+\frac{1}{n(S_t,A_t)}\left[G_t-Q(S_t,A_t)\right]
$$

- **Constant-$\alpha$ update**:

$$
Q(S_t,A_t)\leftarrow Q(S_t,A_t)
+\alpha\left[G_t-Q(S_t,A_t)\right]
$$

Sample-average 방식은 지금까지의 return을 동일한 비중으로 평균내고, constant-$\alpha$ 방식은 최근 return에 더 큰 가중치를 준다.

## Temporal Difference Learning (TD)

Temporal Difference(TD) learning은 tabular updating을 사용하는 model-free 방법이다. Environment의 transition probability를 알지 못한 채 실제 sample transition을 이용해 value function이나 Q function을 update한다.

TD policy iteration도 GPI의 한 형태로 볼 수 있다. 다만 MC처럼 episode 전체를 기다리지 않고, sample episode에서 얻은 **one-step transition**을 이용해 policy evaluation과 policy improvement를 반복한다.

### TD update와 이점

State-value function의 TD update는 다음과 같다.

$$
V(S_t)\leftarrow V(S_t)
+\alpha\left[R_{t+1}+\gamma V(S_{t+1})-V(S_t)\right]
$$

TD의 target은

$$
R_{t+1}+\gamma V(S_{t+1})
$$

이다. TD는 다음 두 가지 특성을 결합한다.

- **DP의 bootstrapping**: episode가 끝날 때까지 실제 final return을 기다리지 않고, 현재 추정한 next-state value를 이용해 update한다. 따라서 online update가 가능하다.
- **MC의 sampling**: transition probability를 모두 알 필요 없이 실제 environment에서 관측한 sample만 사용한다. 따라서 model-free 방식으로 동작한다.

### SARSA와 Q-learning 비교

| 구분 | SARSA | Q-learning |
| --- | --- | --- |
| Target policy | behavior policy와 동일한 policy | greedy target policy |
| Behavior policy | 보통 $\epsilon$-greedy | 보통 $\epsilon$-greedy |
| 실제 다음 action | $A_{t+1}$을 선택하고 update에 사용 | 다음 interaction을 위해 선택하지만 target에는 사용하지 않음 |
| Update target | $R_{t+1}+\gamma Q(S_{t+1},A_{t+1})$ | $R_{t+1}+\gamma\max_{a'}Q(S_{t+1},a')$ |
| Policy 유형 | On-policy TD prediction | Off-policy TD prediction |

여기서 $\alpha$는 constant learning rate이다.

### On-policy와 Off-policy

강화학습에서는 policy를 두 가지 관점으로 나눌 수 있다.

- **Target policy $\pi$**: 학습하거나 평가하려는 policy이다. $q_\pi$는 target policy $\pi$를 따랐을 때의 action-value function이고, $Q^\pi$는 이를 추정한 값이다.
- **Behavior policy $\mu$**: 실제 environment에서 action을 선택하여 sample을 생성하는 policy이다.

#### On-policy

On-policy 방법에서는 target policy와 behavior policy가 같다.

$$
\pi=\mu
$$

SARSA는 현재 policy가 실제로 선택한 다음 action을 target에 사용한다.

$$
Q(S_t,A_t)\leftarrow Q(S_t,A_t)
+\alpha\left[R_{t+1}+\gamma Q(S_{t+1},A_{t+1})-Q(S_t,A_t)\right]
$$

따라서 SARSA는 $(S_t,A_t,R_{t+1},S_{t+1},A_{t+1})$의 다섯 정보를 사용한다. $A_{t+1}$은 behavior policy이자 target policy인 현재 policy에서 실제로 선택된 action이다.

#### Off-policy

Off-policy 방법에서는 target policy와 behavior policy가 다르다.

$$
\pi\neq\mu
$$

Q-learning은 behavior policy가 어떤 next action을 선택했는지와 관계없이, target policy가 선택할 수 있는 action 중 가장 큰 Q값을 target으로 사용한다.

$$
Q(S_t,A_t)\leftarrow Q(S_t,A_t)
+\alpha\left[R_{t+1}+\gamma\max_{a'}Q(S_{t+1},a')-Q(S_t,A_t)\right]
$$

여기서 $\max_{a'}Q(S_{t+1},a')$는 $S_{t+1}$에서 가능한 action들의 현재 Q estimate 중 최댓값이다. Q-learning에서 실제 environment와 상호작용하며 다음 action을 선택할 때는 behavior policy $\mu$, 예를 들어 $\epsilon$-greedy policy를 사용한다. 하지만 이 실제로 선택된 action은 Q-learning의 target 계산에는 사용되지 않고, target에는 greedy한 최댓값이 사용된다.

반대로 SARSA에서는 behavior policy가 선택한 실제 다음 action $A_{t+1}$을 그대로 target에 사용한다. 따라서 SARSA에서는 behavior policy와 target policy가 같은 $\epsilon$-greedy policy이고, Q-learning에서는 behavior policy와 greedy target policy가 다르다.

#### 과거 sample의 재사용

On-policy 방법은 sample을 생성한 policy와 학습하려는 policy가 같아야 하므로, policy가 크게 바뀐 뒤에는 과거 sample이 현재 policy를 반영하지 않을 수 있다. 따라서 과거 경험을 그대로 재사용하기 어렵고, 필요하다면 importance sampling 등의 보정이 필요하다.

Off-policy 방법은 behavior policy $\mu$가 만든 sample로도 target policy $\pi$를 학습할 수 있다. 따라서 replay buffer에 저장된 과거 experience나 다른 policy가 수집한 data를 재사용하기 쉽다. 다만 off-policy라고 해서 $\max$가 과거에 취했던 action들을 직접 고려한다는 뜻은 아니다. 현재 next state에서 가능한 action들의 Q값을 비교해 target을 정한다는 의미이다.

On-policy가 항상 suboptimal policy라는 뜻도 아니다. 학습 중 exploration 때문에 현재 behavior policy가 일시적으로 최적이 아닐 수 있지만, 적절한 조건과 충분한 학습이 주어지면 on-policy 방법도 optimal policy로 수렴할 수 있다.

#### SARSA

SARSA는 $(S_t,A_t,R_{t+1},S_{t+1},A_{t+1})$의 다섯 요소를 사용한다. 즉, 현재 policy가 실제로 선택한 next action $A_{t+1}$을 target에 사용한다.

$$
Q(S_t,A_t)\leftarrow Q(S_t,A_t)
+\alpha\left[R_{t+1}+\gamma Q(S_{t+1},A_{t+1})-Q(S_t,A_t)\right]
$$

![SARSA backup](/assets/img/blog/deep-reinforcement-learning-summary-3/sarsa-backup.png)

SARSA는 behavior policy와 target에 사용하는 policy가 같으므로 **on-policy** 방법이다. $\epsilon$-greedy policy를 사용하면 exploration으로 실제 선택된 $A_{t+1}$이 그대로 update에 반영된다.

{% capture sarsa_algorithm %}
$$
\begin{array}{l}
\textbf{Initialize }Q(s,a)\text{ arbitrarily for all }s\in\mathcal{S},a\in\mathcal{A}(s),\text{ except }Q(\text{terminal},\cdot)=0 \\
\textbf{Repeat for each episode:} \\
\quad\quad \text{Initialize }S \\
\quad\quad \text{Choose }A\text{ from }S\text{ using a policy derived from }Q\text{, e.g. }\epsilon\text{-greedy} \\
\quad\quad \textbf{Repeat for each step:} \\
\quad\quad\quad\quad \text{Take action }A;\text{ observe }R,S' \\
\quad\quad\quad\quad \text{Choose }A'\text{ from }S'\text{ using a policy derived from }Q \\
\quad\quad\quad\quad Q(S,A)\leftarrow Q(S,A)+\alpha\left[R+\gamma Q(S',A')-Q(S,A)\right] \\
\quad\quad\quad\quad S\leftarrow S';\quad A\leftarrow A' \\
\quad\quad \textbf{Until }S\text{ is terminal}
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Algorithm 2. SARSA" label="algorithm:sarsa" math=sarsa_algorithm %}

#### Q-learning

Q-learning은 next state에서 실제로 어떤 action이 선택되었는지와 관계없이, 가능한 action 중 가장 큰 Q값을 target으로 사용한다.

$$
Q(S_t,A_t)\leftarrow Q(S_t,A_t)
+\alpha\left[R_{t+1}+\gamma\max_{a'}Q(S_{t+1},a')-Q(S_t,A_t)\right]
$$

![Q-learning backup](/assets/img/blog/deep-reinforcement-learning-summary-3/q-learning-backup.png)

Q-learning은 behavior policy가 $\epsilon$-greedy여도 target은 greedy action을 사용한다. 따라서 behavior policy와 target policy가 다를 수 있어 **off-policy** 방법이다.

{% capture q_learning_algorithm %}
$$
\begin{array}{l}
\textbf{Initialize }Q(s,a)\text{ arbitrarily for all }s\in\mathcal{S},a\in\mathcal{A}(s),\text{ except }Q(\text{terminal},\cdot)=0 \\
\textbf{Repeat for each episode:} \\
\quad\quad \text{Initialize }S \\
\quad\quad \textbf{Repeat for each step:} \\
\quad\quad\quad\quad \text{Choose }A\text{ from }S\text{ using a policy derived from }Q\text{, e.g. }\epsilon\text{-greedy} \\
\quad\quad\quad\quad \text{Take action }A;\text{ observe }R,S' \\
\quad\quad\quad\quad Q(S,A)\leftarrow Q(S,A)+\alpha\left[R+\gamma\max_{a'}Q(S',a')-Q(S,A)\right] \\
\quad\quad\quad\quad S\leftarrow S' \\
\quad\quad \textbf{Until }S\text{ is terminal}
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Algorithm 3. Q-learning" label="algorithm:q-learning" math=q_learning_algorithm %}

## 참고 강의

- [고려대 오승상 강화학습 10 — Reinforcement Learning](https://www.youtube.com/watch?v=NH3lKBzXBUA)
- [고려대 오승상 강화학습 11 — Monte Carlo method 1](https://www.youtube.com/watch?v=eibrMjPEAMg)
- [고려대 오승상 강화학습 12 — Monte Carlo method 2](https://www.youtube.com/watch?v=TF63tYx-fdk)
- [고려대 오승상 강화학습 13 — Temporal Difference Learning 1](https://www.youtube.com/watch?v=5Vbn4XoE45w)
- [고려대 오승상 강화학습 14 — Temporal Difference Learning 2](https://www.youtube.com/watch?v=1BcEwmxSr8E)
- [고려대 오승상 강화학습 15 — Temporal Difference Learning 3](https://www.youtube.com/watch?v=g7JnA_ArmOU)
