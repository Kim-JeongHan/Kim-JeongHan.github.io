---
layout: post
title: Reinforcement Learning 5 - Policy Gradient, REINFORCE, Actor-Critic
date: 2026-08-28 00:00:00 +0900
slug: deep-reinforcement-learning-summary-5
render_with_liquid: true
use_math: true
categories:
- 공부
- 강화학습
tags:
- reinforcement-learning
- policy-gradient
---

## 00_Policy Gradient 개요

Policy Gradient는 value function에서 policy를 간접적으로 찾는 대신, policy 자체를 neural network로 표현하고 policy parameter를 직접 update하는 방법이다.

### Policy Gradient를 사용하는 이유

DQN은 state space가 크거나 연속적이어도 neural network로 처리할 수 있지만, 출력층에서 action별 Q-value를 계산하므로 기본적으로 discrete action space를 전제로 한다. Continuous action space에서는 가능한 action의 개수가 무한하므로 모든 action의 Q-value를 출력하기 어렵다.

Policy Gradient는 state를 입력으로 받아 action distribution을 직접 출력한다. 따라서 discrete action뿐 아니라 continuous action도 확률분포로 표현하여 sampling할 수 있다.

- **Discrete action**: action별 확률 또는 score를 출력한다.
- **Continuous action**: action dimension마다 Gaussian distribution의 mean과 variance 등을 출력하고, 그 분포에서 action을 sampling한다.

또한 DQN은 Q function을 학습한 뒤 $\epsilon$-greedy로 action을 선택하지만, Policy Gradient는 policy network가 정의한 distribution에서 action을 직접 선택한다.

{% capture quadruped_action_callout %}
사족보행 로봇의 한 state에서 네 다리의 관절 torque를 제어한다고 생각해 보자.

- **Action space**: 로봇이 선택할 수 있는 모든 action의 집합이다. 예를 들어 12개의 관절 torque를 연속적으로 제어한다면
  $$
  \mathcal{A}=[-1,1]^{12}
  $$
  와 같이 표현할 수 있다.
- **Action**: 현재 time step에서 실제로 선택한 하나의 값이다.
  $$
  a_t=(\tau_1,\tau_2,\ldots,\tau_{12})
  $$
- **Action value**: 현재 state $s_t$에서 특정 action $a_t$를 수행한 뒤 policy를 따랐을 때 얻을 expected return이다.
  $$
  Q^\pi(s_t,a_t)=\mathbb{E}_\pi[G_t\mid S_t=s_t,A_t=a_t]
  $$

즉, action space는 **선택 가능한 전체 범위**, action은 그중 **이번에 실제로 선택한 하나의 제어 입력**, action value는 그 action을 선택했을 때의 **장기적인 성능 평가값**이다.

DQN은 discrete action마다 Q-value를 출력해야 하므로, 12개 관절의 torque를 각각 여러 단계로 discretize하면 가능한 action 조합이 급격히 증가한다. Policy Gradient는 12개 action dimension 각각의 distribution을 직접 출력하고 그 안에서 action을 sampling할 수 있어 이런 continuous control에 더 자연스럽게 대응한다.
{% endcapture %}

{% include callout.html type="idea" title="사족보행 로봇으로 이해하는 Action" content=quadruped_action_callout %}

### DQN vs Policy Gradient

| 구분 | DQN | Policy Gradient |
| --- | --- | --- |
| 대표 사용 사례 | Atari: CNN + Q-learning | AlphaGo: Policy Gradient + MCTS |
| 직접 학습하는 대상 | $Q(s,a)$ 또는 $Q_\theta(s,a)$ | policy $\pi_\theta(a\mid s)$ |
| 최적화 방향 | Bellman target과의 Q-value 오차를 줄이는 gradient descent | expected total reward $J(\theta)$를 직접 maximize하는 gradient ascent |
| Action 선택 | $\arg\max_a Q(s,a)$ 또는 $\epsilon$-greedy | policy distribution에서 action을 직접 sampling |
| Continuous action | 기본 DQN에서는 어려움 | action distribution으로 표현 가능 |
| Policy 획득 | 학습한 Q-value에서 greedy policy를 간접적으로 추출 | policy network가 optimal policy를 직접 학습 |
| Replay buffer | DQN의 안정적인 학습에 주로 사용 | 필수는 아님. 새 on-policy trajectory 사용 |
| 구현 난이도 | target network, replay buffer 등 필요 | 구조는 비교적 단순하지만 variance가 큼 |
{: .policy-comparison-table}

DQN은 Q-value를 Bellman equation의 target에 맞게 update한 뒤, 가장 큰 Q-value를 갖는 action을 선택한다. 반면 Policy Gradient는 policy network의 parameter를 직접 update하여 expected total reward가 커지는 방향으로 policy를 학습한다.

기본 Policy Gradient는 episode에서 얻은 total reward 또는 return을 사용하므로 DQN과 같은 replay buffer가 필수는 아니다. 다만 현재 policy가 생성한 on-policy trajectory를 minibatch로 묶어 계산할 수 있으며, PPO처럼 rollout data를 여러 minibatch update에 사용하는 방법도 있다.

일반적으로 Policy Gradient의 기본 구현은 DQN보다 단순하지만, sample variance가 커서 학습이 불안정할 수 있다. 이 문제를 줄이기 위해 baseline, Actor-Critic, advantage estimation 등의 기법이 추가된다.

### 기본 notation

policy gradient는 policy $\pi_\theta(a\mid s)$를 neural network로 표현하고, policy parameter $\theta$를 직접 update하는 방법이다. Policy Gradient의 notation은 다음과 같다.
- $ \pi_\theta(a\mid s) =P(A_t=a\mid S_t=s;\theta) $ : network 파라미터를 사용한 policy가 state $s$에서 action $a$를 선택할 확률

- $ \tau=(S_0,A_0,R_1,S_1,A_1,\ldots,S_T) $ : trajectory, 즉 episode에서 생성된 state, action, reward의 sequence

-  $ r(\tau)=G_0 =\sum_{t=0}^{T-1}\gamma^tR_{t+1} $ : trajectory $\tau$에서 얻은 discounted total return

## 01_목적 함수와 Policy Update

### Expected return

이를 위해, policy gradient는 다음과 같은 objective function을 정의하고, 이를 최대화하는 방향으로 policy parameter $\theta$를 update한다.

$$
J(\theta)
=\mathbb{E}_{\tau\sim\pi_\theta}[r(\tau)]
$$

### Gradient ascent

Objective function $J(\theta)$는 expected total reward이므로, 이를 최대화하기 위해 gradient ascent를 사용한다.

$$
\theta\leftarrow\theta+\alpha\nabla_\theta J(\theta)
$$

여기서 $\alpha$는 gradient ascent의 step size이다.

### Trajectory distribution 표현

Objective function을 미분하기 위해 우리는 먼저 $ J(\theta)$를 trajectory distribution $p(\tau;\theta)$를 이용해 표현한다.

$$
\text{Continuous trajectory:}\qquad
J(\theta)=\int p(\tau;\theta)r(\tau)\,d\tau
$$

$$
\text{Discrete trajectory:}\qquad
J(\theta)=\sum_\tau p(\tau;\theta)r(\tau)
$$

이중 우리는 주로 continous trajectory로 문제를 다루겠다. 이제 objective funcnction을 다시 써보면 아래와 같은 형태가 된다.

$$
\nabla_\theta J(\theta)
=\nabla_\theta\int p(\tau;\theta)r(\tau)\,d\tau
$$

문제는 trajectory의 reward $r(\tau)$뿐 아니라 trajectory가 생성될 확률 $p(\tau;\theta)$도 policy parameter $\theta$에 의존한다는 점이다. 따라서 objective function의 expectation을 어떻게 미분할지에 대한 추가적인 방법이 필요하다. 이때 사용되는 것이 바로 **Policy Gradient Theorem**이다.

## 02_Policy Gradient Theorem

Policy Gradient Theorem은 expected return의 gradient를 trajectory reward와 policy의 log-probability gradient의 곱에 대한 expectation으로 바꾸어 표현하여 gradient를 계산할 수 있도록 한다. Policy Gradient Theorem은 다음과 같이 표현된다.

$$
\nabla_\theta J(\theta)
= \mathbb{E}_{\tau\sim\pi_\theta}
\left[
r(\tau)\sum_{t=0}^{T-1}
\nabla_\theta\log\pi_\theta(A_t\mid S_t)
\right]
$$

위의 결과를 얻기 위한 과정을 하나씩 살펴보자.

### 1. Log-derivative trick

먼저 objective function을 trajectory probability를 이용해 표현한다.

$$
J(\theta)=\int p(\tau;\theta)r(\tau)\,d\tau
$$

objective function을 미분하고 이를 적분 안으로 넣으면 다음과 같이 쓸 수 있다.

$$
\nabla_\theta J(\theta)
=\int \nabla_\theta p(\tau;\theta)r(\tau)\,d\tau
$$

이중 gradient $\nabla_\theta p(\tau;\theta)$를 log-probability의 gradient로 바꾸기 위해 log의 미분 결과를 먼저 확인한다. $p(\tau;\theta)>0$인 경우,

$$
\nabla_\theta\log p(\tau;\theta)
=\frac{\nabla_\theta p(\tau;\theta)}{p(\tau;\theta)}
$$

양변에 $p(\tau;\theta)$를 곱하면 원하는 identity를 얻을 수 있다. 이를 분수를 곱하는 형태로 쓰면,

$$
\begin{aligned}
\nabla_\theta p(\tau;\theta)
&=\nabla_\theta p(\tau;\theta)
  \frac{p(\tau;\theta)}{p(\tau;\theta)} \\
&=p(\tau;\theta)
  \frac{\nabla_\theta p(\tau;\theta)}{p(\tau;\theta)} \\
&=p(\tau;\theta)\nabla_\theta\log p(\tau;\theta)
\end{aligned}
$$

그러면

$$
\begin{aligned}
\nabla_\theta J(\theta)
&=\int p(\tau;\theta)r(\tau)
\nabla_\theta\log p(\tau;\theta)\,d\tau \\
&=\mathbb{E}_{\tau\sim\pi_\theta}
\left[r(\tau)\nabla_\theta\log p(\tau;\theta)\right]
\end{aligned}
$$

이처럼 확률의 gradient를 log-probability의 gradient로 바꾸는 과정을 log-derivative trick이라고 한다.

### 2. Trajectory probability의 분해

$$ p(\tau;\theta) = p(s_0)p(a_0\mid s_0)p(s_1\mid s_0,a_0)\cdots p(a_{T-1}\mid s_{T-1}, a_{T-2}, \cdots s_0,a_0)p(s_T\mid s_{T-1},a_{T-1}, \cdots , s_0,a_0) $$
$p(\tau;\theta)$는 initial state distribution, policy, environment transition의 곱으로 분해된다. 이때 Markov property를 이용하면 마지막 항을 단순화할수 있다.

<!-- callout -->

{% capture markov_property_callout %}
MDP의 Markov property에 의해 다음 state의 확률은 전체 과거가 아니라 현재 state와 action에만 의존한다.

$$
p(s_{t+1}\mid s_0,a_0,\ldots,s_t,a_t)
=p(s_{t+1}\mid s_t,a_t)
$$
{% endcapture %}

{% include callout.html type="note" title="Markov property" content=markov_property_callout %}

따라서 trajectory probability는 initial state distribution, policy, environment transition의 곱으로 분해된다.

$$
p(\tau;\theta)
=p(s_0)
\prod_{t=0}^{T-1}
\pi_\theta(a_t\mid s_t)
p(s_{t+1}\mid s_t,a_t)
$$

이제 이렇게 분해된 trajectory probability를 log-derivative trick 결과에 적용한다.

### 3. Log probability의 gradient

Trajectory probability에 log를 취하면 곱이 합으로 바뀐다.

$$
\log p(\tau;\theta)
=\log p(s_0)
+\sum_{t=0}^{T-1}
\left[
\log\pi_\theta(a_t\mid s_t)
+\log p(s_{t+1}\mid s_t,a_t)
\right]
$$

Initial state distribution과 environment transition은 policy parameter $\theta$와 관계없이 고정되어 있다. 따라서 이 두 항의 gradient는 0이고, policy 항만 남는다.

$$
\nabla_\theta\log p(\tau;\theta)
=\sum_{t=0}^{T-1}
\nabla_\theta\log\pi_\theta(a_t\mid s_t)
$$

이를 log-derivative 결과에 대입하면 Policy Gradient Theorem을 얻는다.

$$
\nabla_\theta J(\theta)
=\mathbb{E}_{\tau\sim\pi_\theta}
\left[
r(\tau)\sum_{t=0}^{T-1}
\nabla_\theta\log\pi_\theta(a_t\mid s_t)
\right]
$$

실제로는 expectation을 직접 계산할 수 없으므로 $N$개의 sample trajectory를 사용해 다음과 같이 근사한다.

$$
{\nabla_\theta J(\theta)}
=\frac{1}{N}\sum_{i=1}^{N}
r(\tau_i)
\sum_{t=0}^{T_i-1}
\nabla_\theta\log\pi_\theta(a_t^{(i)}\mid s_t^{(i)})
$$

이 sample gradient를 이용해 gradient ascent를 수행하면 policy가 높은 expected return을 만드는 방향으로 update된다.

### Policy Gradient Theorem의 의미와 장점

Policy Gradient Theorem을 사용하면 다음과 같은 장점이 있다.

1. **Trajectory probability를 알 필요가 없음**: $p(\tau;\theta)$를 직접 계산하거나 미분하지 않고, policy가 선택한 action의 log-probability gradient만 사용한다.
2. **Environment transition model을 알 필요가 없음**: $p(s_{t+1}\mid s_t,a_t)$를 명시적으로 알지 못해도 실제 environment와 상호작용하여 얻은 sample trajectory로 학습할 수 있다. 특히 continuous state나 action space에서는 모든 transition probability를 계산하는 것이 어렵기 때문에 중요한 장점이다.
3. **Expectation을 sample로 근사 가능**: Policy Gradient Theorem의 expectation은 여러 trajectory로 구성된 minibatch의 평균으로 계산할 수 있다.

$$
\mathbb{E}_{\tau\sim\pi_\theta}[f(\tau)]
\approx \frac{1}{N}\sum_{i=1}^{N}f(\tau_i)
$$

따라서 policy gradient를 계산하기 위해 trajectory distribution 전체를 알 필요 없이, policy로부터 sample trajectory를 생성하고 그 결과를 minibatch로 묶어 update하면 된다.

## 03_REINFORCE

### Monte Carlo Policy Gradient

REINFORCE는 가장 대표적인 Monte Carlo policy gradient 알고리즘이다. Policy Gradient Theorem의 expectation을 실제로 생성한 sample trajectory들의 평균으로 근사하고, 각 action 이후에 얻은 discounted return $G_t$를 policy gradient의 weight로 사용한다.

### REINFORCE의 학습 절차

1. 현재 policy $\pi_\theta$를 사용해 $M$개의 trajectory를 생성한다.
2. 각 trajectory에서 time step $t$ 이후의 discounted return $G_t^{(i)}$를 계산한다.
3. $M$개 trajectory의 return과 log-policy gradient를 이용해 policy gradient를 근사한다.
4. gradient ascent로 policy parameter $\theta$를 update한다.

### Gradient estimate

실제 sample을 이용한 gradient estimate는 다음과 같다.

$$
g_\theta
:=\frac{1}{M}\sum_{i=1}^{M}
\sum_{t=0}^{T_i-1}
G_t^{(i)}\nabla_\theta\log\pi_\theta
\left(a_t^{(i)}\mid s_t^{(i)}\right)
\approx \nabla_\theta J(\theta)
$$

계산한 gradient를 이용해 policy를 다음과 같이 update한다.

$$
\theta\leftarrow\theta+\alpha g_\theta
\approx\theta+\alpha\nabla_\theta J(\theta)
$$

### REINFORCE의 한계

REINFORCE는 trajectory가 끝난 뒤 얻은 return을 사용하므로 Monte Carlo 방법이며, next-state value estimate를 target에 사용하는 bootstrapping은 하지 않는다. 대신 전체 episode의 결과가 각 action의 gradient에 영향을 주므로 gradient estimate의 variance가 커질 수 있다.

## 04_REINFORCE with Baseline

### Bias–Variance Trade-off와 Baseline

REINFORCE는 실제 episode의 return $G_t$를 사용하므로 target에 대한 bias는 작지만, stochastic policy와 stochastic environment에서 여러 trajectory의 return이 크게 달라질 수 있어 gradient estimate의 variance가 높다. 반대로 TD처럼 next-state value estimate를 사용하면 variance는 줄어들 수 있지만 bootstrapping으로 인한 bias가 생길 수 있다.

| 방법 | Bias | Variance |
| --- | --- | --- |
| Monte Carlo / REINFORCE | 낮음 또는 없음 | 높음 |
| Temporal Difference | 있음 | 낮음 |

REINFORCE의 높은 variance를 줄이기 위해 total return에 **baseline**을 뺄 수 있다. Baseline은 보통 현재 state의 value function $b(s_t)=V^\pi(s_t)$를 사용한다.

$$
\nabla_\theta J(\theta)
\approx \frac{1}{M}\sum_{i=1}^{M}
\sum_{t=0}^{T_i-1}
\left[G_t^{(i)}-b(s_t^{(i)})\right]
\nabla_\theta\log\pi_\theta
\left(a_t^{(i)}\mid s_t^{(i)}\right)
$$

이때

$$
A^\pi(s_t,a_t)=G_t-V^\pi(s_t)
$$

는 해당 action이 state의 평균적인 value보다 얼마나 좋은지를 나타내는 advantage의 sample estimate로 볼 수 있다. Baseline이 action 자체에 의존하지 않으면 policy gradient의 기대값은 바뀌지 않고, return의 변동만 줄이는 방향으로 작동한다.

### Baseline이 bias를 만들지 않는 이유

Baseline을 추가한 policy gradient에서는 basline의 expectation이 0임을 보여야지, basline추가가 bias를 만들지 않는다는 것을 증명할 수 있다. Baseline이 action과 무관하므로 expectation을 계산할 때 이를 분리해서 쓰면 다음과 같다.

$$
\mathbb{E}_{a_t\sim\pi_\theta(\cdot\mid s_t)}
\left[b(s_t)\nabla_\theta\log\pi_\theta(a_t\mid s_t)\right]
$$

해당 수식의 expectation을 summation으로 바꾼뒤, a_t와 무관한 baseline $b(s_t)$를 밖으로 빼면 쉽게 정리가 가능하다.

$$
\begin{aligned}
&\mathbb{E}_{a_t\sim\pi_\theta(\cdot\mid s_t)}
\left[b(s_t)\nabla_\theta\log\pi_\theta(a_t\mid s_t)\right] \\
&=\sum_{a_t}\pi_\theta(a_t\mid s_t)b(s_t)
\nabla_\theta\log\pi_\theta(a_t\mid s_t) \\
&=b(s_t)\sum_{a_t}\pi_\theta(a_t\mid s_t)
\frac{\nabla_\theta\pi_\theta(a_t\mid s_t)}
{\pi_\theta(a_t\mid s_t)} \\
&=b(s_t)\sum_{a_t}\nabla_\theta\pi_\theta(a_t\mid s_t) \\
&=b(s_t)\nabla_\theta\sum_{a_t}\pi_\theta(a_t\mid s_t) \\
&=b(s_t)\nabla_\theta 1 \\
&=0
\end{aligned}
$$

따라서 baseline을 뺀 gradient의 expectation은 기존 gradient와 동일하다.

$$
\mathbb{E}\left[(G_t-b(s_t))
\nabla_\theta\log\pi_\theta(a_t\mid s_t)\right]
=\mathbb{E}\left[G_t
\nabla_\theta\log\pi_\theta(a_t\mid s_t)\right]
$$

즉, action과 무관한 baseline은 gradient의 평균 방향을 바꾸지 않으면서 sample별 값의 변동을 줄여 variance를 낮춘다. Continuous action space에서는 위의 action summation이 probability density에 대한 integral로 바뀌지만, density의 적분이 1이라는 같은 원리가 적용된다.

### State-value function을 baseline으로 사용하는 이유

좋은 baseline은 action과는 관련이 없고 현재 state와는 관련이 있어야 한다. Baseline이 action에 의존하면 policy gradient의 기대값을 바꿀 수 있어 bias가 발생할 수 있지만, state에만 의존하는 baseline은 gradient의 기대값을 바꾸지 않으면서 variance를 줄일 수 있다.

State-value function은 현재 state에서 policy를 따랐을 때 얻는 return의 expectation이므로 baseline으로 사용하기 적절하다.

$$
V^\pi(s)=\mathbb{E}_\pi[G_t\mid S_t=s]
$$

따라서 REINFORCE에서는 다음과 같이 state-value function을 baseline으로 사용한다.

$$
\delta_t=G_t-V(S_t;\phi)
$$

$\delta_t$는 실제 return이 현재 state의 value estimate보다 얼마나 큰지를 나타내는 값이며, advantage의 sample estimate로 볼 수 있다.

### Actor와 Critic 구조

REINFORCE with baseline에서는 두 개의 network를 사용한다.

- **Critic**: state-value function $V(s;\phi)$를 추정한다. 현재 state가 앞으로 얼마나 좋은지를 평가하고, baseline으로 사용해 actor gradient의 variance를 줄인다.
- **Actor**: policy $\pi(a\mid s;\theta)$를 생성한다. state가 주어졌을 때 action을 선택하는 확률분포를 학습한다.

각 network의 parameter와 step size는 서로 다르게 둔다.

| 구성 | 학습 대상 | Parameter | Step size | 역할 |
| --- | --- | --- | --- | --- |
| Actor | policy $\pi(a\mid s;\theta)$ | $\theta$ | $\alpha$ | action 선택 policy 개선 |
| Critic | state-value $V(s;\phi)$ | $\phi$ | $\beta$ | state value와 baseline 추정 |

여기서 Actor와 Critic이 두 개라는 말은 반드시 전체 neural network를 두 벌 복제한다는 뜻은 아니다. 일반적으로는 state를 처리하는 앞부분의 feature extractor를 공유하고, 마지막 부분을 두 개의 head로 나눈다. 하나의 head는 Actor의 policy를 출력하고 다른 head는 Critic의 state-value를 출력한다.

$$
h=f_\psi(s),
\qquad
\pi_\theta(a\mid s)=\pi_\theta(a\mid h),
\qquad
V_\phi(s)=V_\phi(h)
$$

이 구조에서는 공통 feature extractor $f_\psi$를 한 번만 사용하고, 마지막 FC layer 또는 output layer만 Actor와 Critic이 각각 가진다. 따라서 독립적인 network 두 개를 처음부터 끝까지 따로 만드는 것보다 parameter 수가 훨씬 작다. 다만 구현에 따라 Actor와 Critic을 완전히 별도의 network로 구성할 수도 있다.

### Actor와 Critic Update

Critic은 return $G_t$와 현재 value estimate의 차이를 줄이는 방향으로 update한다.

$$
\phi\leftarrow\phi+\beta\delta_t\nabla_\phi V(S_t;\phi)
$$

Actor는 $\delta_t$가 양수이면 해당 action의 probability를 높이고, 음수이면 낮추는 방향으로 update한다.

$$
\theta\leftarrow\theta+\alpha\gamma^t\delta_t
\nabla_\theta\log\pi(A_t\mid S_t;\theta)
$$

여기서 $\gamma^t$는 time step $t$에서 얻은 gradient에 적용되는 discount weighting이다.

### REINFORCE with Baseline Algorithm

{% capture reinforce_baseline_algorithm %}
$$
\begin{array}{l}
\textbf{Initialize state-value }V(s;\phi)\text{ and policy }\pi(a\mid s;\theta)\text{ randomly} \\
\textbf{Choose step sizes }\alpha>0,\ \beta>0 \\
\textbf{For each episode }1,\ldots,M\textbf{:} \\
\quad\quad \text{Generate an episode }s_0,a_0,r_1,s_1,\ldots,s_{T-1},a_{T-1},r_T\text{ using }\pi(\cdot\mid\cdot;\theta) \\
\quad\quad \textbf{For }t=0,\ldots,T-1\textbf{:} \\
\quad\quad\quad\quad G_t\leftarrow\text{return from step }t \\
\quad\quad\quad\quad \delta_t\leftarrow G_t-V(s_t;\phi) \\
\quad\quad\quad\quad \phi\leftarrow\phi+\beta\delta_t\nabla_\phi V(s_t;\phi) \\
\quad\quad\quad\quad \theta\leftarrow\theta+\alpha\gamma^t\delta_t\nabla_\theta\log\pi(a_t\mid s_t;\theta)
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Algorithm 1. REINFORCE with baseline" label="algorithm:reinforce-with-baseline" math=reinforce_baseline_algorithm %}

이 알고리즘에서 Critic은 $G_t$를 이용해 state-value function을 학습하고, Actor는 $G_t-V(S_t;\phi)$라는 residual을 이용해 policy를 개선한다. 즉, baseline은 Actor의 update 방향을 바꾸지 않고 각 sample의 scale과 variance를 줄이는 역할을 한다.

다만 REINFORCE with Baseline은 Critic을 사용하더라도 episode가 끝난 뒤 계산한 Monte Carlo return $G_t$를 target으로 사용하며 bootstrapping은 하지 않는다. 다음 Actor-Critic에서는 one-step TD target을 사용하여 episode가 끝나기 전에도 Actor와 Critic을 update한다.

## 05_Actor-Critic

### REINFORCE에서 Actor-Critic으로

Actor-Critic은 policy를 학습하는 Actor와 value function을 학습하는 Critic을 함께 사용하는 방법이다. A3C(Asynchronous Advantage Actor-Critic)가 대표적인 Actor-Critic 알고리즘이다.

REINFORCE with baseline과 비슷하게 Critic은 Actor의 update에 baseline 또는 value estimate를 제공한다. 하지만 REINFORCE처럼 episode가 끝날 때까지 전체 $G_t$를 기다리지 않고, Critic의 현재 value estimate를 이용해 one-step TD 방식으로 update할 수 있다. 따라서 online learning이 가능하고, 전체 return을 직접 사용하는 REINFORCE보다 gradient variance를 줄일 수 있다.

### Actor와 Critic 구조

![Actor-Critic의 Actor와 Critic 구조](/assets/img/blog/deep-reinforcement-learning-summary-5/actor-critic-structure.png)

- **Actor network**: state를 입력받아 policy $\pi_\theta(a\mid s)$를 출력하고, environment에서 action을 선택한다.
- **Critic network**: state 또는 state-action pair를 입력받아 $V_\phi(s)$ 또는 $Q_\phi(s,a)$를 추정한다.
- Critic의 value estimate는 Actor가 policy를 어느 방향으로 개선할지 판단하는 데 사용된다.

Actor와 Critic은 완전히 별도의 network로 만들 수도 있고, 앞부분의 feature extractor를 공유한 뒤 마지막 output head만 분리할 수도 있다. 따라서 Actor와 Critic이 두 개라는 것이 항상 network 전체 크기가 두 배라는 뜻은 아니다.

Value와 policy를 무엇으로 학습하는지에 따라 다음과 같이 생각할 수 있다.

- Value function만 학습: DQN과 같은 value-based 방법
- Policy만 학습: REINFORCE와 같은 policy gradient 방법
- Value function과 policy를 함께 학습: Actor-Critic 방법

### Policy Gradient와 Actor-Critic의 관계

![Policy Gradient와 Actor-Critic 방법의 관계](/assets/img/blog/deep-reinforcement-learning-summary-5/actor-critic-variants.png)

Policy gradient의 기본 형태는 policy gradient의 weight에 무엇을 사용하는지에 따라 나눌 수 있다. REINFORCE와 REINFORCE with Baseline은 앞에서 살펴봤으므로, 여기서는 Critic이 추정하는 값에 따른 Actor-Critic 형태를 살펴본다.

### Q-value Actor-Critic

Critic이 action-value function $Q_\phi(s,a)$를 추정하고, 이를 Actor의 policy gradient weight로 사용한다.

$$
\nabla_\theta J(\theta)
=\mathbb{E}_{\pi_\theta}
\left[Q_\phi(s,a)\nabla_\theta\log\pi_\theta(a\mid s)\right]
$$

Discrete action space에서는 action별 Q-value를 비교하기 쉽다. Continuous action space에서도 Q critic을 사용할 수 있지만, $\arg\max_a Q(s,a)$를 직접 계산하기 어렵기 때문에 Actor가 action을 생성하도록 별도로 학습하는 구조가 필요하다.

### Advantage Actor-Critic

Advantage function은 action-value와 state-value의 차이로 정의한다.

$$
A_{\phi_1,\phi_2}(s,a)
=Q_{\phi_2}(s,a)-V_{\phi_1}(s)
$$

$V_{\phi_1}(s)$는 action에 의존하지 않으므로, policy의 action distribution에 대한 expectation에서 다음 항은 0이 된다.

$$
\begin{aligned}
&\mathbb{E}_{a\sim\pi_\theta(\cdot\mid s)}
\left[V_{\phi_1}(s)\nabla_\theta\log\pi_\theta(a\mid s)\right] \\
&=V_{\phi_1}(s)
\nabla_\theta\sum_a\pi_\theta(a\mid s) \\
&=V_{\phi_1}(s)\nabla_\theta 1 \\
&=0
\end{aligned}
$$

따라서 $Q$-value에서 state-value baseline을 빼더라도 policy gradient의 expectation은 바뀌지 않는다.

$$
\begin{aligned}
\nabla_\theta J(\theta)
&=\mathbb{E}_{\pi_\theta}
\left[Q_{\phi_2}(s,a)
\nabla_\theta\log\pi_\theta(a\mid s)\right] \\
&=\mathbb{E}_{\pi_\theta}
\left[\left(Q_{\phi_2}(s,a)-V_{\phi_1}(s)\right)
\nabla_\theta\log\pi_\theta(a\mid s)\right] \\
&=\mathbb{E}_{\pi_\theta}
\left[A_{\phi_1,\phi_2}(s,a)
\nabla_\theta\log\pi_\theta(a\mid s)\right]
\end{aligned}
$$

$A(s,a)>0$이면 해당 action이 state의 평균적인 action보다 좋으므로 Actor가 그 action의 probability를 높이고, $A(s,a)<0$이면 probability를 낮추는 방향으로 update한다.

### TD Actor-Critic

TD Actor-Critic은 one-step TD error를 advantage의 sample estimate로 사용한다. 다음 절에서는 TD Actor-Critic을 대표 사례로 두고 update 과정과 algorithm을 자세히 살펴본다.

## 06_TD Actor-Critic

### TD Error와 Advantage

TD Actor-Critic은 Critic이 state-value function $V_\phi(s)$만 추정하고, one-step TD error를 advantage의 근사값으로 사용한다.

$$
\delta_t
=R_{t+1}+\gamma V_\phi(S_{t+1})-V_\phi(S_t)
$$

이 TD error는 다음과 같이 one-step return과 state value의 차이로도 볼 수 있다.

$$
\delta_t
=G_t^{(1)}-V_\phi(S_t)
$$

Value function이 정확하다면 조건부 expectation에서

$$
\mathbb{E}[\delta_t\mid S_t=s,A_t=a]
=Q^\pi(s,a)-V^\pi(s)
=A^\pi(s,a)
$$

가 된다. 따라서 TD error를 advantage의 sample estimate로 사용할 수 있다.

Actor update는 다음과 같다.

$$
\theta\leftarrow\theta
+\alpha\,\delta_t\nabla_\theta\log\pi_\theta(A_t\mid S_t)
$$

Critic update는 다음과 같다.

$$
\phi\leftarrow\phi
+\beta\,\delta_t\nabla_\phi V_\phi(S_t)
$$

TD Actor-Critic은 $V_\phi(s)$ 하나를 Critic으로 사용하면서도 한 step 뒤에 바로 Actor와 Critic을 update할 수 있다. 그래서 REINFORCE처럼 전체 episode return을 기다리지 않아도 되고, continuous control을 포함한 다양한 문제에서 실용적으로 많이 사용된다.

Actor-Critic을 구현할 때는 Critic과 Actor의 update 방향을 구분해야 한다.

- **Critic**은 target과 현재 value estimate의 차이를 줄이도록 state-value function을 학습한다.
- **Actor**는 expected return을 높이는 방향으로 policy parameter를 학습한다.

### Critic Update

Critic의 value function을 $V_\phi(s)$라고 하자. Critic은 target과 $V_\phi(s_t)$의 차이를 residual $\delta_t$로 두고 update한다.

Monte Carlo target을 사용하면

$$
\delta_t^{\mathrm{MC}}=G_t-V_\phi(S_t)
$$

이며, Critic update는 다음과 같다.

$$
\phi\leftarrow\phi
+\beta\delta_t^{\mathrm{MC}}
\nabla_\phi V_\phi(S_t)
$$

이는 다음 MSE loss를 최소화하는 gradient descent와 같은 방향이다.

$$
L_{\mathrm{MC}}(\phi)
=\frac12\left[G_t-V_\phi(S_t)\right]^2
$$

TD target을 사용하면

$$
\delta_t^{\mathrm{TD}}
=R_{t+1}+\gamma V_\phi(S_{t+1})-V_\phi(S_t)
$$

이고, Critic update는 다음과 같다.

$$
\phi\leftarrow\phi
+\beta\delta_t^{\mathrm{TD}}
\nabla_\phi V_\phi(S_t)
$$

### Actor Update

Actor는 policy gradient를 이용해 expected return $J(\theta)$를 최대화한다.

$$
\theta\leftarrow\theta+\alpha\nabla_\theta J(\theta)
$$

REINFORCE with baseline에서는 MC residual을 policy gradient의 weight로 사용한다.

$$
\Delta\theta_t^{\mathrm{MC}}
=\alpha\gamma^t
\left[G_t-V_\phi(S_t)\right]
\nabla_\theta\log\pi_\theta(A_t\mid S_t)
$$

TD Actor-Critic에서는 TD residual을 사용한다.

$$
\Delta\theta_t^{\mathrm{TD}}
=\alpha\gamma^t
\left[R_{t+1}+\gamma V_\phi(S_{t+1})-V_\phi(S_t)\right]
\nabla_\theta\log\pi_\theta(A_t\mid S_t)
$$

즉, Critic은 $\delta_t$를 이용해 $V_\phi$를 target에 맞추고, Actor는 같은 $\delta_t$를 이용해 선택한 action의 probability를 조절한다. MC에서는 $G_t$가 target이고, TD에서는 $R_{t+1}+\gamma V_\phi(S_{t+1})$가 target이다.

### TD Actor-Critic Algorithm

TD Actor-Critic은 episode가 끝날 때까지 기다리지 않고, 매 step마다 TD error를 계산하여 Critic과 Actor를 함께 update한다.

{% capture td_actor_critic_algorithm %}
$$
\begin{array}{l}
\textbf{Initialize critic }V(s;\phi)\text{ and actor }\pi(a\mid s;\theta)\text{ randomly} \\
\textbf{Choose step sizes }\alpha>0,\ \beta>0 \\
\textbf{For each episode }1,\ldots,M\textbf{:} \\
\quad\quad \text{Initialize }s\text{ as the first state of the episode} \\
\quad\quad I\leftarrow1 \\
\quad\quad \textbf{While }s\text{ is not terminal:} \\
\quad\quad\quad\quad \text{Select action }a\text{ according to }\pi(\cdot\mid s;\theta) \\
\quad\quad\quad\quad \text{Execute }a\text{ and observe }r,s' \\
\quad\quad\quad\quad \delta\leftarrow r+\gamma V(s';\phi)-V(s;\phi) \\
\quad\quad\quad\quad \phi\leftarrow\phi+\beta\delta\nabla_\phi V(s;\phi) \\
\quad\quad\quad\quad \theta\leftarrow\theta+\alpha I\delta\nabla_\theta\log\pi(a\mid s;\theta) \\
\quad\quad\quad\quad I\leftarrow\gamma I \\
\quad\quad\quad\quad s\leftarrow s'
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Algorithm 2. TD Actor-Critic" label="algorithm:td-actor-critic" math=td_actor_critic_algorithm %}

여기서 $I$는 처음에 1로 시작하여 매 step마다 $\gamma$를 곱하는 누적 discount factor이다.

$$
I_t=\gamma^t
$$

따라서 Actor update의 $I\delta$는 time step $t$에 따른 discount weighting을 반영한다. Critic은 현재 state value를 한 step TD target에 맞추고, Actor는 TD error가 양수인지 음수인지에 따라 선택한 action의 probability를 조정한다.

### REINFORCE with Baseline과 Target 비교

두 방법 모두 target과 현재 state value의 차이를 Actor update에 사용하지만, target을 계산하는 방식이 다르다.

- **REINFORCE with baseline**:

$$
G_t-V_\phi(S_t)
$$

여기서 $G_t$는 episode를 끝까지 실행한 뒤 계산한 **Monte Carlo target**이다. 실제 전체 return을 사용하므로 bootstrapping은 하지 않지만, episode 종료까지 기다려야 하고 variance가 클 수 있다.

- **TD Actor-Critic**:

$$
\left[R_{t+1}+\gamma V_\phi(S_{t+1})\right]-V_\phi(S_t)
$$

여기서 $R_{t+1}+\gamma V_\phi(S_{t+1})$는 **one-step TD target**이다. 다음 state의 value estimate를 target에 포함하므로 bootstrapping을 사용하며, episode가 끝나기 전에도 update할 수 있다.

결국 $G_t$를 사용하면 Monte Carlo policy gradient가 되고, $R_{t+1}+\gamma V_\phi(S_{t+1})$를 사용하면 TD Actor-Critic이 된다.

## 07_Asynchronous Advantage Actor-Critic (A3C)

Asynchronous Advantage Actor-Critic(A3C)은 여러 actor-learner(worker)가 각자의 environment에서 동시에 experience를 생성하고, 하나의 shared global network를 asynchronous하게 update하는 Actor-Critic 방법이다. 즉, 하나의 global network와 worker마다 복사된 여러 local network를 함께 사용한다.

### Asynchronous 구조

A3C는 하나의 shared global network와 다수의 worker로 구성된다. Global network는 공유되는 actor parameter $\theta$와 critic parameter $\phi$를 저장한다. 각 worker는 global network의 local copy인 $\theta'$와 $\phi'$를 가지고, 서로 독립적인 environment instance와 상호작용한다.

![A3C의 Global Network와 Worker 구조](/assets/img/blog/deep-reinforcement-learning-summary-5/a3c-global-network-workers.png)

Worker는 global parameter에서 local parameter를 복사해 시작한다. 여러 worker가 각자의 environment에서 병렬로 trajectory를 생성하는 동안 local network는 잠시 서로 다른 parameter를 사용할 수 있다. 각 worker는 다른 worker가 작업을 끝낼 때까지 기다리지 않고, 계산이 끝나는 순서대로 자신의 gradient를 global network에 적용한다.

### Asynchronous Update 과정

각 worker는 다음 과정을 반복한다.

1. Global network의 shared actor parameter $\theta$와 critic parameter $\phi$를 local network의 $\theta'$와 $\phi'$로 복사한다. 그리고 accumulated gradient를 저장할 $\Delta\theta$와 $\Delta\phi$를 0으로 초기화한다.
2. Local network로 자신의 environment와 상호작용하며 최대 $t_{\max}$ step까지 trajectory를 생성한다. Episode가 그보다 일찍 끝나면 해당 시점에서 rollout을 종료한다.
3. 수집한 trajectory의 각 step에 대해 $n$-step return $G_t^{(n)}$을 사용해 Actor와 Critic의 gradient를 누적한다. $G_t^{(n)}$의 자세한 정의는 아래에서 설명한다.

$$
\Delta\theta \leftarrow \Delta\theta +
\left(G_t^{(n)}-V_{\phi'}(s_t)\right)
\nabla_{\theta'}\log\pi_{\theta'}(a_t\mid s_t)
$$

$$
\Delta\phi \leftarrow \Delta\phi -
\left(G_t^{(n)}-V_{\phi'}(s_t)\right)
\nabla_{\phi'}V_{\phi'}(s_t)
$$

여기서 $\Delta\theta$는 Actor objective를 maximize하기 위한 gradient이고, $\Delta\phi$는 Critic value loss를 minimize하기 위한 loss gradient이다. 이처럼 $t_{\max}$ step 동안 누적한 값을 accumulated gradient라고 한다.

4. Worker는 다른 worker와 관계없이 accumulated gradient를 global network에 asynchronous하게 적용한다.

$$
\theta \leftarrow \theta + \alpha\Delta\theta
\qquad\text{and}\qquad
\phi \leftarrow \phi - \beta\Delta\phi
$$

Actor는 gradient ascent를 사용하고, Critic은 value loss에 대한 gradient descent를 사용하므로 두 update의 부호가 다르다. 각 worker의 gradient는 다른 worker의 update가 끝나기를 기다리지 않고 global network에 도착하는 대로 적용된다.

5. Update가 끝나면 global network의 parameter를 다시 local network로 복사해 $\theta'\leftarrow\theta$, $\phi'\leftarrow\phi$로 동기화한다. 이후 다시 rollout을 생성하고 gradient를 누적한다.

### Asynchronous 학습의 장점

여러 worker를 병렬로 실행하고 서로 다른 trajectory에서 계산한 update를 global network에 섞는 구조는 다음과 같은 장점이 있다.

1. **Temporal correlation과 non-stationarity 완화**: 하나의 worker가 연속해서 생성한 trajectory에는 여전히 temporal correlation이 존재할 수 있다. 하지만 여러 worker의 서로 다른 environment 경험과 update가 섞이면서 한 trajectory에 치우친 correlation과 policy 변화에 따른 non-stationarity의 영향이 줄어든다. 두 문제가 완전히 사라지는 것은 아니다.
2. **Experience replay 불필요**: Parallel actor-learner가 계속 새로운 experience를 생성하므로 DQN과 같은 experience replay를 사용하지 않아도 된다.
3. **다양한 exploration**: Worker마다 다른 environment state와 trajectory를 경험하고, local parameter가 잠시 다르게 유지될 수 있어 서로 다른 방향으로 exploration할 수 있다.
4. **On-policy RL 지원**: 각 worker가 자신의 현재 local policy로 생성한 trajectory를 사용하므로, replay buffer 없이 on-policy 학습을 수행할 수 있다.
5. **Multi-core CPU 활용**: 여러 worker를 multi-core CPU에서 parallel하게 실행할 수 있다.

### n-step Return을 이용한 Advantage Estimate

Policy gradient(REINFORCE)는 trajectory 전체의 return을 모든 action에 똑같이 할당하기보다, 각 action 이후의 reward-to-go return $G_t$를 사용해 해당 action의 log-probability를 업데이트한다. $A_t$ 이전에 발생한 reward는 $A_t$가 원인이 아니므로 함께 사용하면 gradient variance만 커질 수 있다.

$G_t$는 $A_t$를 선택한 뒤의 결과를 추정하지만, 그 부호만으로 action이 절대적으로 좋은지 나쁜지를 판단하는 것은 아니다. Advantage는 같은 state에서 policy가 평균적으로 얻는 값인 $V^\pi(s)$와 비교한다. 따라서 positive advantage는 해당 state에서 policy의 평균적인 action보다 나은 결과를, negative advantage는 더 나쁜 결과를 의미한다. Advantage function은 다음과 같이 정의된다.

$$
A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s)
$$

$Q(s,a)$와 $V(s)$를 각각 추정해야 하므로 두 개의 value estimate가 필요하지만, 이것이 반드시 두 개의 separate neural network를 의미하는 것은 아니다. A3C는 별도의 $Q$ network를 사용하지 않고, $n$-step return을 $Q^\pi(S_t,A_t)$의 sample estimate로 사용한다.

$$
G_t^{(n)}
=\sum_{k=0}^{n-1}\gamma^kR_{t+k+1}
+\gamma^nV_\phi(S_{t+n})
$$

Trajectory가 $n$ step 전에 terminal state에 도달하면 마지막 bootstrap value는 0으로 둔다. $n$이 커질수록 bootstrap을 덜 사용하므로 $G_t^{(n)}$은 Monte Carlo return 또는 reward-to-go에 가까워진다. 이때 bootstrap bias는 줄어들지만 gradient variance는 커질 수 있다. 반대로 작은 $n$은 더 많이 bootstrap하므로 일반적으로 bias는 커지고 variance는 줄어든다. 따라서 $n$을 조절해 bias와 variance 사이의 trade-off를 선택할 수 있다. A3C의 advantage estimate는 다음과 같다.

$n$은 모든 sample에 대해 고정된 값이 아니다. A3C의 $t_{\max}$는 rollout의 최대 길이일 뿐이며, backward loop에서는 마지막 transition에 1-step return, 그 이전 transition에 2-step return을 적용하는 식으로 rollout 길이(최대 $t_{\max}$)까지 이어간다. Episode가 일찍 종료되면 유효한 $n$도 그보다 짧아진다. 따라서 하나의 rollout 안에서도 여러 $n$-step return이 유연하게 함께 사용된다.

$$
\hat{A}_t
=G_t^{(n)}-V_\phi(S_t)
$$

따라서 A3C에는 별도의 $Q$ network가 필요하지 않다. 실제 network는 보통 feature extractor를 공유하고, action distribution을 출력하는 policy head와 $V_\phi(s)$를 출력하는 value head로 나뉜다.

Actor는 $\hat{A}_t$를 policy gradient의 weight로 사용한다.

$$
g_\theta
=\sum_t
\nabla_\theta\log\pi_\theta(A_t\mid S_t)\hat{A}_t
$$

Critic은 $n$-step return과 state-value estimate의 차이를 줄인다.

$$
L_V(\phi)
=\frac{1}{2}
\left[G_t^{(n)}-V_\phi(S_t)\right]^2
$$

원래 A3C는 policy가 너무 일찍 deterministic해지는 것을 막고 exploration을 유지하기 위해 Actor objective에 entropy regularization도 추가한다.

### A3C Algorithm

A3C의 한 worker는 global network의 parameter를 local network로 동기화한 뒤, 자신의 environment에서 최대 $t_{\max}$ step만큼 rollout을 생성하고 gradient를 누적한다.

{% capture a3c_worker_algorithm %}
$$
\begin{array}{l}
\textbf{Global network: }\theta,\phi;\quad
\textbf{local network: }\theta',\phi' \\
\textbf{Initialize shared global step counter }t\leftarrow1 \\
\textbf{repeat} \\
\quad \Delta\theta\leftarrow0,\quad \Delta\phi\leftarrow0 \\
\quad \theta'\leftarrow\theta,\quad \phi'\leftarrow\phi \\
\quad t_{\mathrm{start}}\leftarrow t,\quad \text{get state }s_t \\
\quad \textbf{while }s_t\text{ is not terminal and }t<t_{\mathrm{start}}+t_{\max}\textbf{ do} \\
\qquad \text{sample }a_t\sim\pi_{\theta'}(\cdot\mid s_t) \\
\qquad \text{execute }a_t;\ \text{observe }r_{t+1},s_{t+1};\quad t\leftarrow t+1 \\
\quad \textbf{end while} \\
\quad R\leftarrow
\begin{cases}
0,&\text{if }s_t\text{ is terminal},\\
V_{\phi'}(s_t),&\text{otherwise}
\end{cases} \\
\quad \textbf{for }i=t-1,\ldots,t_{\mathrm{start}}\textbf{ do} \\
\qquad R\leftarrow r_{i+1}+\gamma R \\
\qquad \Delta\theta\leftarrow\Delta\theta+
(R-V_{\phi'}(s_i)) \\
\qquad\qquad {}\cdot\nabla_{\theta'}\log\pi_{\theta'}(a_i\mid s_i) \\
\qquad \Delta\phi\leftarrow\Delta\phi-
(R-V_{\phi'}(s_i)) \\
\qquad\qquad {}\cdot\nabla_{\phi'}V_{\phi'}(s_i) \\
\quad \textbf{end for} \\
\quad \theta\leftarrow\theta+\alpha\Delta\theta,\quad
\phi\leftarrow\phi-\beta\Delta\phi \\
\textbf{until training ends}
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Algorithm 3. A3C worker" label="algorithm:a3c-worker" math=a3c_worker_algorithm %}

Backward loop에서 $R$을 반복해서 갱신하면 다음과 같이 $n$-step return이 전개된다.

$$
R_i=r_{i+1}+\gamma r_{i+2}+\cdots+\gamma^{n-1}r_{i+n}
+\gamma^nV_{\phi'}(s_{i+n})=G_i^{(n)}
$$

Rollout이 terminal state에서 끝나면 bootstrap value $V_{\phi'}(s_{i+n})$는 $0$으로 둔다.

### State Space와 Action Space

A3C는 neural network를 function approximator로 사용하므로 discrete state뿐 아니라 continuous state나 image와 같은 high-dimensional state도 처리할 수 있다.

- **Discrete action space**: policy head가 action별 probability를 출력한다.
- **Continuous action space**: policy head가 Gaussian distribution의 mean과 variance 같은 parameter를 출력하고 그 distribution에서 action을 sampling한다.

따라서 state와 action이 모두 continuous인 문제에도 A3C를 적용할 수 있다. 다만 continuous control에서는 반드시 A3C를 먼저 사용해야 한다기보다, value-based DQN보다 continuous action으로 확장하기 쉬운 on-policy 방법이라고 보는 편이 정확하다.

### DQN과 A3C 비교

| 구분 | DQN | A3C |
| --- | --- | --- |
| 학습 대상 | Action-value $Q(s,a)$ | Policy $\pi(a\mid s)$와 state-value $V(s)$ |
| 학습 방식 | Off-policy | On-policy |
| Experience replay | 사용 | 사용하지 않음 |
| Experience 생성 | 일반적으로 하나의 agent | 여러 actor-learner가 parallel하게 생성 |
| Update | Replay buffer에서 minibatch를 sampling | Worker gradient를 global network에 asynchronous하게 적용 |
| Return | 기본적으로 one-step TD target | 최대 $t_{\max}$의 $n$-step return |
| Action space | 기본적으로 discrete action | Discrete action과 continuous action 모두 가능 |

[A3C 원 논문](https://proceedings.mlr.press/v48/mniha16.html)의 Atari 실험에서는 16개의 CPU worker를 사용한 asynchronous 방법들이 GPU로 학습한 DQN보다 빠르게 학습하는 경향을 보였고, A3C는 당시 DQN 계열과 비교해 절반의 training time으로 높은 평균 score를 기록했다. 다만 hardware, hyperparameter search와 game별 결과가 다르므로, 이를 모든 문제에서 A3C가 DQN이나 Double DQN보다 빠르게 수렴한다는 일반적인 결론으로 확대해서는 안 된다.

## 08_Synchronous Advantage Actor-Critic (A2C)

Advantage Actor-Critic(A2C)는 A3C의 asynchronous update를 synchronous하게 바꾼 variant이다. 여러 worker가 각자의 environment에서 rollout을 수집한다는 점과 advantage를 사용해 Actor와 Critic을 함께 학습한다는 점은 A3C와 같다. 핵심 차이는 worker의 gradient를 global network에 적용하는 시점이다.

### A2C가 Synchronous인 이유

A3C의 worker들이 항상 본질적으로 서로 다른 policy를 사용하는 것은 아니다. 각 worker는 global network의 parameter를 서로 다른 시점에 local network로 복사한다. 그 후 다른 worker가 update를 끝내기를 기다리지 않고 rollout과 gradient 계산을 진행하므로, global network가 계속 바뀌는 동안 worker의 local parameter가 잠시 stale하거나 서로 다른 policy version이 될 수 있다. 따라서 global network에 도착하는 gradient들은 약간씩 다른 policy version으로 계산된 값일 수 있다.

A2C는 이 inconsistency를 줄이기 위해 하나의 update cycle 안에서 모든 worker가 동일한 현재 global actor와 critic parameter를 받도록 한다. Worker마다 environment state와 trajectory는 다르지만, 적어도 해당 rollout을 시작할 때 사용하는 policy version은 같다.

### Synchronous Update 과정

A2C의 한 update cycle은 다음과 같이 진행된다.

1. 현재 global parameter $\theta^k,\phi^k$를 모든 worker에 broadcast한다.
2. 모든 worker는 $\theta^k,\phi^k$의 local copy로 각자의 environment에서 rollout을 수집하고, $n$-step return과 advantage를 계산한다.
3. 먼저 rollout을 끝낸 worker도 synchronization barrier에서 다른 worker를 기다린다.
4. 모든 worker의 gradient 또는 rollout loss를 하나의 batch로 aggregate한다.
5. Aggregate된 gradient로 global network를 한 번 update한다.
6. 새 global parameter를 다시 모든 worker에 broadcast하고 다음 cycle을 시작한다.

이를 간단히 쓰면, worker $i$가 계산한 gradient를 $g_i$라고 할 때

$$
g=\frac{1}{N}\sum_{i=1}^{N}g_i,
\qquad
\theta^{k+1}=\theta^k+\alpha g_\theta,
\qquad
\phi^{k+1}=\phi^k-\beta g_\phi
$$

와 같이 update할 수 있다. 여기서 coordinator 또는 barrier는 모든 worker가 한 cycle을 끝낼 때까지 기다렸다가 batch aggregation과 global update를 진행하도록 만드는 동기화 개념이다. 반드시 별도의 standalone component가 있어야 하는 것은 아니며, vectorized environment나 multiprocessing framework가 이 synchronization을 구현할 수도 있다.

이 방식에서는 한 batch 안에서 worker가 계산한 gradient가 global network에 순서대로 asynchronous하게 적용되지 않는다. 대신 동일한 global parameter version에서 생성된 여러 rollout을 모아 한 번에 update하므로, A3C보다 cohesive한 same-policy batch를 구성할 수 있다.

### A3C와 A2C 비교

| 구분 | A3C | A2C |
| --- | --- | --- |
| Update timing | Worker가 준비되는 대로 asynchronous하게 update | 모든 worker가 준비된 뒤 synchronous하게 update |
| Local policy version | Worker마다 sync 시점이 달라 stale하거나 서로 다를 수 있음 | 한 cycle 시작 시 같은 global policy version을 broadcast |
| Gradient application | Worker gradient를 global network에 도착하는 대로 적용 | Gradient를 aggregate한 뒤 global network를 한 번 적용 |
| Waiting | 다른 worker를 기다리지 않음 | 먼저 끝난 worker도 가장 느린 worker를 기다림 |
| Compute pattern | 비동기 worker update, CPU 병렬 실행에 적합 | Batch/vectorized computation과 large batch 구성에 적합 |
| Main trade-off | Staleness를 허용하는 대신 worker idle을 줄임 | 더 coherent한 update를 얻는 대신 synchronization과 straggler 대기 비용이 생김 |

A2C는 같은 policy version에서 수집한 rollout을 사용하므로 gradient variance가 낮아지는 경우가 있고, large batch 또는 vectorized computation을 효율적으로 활용할 수 있다. 반면 매 cycle마다 가장 느린 worker를 기다려야 하며, batch size가 크다고 해서 항상 더 빠르게 수렴하거나 모든 task에서 A3C보다 좋은 성능을 보장하는 것은 아니다.

## 참고 강의

- [고려대 오승상 강화학습 21 — Policy Gradient algorithm](https://www.youtube.com/watch?v=QoHWaruzGZ4)
- [고려대 오승상 강화학습 22 — REINFORCE](https://www.youtube.com/watch?v=CH09gfU7ko4)
- [고려대 오승상 강화학습 23 — Actor-Critic method](https://www.youtube.com/watch?v=l-9oSDKIaxg)
- [고려대 오승상 강화학습 24 — A3C 1](https://www.youtube.com/watch?v=YJi3sBv2fRg)
- [고려대 오승상 강화학습 25 — A3C 2](https://www.youtube.com/watch?v=spAnltgCRY8)
