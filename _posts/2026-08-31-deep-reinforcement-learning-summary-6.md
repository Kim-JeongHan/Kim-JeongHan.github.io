---
layout: post
title: Reinforcement Learning 6 - Policy Gradient Algorithms (DDPG, TRPO, PPO)
date: 2026-08-31 00:00:00 +0900
slug: deep-reinforcement-learning-summary-6
render_with_liquid: true
use_math: true
categories:
- 공부
- 강화학습
tags:
- reinforcement-learning
- ddpg
- deterministic-policy-gradient
---

## 00_DDPG 개요

Deep Deterministic Policy Gradient(DDPG)는 continuous action space를 다루기 위한 model-free, off-policy actor-critic 알고리즘이다. Actor는 state $s$를 입력으로 받아 하나의 action을 직접 출력하는 deterministic policy $\mu_\theta(s)$를 사용하고, Critic은 action-value function $Q^\mu(s,a)$를 neural network로 approximation한다.

DDPG의 Critic이 DQN 그 자체인 것은 아니다. 다만 DQN에서 효과적이었던 두 가지 안정화 아이디어를 가져온다.

- **Experience replay**: 과거 transition $(s_t,a_t,r_{t+1},s_{t+1})$를 replay buffer에 저장하고, 서로 상관이 적은 minibatch를 sampling하여 학습한다.
- **Target network**: target actor $\mu_{\hat\theta}$와 target critic $Q_{\hat\phi}$를 따로 두어 Bellman target을 계산하고, parameter를 soft update한다.

따라서 Critic target은 대략

$$
y_t=r_{t+1}+\gamma Q_{\hat\phi}(s_{t+1},\mu_{\hat\theta}(s_{t+1}))
$$

처럼 계산된다. Actor가 action을 deterministic하게 출력하기 때문에, transition을 수집할 때는 보통 exploration noise를 더한 behaviour policy

$$
a_t=\mu_\theta(s_t)+\epsilon_t
$$

를 사용한다. 즉 target policy는 deterministic하지만 data collection은 noise를 통해 탐색한다. 자세한 알고리즘 구성은 [DDPG 원 논문](https://arxiv.org/abs/1509.02971)에서 확인할 수 있다.

DDPG에서 학습 중인 return이나 episode reward가 training step에 따라 monotonically 증가할 필요는 없다. Critic approximation error, bootstrapping, off-policy replay data, nonlinear neural network approximation이 서로 영향을 주기 때문에 value와 policy update가 흔들리거나 일시적으로 성능이 낮아질 수 있다. 따라서 평균 reward의 추세와 여러 seed의 결과를 함께 확인해야 한다.

## 01_Deterministic Policy

Stochastic policy는 state에서 action distribution을 정의하고 그 distribution에서 action을 sampling한다.

$$
a_t\sim\pi_\theta(\cdot\mid s_t),
\qquad
\pi_\theta(a\mid s)=P(A_t=a\mid S_t=s;\theta)
$$

반면 deterministic policy는 각 state에 대해 하나의 action을 직접 정한다.

$$
a=\mu_\theta(s)
$$

즉, stochastic policy가 같은 state에서도 여러 action을 확률적으로 선택할 수 있는 distribution이라면, deterministic policy는 같은 state에서 항상 같은 action을 출력한다. Action이 연속적인 경우 deterministic actor가 action vector를 직접 출력하므로 continuous하고 high-dimensional한 action space에 적용하기 쉽다.

다만 deterministic policy 자체에는 action을 다양하게 선택하게 하는 확률적 요소가 없다. 그러므로 학습 데이터를 수집할 때는 위와 같이 Gaussian noise 등의 exploration noise를 action에 추가하거나 별도의 behaviour policy를 사용해야 한다. 이 점에서 policy가 deterministic이라는 것과 exploration이 필요 없다는 것은 같은 의미가 아니다.

## 02_Deterministic Policy Gradient

Deterministic Policy Gradient(DPG)는 stochastic policy처럼 action distribution 전체를 parameterize하고 sampling하는 대신, 현재 state에서 actor가 출력한 action을 Critic의 gradient 방향으로 이동시킨다. 한 state에서의 actor parameter update 방향은 다음과 같이 쓸 수 있다.

$$
\Delta\theta
=
\left.\nabla_a Q^\mu(s,a)\right\vert_{a=\mu_\theta(s)}
\nabla_\theta\mu_\theta(s)
$$

이는 chain rule을 사용한 표현이다. $\nabla_a Q^\mu(s,a)$는 해당 state에서 action을 어느 방향으로 바꾸면 Q-value가 증가하는지 나타내고, $\nabla_\theta\mu_\theta(s)$는 actor parameter를 바꿀 때 action이 어떻게 변하는지를 나타낸다.

여기서 Actor가 deterministic이라고 해서 $Q^\mu(s,a)$ 자체가 deterministic한 함수로 바뀌거나 action 변수가 사라지는 것은 아니다. Critic은 여전히 state와 action의 함수 $Q^\mu(s,a)$이고, Actor가 state에서 결정한 $a=\mu_\theta(s)$를 대입하여 action에 대한 민감도를 계산한다.

전체 deterministic policy gradient는 discounted state visitation measure를 사용해 state에 대해 적분한다.

$$
\nabla_\theta J(\mu_\theta)
=
\int_{\mathcal{S}}
\rho_\mu(s)
\left.
\nabla_a Q^\mu(s,a)\,\nabla_\theta\mu_\theta(s)
\right\vert_{a=\mu_\theta(s)}
\,ds
$$

이를 theorem의 expectation 표기로 쓰면 다음과 같다.

$$
\nabla_\theta J(\mu_\theta)
=
\mathbb{E}_{s\sim\rho_\mu}
\left[
\left.\nabla_a Q^\mu(s,a)\right\vert_{a=\mu_\theta(s)}
\nabla_\theta\mu_\theta(s)
\right]
$$

### Stochastic Policy Gradient와의 비교

Stochastic Policy Gradient는 일반적으로 state와 action 모두에 대해 평균을 낸다.

$$
\nabla_\theta J(\pi_\theta)
=
\int_{\mathcal{S}}\rho_\pi(s)
\int_{\mathcal{A}}
\pi_\theta(a\mid s)
\nabla_\theta\log\pi_\theta(a\mid s)
Q^\pi(s,a)\,da\,ds
$$

동일한 내용을 score-function 형태로 쓰면

$$
\nabla_\theta J(\pi_\theta)
=
\mathbb{E}_{s\sim\rho_\pi,\,a\sim\pi_\theta(\cdot\mid s)}
\left[
Q^\pi(s,a)\nabla_\theta\log\pi_\theta(a\mid s)
\right]
$$

이다. 즉 stochastic policy는 같은 state에서도 여러 action을 sampling하므로 state와 action에 대한 expectation/integral이 모두 필요하다.

반면 DPG에서는 각 state의 action이 $a=\mu_\theta(s)$로 고정되므로 action space에 대한 별도의 적분이 없다. 따라서 action dimension이 큰 continuous control에서도 action distribution 전체를 적분하거나 sampling하는 부담을 줄여 gradient를 더 효율적으로 추정할 수 있다. 그렇다고 DPG가 action과 무관하다는 뜻은 아니다. Actor가 출력하는 action에서 Critic의 action gradient $\nabla_a Q^\mu(s,a)$를 계산하고, 그 값을 통해 actor parameter를 update한다.

위 DPG theorem의 expectation은 policy $\mu$를 따를 때의 discounted state visitation measure $\rho_\mu$에 대한 것이다. 이것이 true DPG theorem의 objective/distribution이고, 실제 DDPG에서는 off-policy replay buffer에서 state를 sampling하는 practical actor surrogate를 사용한다. 두 방식의 차이는 다음 절에서 구체적으로 정리한다.

DPG의 자세한 정리와 deterministic policy gradient theorem은 [Deterministic Policy Gradient 원 논문](https://proceedings.mlr.press/v32/silver14.html)을 참고할 수 있다.

## 03_Discounted State Visitation Frequency

Policy gradient에서 state별로 gradient를 얼마나 자주 반영할지 나타내기 위해 discounted state visitation frequency 또는 occupancy measure를 사용한다.

$$
\rho_\pi(s)
=\sum_{t=0}^{\infty}\gamma^t P(S_t=s\mid\pi)
=
\int_{\mathcal{S}}
p_0(s')
\sum_{t=0}^{\infty}
\gamma^t
p(s'\!\to s,t,\pi)\,ds'
$$

Discrete state에서는 첫 번째 식의 $P(S_t=s\mid\pi)$를 사용하고, continuous state space에서는 이를 한 점의 probability라기보다 해당 시점의 state density $p_t(s\mid\pi)$로 해석한다. 초기 state가 한 state에만 고정되지 않고 모든 state에서 시작할 수 있다면, 이를 초기 state density와 transition density로 전개할 수 있다.

여기서 $p_0(s')$는 initial state $s'$의 density이고, $p(s'\!\to s,t,\pi)$는 policy $\pi$를 따를 때 initial state $s'$에서 $t$ time step 뒤 state $s$에 도달하는 probability density이다. 초기 state $s'$가 특정 하나로 정해지는 것이 아니라 모든 state에서 가능하기 때문에 $s'$에 대해 적분한다.

이 measure를 모든 state에 대해 적분하면 각 시점의 state density는 1로 적분되므로

$$
\int_{\mathcal{S}}\rho_\pi(s)\,ds
=
\sum_{t=0}^{\infty}\gamma^t
=
\frac{1}{1-\gamma}
$$

가 된다. Discrete state에서는 적분 대신 $\sum_{s\in\mathcal{S}}$를 사용한다. 따라서

$$
d_\pi(s)=(1-\gamma)\rho_\pi(s)
$$

로 정의하면 $d_\pi(s)$는 적분값이 1인 proper probability density가 된다. 원래 deterministic policy gradient처럼 $\rho_\pi$를 사용하는 식을 $d_\pi$에 대한 expectation으로 다시 쓰면

$$
\int_{\mathcal{S}}\rho_\pi(s)f(s)\,ds
=
\frac{1}{1-\gamma}
\mathbb{E}_{s\sim d_\pi}[f(s)]
$$

이다. 따라서 $\rho_\pi$를 $d_\pi$로 바꿀 때 생기는 $1/(1-\gamma)$ factor는 gradient의 방향을 바꾸지 않고 크기만 바꾸며, learning rate에 흡수할 수 있다.

## 04_DDPG 학습 방법

### Parameter 구성

DDPG는 online network와 target network를 각각 actor와 critic에 대해 유지한다.

- Online actor: $\mu_\theta(s)$ — state $s$에서 deterministic action을 출력한다.
- Online critic: $Q_\phi(s,a)$ — state-action pair의 value를 approximation한다.
- Target actor: $\mu_{\hat\theta}(s)$
- Target critic: $Q_{\hat\phi}(s,a)$

Online parameter $\theta,\phi$는 replay buffer의 transition으로 학습하고, target parameter $\hat\theta,\hat\phi$는 online network를 천천히 따라가도록 유지한다. 앞의 DPG theorem에서는 true value function을 나타내기 위해 $Q^\mu$를 사용했고, 여기서는 neural network로 approximation하는 online critic을 $Q_\phi$로 표기한다.

### Critic Update

Replay buffer $D$에서 transition $(s,a,r,s')$를 minibatch로 sampling하고, target actor가 다음 state의 action을 결정한 뒤 target critic으로 Bellman target을 계산한다.

$$
y=r+\gamma Q_{\hat\phi}\left(s',\mu_{\hat\theta}(s')\right)
$$

Terminal transition이면 bootstrap 항을 제외하도록 보통 $y=r+\gamma(1-d)Q_{\hat\phi}(s',\mu_{\hat\theta}(s'))$처럼 done mask $d$를 곱한다. TD error는

$$
\delta=y-Q_\phi(s,a)
$$

이고, critic loss는 다음과 같이 둘 수 있다.

$$
L(\phi)=\frac{1}{2}\mathbb{E}_{(s,a,r,s')\sim D}\left[\delta^2\right]
$$

Target network로 계산한 $y$는 해당 critic update에서 고정된 값으로 취급하는 semi-gradient를 사용한다. 따라서

$$
\nabla_\phi L(\phi)
\approx
-\mathbb{E}_{D}\left[\delta\nabla_\phi Q_\phi(s,a)\right],
\qquad
\phi\leftarrow\phi-\alpha_Q\nabla_\phi L(\phi)
$$

이며, 이를 한 번에 쓰면 {::nomarkdown}\(\phi\leftarrow\phi+\alpha_Q\mathbb{E}_{D}[\delta\nabla_\phi Q_\phi(s,a)]\){:/nomarkdown}이다. 즉 online critic은 천천히 변하는 target actor와 target critic이 제공하는 target을 향해 학습하므로, target이 매 순간 함께 크게 움직이는 경우보다 update가 안정적이다.

### Actor Update

실제 DDPG actor는 true DPG theorem의 $s\sim\rho_\mu$를 직접 sampling하지 않고, off-policy로 수집된 replay buffer $D$에서 state를 sampling하는 practical surrogate를 최적화한다.

$$
J_{\mathrm{actor}}(\theta)
=
\mathbb{E}_{s\sim D}\left[Q_\phi\left(s,\mu_\theta(s)\right)\right]
$$

Chain rule을 적용한 actor gradient는

$$
\nabla_\theta J_{\mathrm{actor}}(\theta)
=
\mathbb{E}_{s\sim D}
\left[
\left.\nabla_aQ_\phi(s,a)\right\vert_{a=\mu_\theta(s)}
\nabla_\theta\mu_\theta(s)
\right]
$$

이다. Minibatch $\{s_i\}_{i=1}^{B}$에 대해서는

$$
\hat g_\theta
=
\frac{1}{B}\sum_{i=1}^{B}
\left[
\left.\nabla_aQ_\phi(s_i,a)\right\vert_{a=\mu_\theta(s_i)}
\nabla_\theta\mu_\theta(s_i)
\right]
$$

를 계산하고, actor는 gradient ascent로 $\theta\leftarrow\theta+\alpha_\mu\hat g_\theta$처럼 update한다. 구현에서 actor loss를 $-Q_\phi(s,\mu_\theta(s))$로 정의하면 이와 같은 update를 gradient descent로 구현할 수 있다. 따라서 DPG theorem의 state distribution은 $\rho_\mu$이지만, DDPG의 실용적인 actor update는 replay distribution $D$를 사용하는 off-policy update이다.

### Exploration Noise

Deterministic actor는 같은 state에서 항상 같은 action을 출력하므로 data collection에서는 noise를 더한 behaviour action을 사용한다.

$$
a_t=\mu_\theta(s_t)+N_t
$$

여기서 $N_t$는 시간에 따라 변해야 한다. DQN의 $\epsilon$-greedy는 discrete action 중 임의의 action을 선택하는 방식인 반면, continuous action space에서는 현재 actor action에 additive noise를 더하는 방식이 자연스럽다. 둘 다 exploration을 위한 장치이지만 같은 알고리즘은 아니다. DDPG 원 논문에서는 시간적으로 상관된 Ornstein–Uhlenbeck(OU) noise process를 사용했지만, 실제로는 time-varying Gaussian noise 등 다른 noise process도 사용할 수 있다. 이때 target policy $\mu_{\hat\theta}$는 noise가 없는 deterministic policy이고, noise가 더해진 action은 environment와 상호작용할 때의 behaviour action이다.

### Soft Target Update

Target network는 매 update step마다 online parameter의 작은 비율만 섞어 다음처럼 갱신한다.

$$
\hat\phi\leftarrow\tau\phi+(1-\tau)\hat\phi,
\qquad
\hat\theta\leftarrow\tau\theta+(1-\tau)\hat\theta,
\qquad \tau\ll1
$$

DQN에서 흔히 쓰는 hard update가 $C$ step마다 online network를 target network에 통째로 복사하는 방식이라면, DDPG의 soft update는 매 step 조금씩 이동하는 방식이다. 예를 들어 $\tau=0.01$이면 매 step 현재 online parameter의 1%를 target에 반영한다. 이는 단순히 100 step마다 한 번 복사하는 것과 수학적으로 동일하지는 않지만, target이 급격히 변하지 않도록 하여 critic의 bootstrap target과 actor update를 안정화한다.

## 05_DDPG Algorithm

앞에서 설명한 online actor/critic, target network, replay buffer, exploration noise를 함께 사용하는 전체 학습 과정은 다음과 같다.

{% capture ddpg_algorithm %}
$$
\begin{array}{l}
\textbf{Initialize online actor }\mu_\theta(s)\text{ and critic }Q_\phi(s,a) \\
\quad\quad \text{with random weights} \\
\textbf{Initialize target actor }\mu_{\hat\theta}(s)\text{ and target critic }Q_{\hat\phi}(s,a) \\
\quad\quad \text{with online weights} \\
\quad\quad \text{Set }\hat\theta\leftarrow\theta,\quad\hat\phi\leftarrow\phi \\
\textbf{Initialize replay buffer }\mathcal{R} \\
\textbf{For each episode }1,\ldots,M\textbf{:} \\
\quad\quad \text{Initialize time-varying noise process }\mathcal{N} \\
\quad\quad \text{Receive initial state }s_1 \\
\quad\quad \textbf{For }t=1,\ldots,T\textbf{:} \\
\quad\quad\quad\quad \text{Select behaviour action }a_t\leftarrow\mu_\theta(s_t)+N_t \\
\quad\quad\quad\quad \text{Execute }a_t\text{ and observe }r_{t+1},s_{t+1},d_t \\
\quad\quad\quad\quad \mathcal{R}\leftarrow\mathcal{R}\cup\{(s_t,a_t,r_{t+1},s_{t+1},d_t)\} \\
\quad\quad\quad\quad \text{Sample minibatch }B\text{ of transitions from }\mathcal{R} \\
\quad\quad\quad\quad \text{For each }i\in B,\quad y_i\leftarrow r_{i+1}+\gamma(1-d_i) \\
\quad\quad\quad\quad\quad\quad\quad\quad {}\cdot Q_{\hat\phi}\left(s_{i+1},\mu_{\hat\theta}(s_{i+1})\right) \\
\quad\quad\quad\quad \text{Set }\mathcal{L}_Q(\phi)\leftarrow\frac{1}{2|B|}\sum_{i\in B} \\
\quad\quad\quad\quad\quad\quad\quad\quad\left[y_i-Q_\phi(s_i,a_i)\right]^2 \\
\quad\quad\quad\quad \text{Update critic by minimizing }\mathcal{L}_Q(\phi) \\
\quad\quad\quad\quad \phi\leftarrow\phi-\alpha_Q\nabla_\phi\mathcal{L}_Q(\phi) \\
\quad\quad\quad\quad \text{Compute minibatch deterministic policy gradient }\hat g_\theta: \\
\quad\quad\quad\quad \hat g_\theta\leftarrow\frac{1}{|B|}\sum_{i\in B} \\
\quad\quad\quad\quad\quad\quad\quad\quad\left.\nabla_aQ_\phi(s_i,a)\right|_{a=\mu_\theta(s_i)} \\
\quad\quad\quad\quad\quad\quad\quad\quad {}\cdot\nabla_\theta\mu_\theta(s_i) \\
\quad\quad\quad\quad \theta\leftarrow\theta+\alpha_\mu\hat g_\theta \\
\quad\quad\quad\quad \text{Soft-update target networks:} \\
\quad\quad\quad\quad \hat\theta\leftarrow\tau\theta+(1-\tau)\hat\theta \\
\quad\quad\quad\quad \hat\phi\leftarrow\tau\phi+(1-\tau)\hat\phi \\
\quad\quad\quad\quad \textbf{If }d_t=1\textbf{, break the time-step loop} \\
\quad\quad \textbf{End for} \\
\textbf{End for}
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Algorithm 1. DDPG" label="algorithm:ddpg" math=ddpg_algorithm %}

### DQN과 달라지는 지점

Replay buffer와 target network를 이용한 안정화는 DQN에서 이어진 공통점이다. DQN과 달라지는 핵심은 다음 세 가지다.

1. **Action selection**: DQN은 discrete action space에서 {::nomarkdown}\(a_t=\operatorname*{arg\,max}_aQ(s_t,a;\theta)\){:/nomarkdown}처럼 Q값이 가장 큰 action을 선택한다. DDPG는 online actor가 {::nomarkdown}\(a_t=\mu_\theta(s_t)\){:/nomarkdown}를 직접 출력하고, 학습 데이터를 수집할 때는 {::nomarkdown}\(a_t=\mu_\theta(s_t)+N_t\){:/nomarkdown}처럼 외부 exploration noise를 더한다.
2. **Critic target**: DQN은 next state에서 가능한 action의 최댓값을 사용해 $y=r+\gamma\max_a\hat Q(s',a;\hat\theta)$를 만든다. DDPG는 target actor가 continuous action $\mu_{\hat\theta}(s')$를 먼저 선택하고, target critic이 그 action을 평가해 $y=r+\gamma(1-d)Q_{\hat\phi}(s',\mu_{\hat\theta}(s'))$를 계산한다. 여기서 $\hat\theta,\hat\phi$는 generic estimate를 뜻하는 기호가 아니라 target network의 parameter이다.
3. **Actor update**: DQN에는 별도의 actor가 없으므로 Q-network만 update한다. DDPG는 actor도 따로 update하며, critic이 제공하는 $\nabla_aQ_\phi$를 actor의 $\nabla_\theta\mu_\theta$까지 chain rule로 backpropagation하여 $\nabla_\theta J$를 계산한다.

## 06_Trust Region Policy Optimization (TRPO)

앞에서 본 것처럼 DDPG는 continuous action space를 다룰 수 있지만, 매 update마다 성능이 monotonically 좋아진다는 보장은 없다. TRPO는 DDPG의 직접적인 확장이나 수정판이라기보다, policy 변화량을 제한해 update를 안정화하는 별도의 on-policy 방법으로 비교해 볼 수 있다.

### DDPG와 TRPO 비교

두 방법 모두 actor를 학습하지만 policy와 data 사용 방식, update 방식이 다르다.

| 구분 | DDPG | TRPO |
| --- | --- | --- |
| Policy / data | Deterministic policy, off-policy replay buffer | Typically stochastic policy, on-policy fresh trajectories |
| Exploration | Actor action에 external noise 추가 | Stochastic policy에서 action sampling |
| Stability mechanism | Replay buffer와 target network로 critic target 안정화 | KL trust region으로 policy update 제한 |
| Update characteristic / monotonicity | Critic gradient를 통한 actor update, 성능의 단조 증가 보장 없음 | Constrained surrogate update, 이론적 단조 증가 관점은 있으나 practical guarantee는 절대적이지 않음 |
{: .policy-comparison-table}

### TRPO의 핵심 아이디어

![Line search와 trust region의 직관을 비교한 그림](/assets/img/blog/deep-reinforcement-learning-summary-6/trpo-line-search-trust-region.png)

정책을 제한 없이 크게 update하면 gradient의 noise나 approximation error 때문에 성능이 매우 나쁜 영역으로 이동할 수 있다. 반대로 step size를 너무 작게 설정하면 안정적이지만 학습이 지나치게 느려진다. 그림에서 왼쪽의 line search는 이런 trade-off를 보여준다.

TRPO는 한 번의 update에서 policy가 바뀔 수 있는 범위를 제한하고, 그 trust region 안에서 local surrogate가 비교적 신뢰할 수 있는 방향을 찾는다. 다만 산과 경로는 직관을 위한 비유일 뿐이다. 실제 trust region은 물리적 공간이나 parameter의 Euclidean movement가 아니라, old policy와 new policy의 action distribution 사이 KL divergence를 제한하는 조건이다.

TRPO는 다음 두 아이디어를 결합한다.

1. **Minorization–Maximization (MM)**: 현재 policy의 expected return에 닿는 lower-bound surrogate를 만들고, 이 surrogate를 개선하는 방향으로 update한다.
2. **Trust region**: old policy와 new policy의 action distribution 사이 KL divergence를 제한해 policy가 한 번에 너무 크게 바뀌지 않도록 한다. Parameter의 Euclidean distance보다 실제 policy distribution의 변화를 제한하는 방식이다.

이론적으로는 valid한 lower bound를 개선하므로 monotonic improvement를 설명할 수 있다. 다만 practical TRPO는 sampled trajectory와 average KL 같은 근사를 사용하고, $\delta$와 line search로 step size를 여전히 조절하므로 모든 update의 성능 향상이 절대적으로 보장되지는 않는다. 따라서 전역 최적점이나 국소 최적점에 도달한다는 보장도 아니다.

이 과정에는 Hessian/Fisher-vector product를 conjugate gradient로 계산하는 단계와 line search가 필요해 구현과 computation cost가 크다. 그렇다고 CNN이나 RNN을 사용할 수 없는 것은 아니다. 원 논문도 CNN을 사용했으며, RNN도 가능하지만 관련 계산과 구현이 더 까다로운 일이다.

[TRPO 원 논문](https://proceedings.mlr.press/v37/schulman15.html)

## 07_TRPO의 Policy Improvement 이론

TRPO의 목표는 새로운 policy의 expected return을 old policy의 advantage로 표현하는 것이다. 여기서 policy $\pi$의 목적함수는 reward를 maximize하는 expected return으로 정의한다.

$$
\eta(\pi)
=
\mathbb{E}_{\tau\sim\pi}
\left[\sum_{t=0}^{\infty}\gamma^t r(s_t)\right],
\qquad 0\le\gamma<1
$$

여기서 trajectory $\tau=(s_0,a_0,s_1,a_1,\ldots)$는 policy $\pi$로 생성된 상태-행동 sequence이며, 모든 policy는 같은 initial-state distribution $s_0\sim\rho_0$에서 시작한다고 하자.

### 1. Expected Return을 Old Policy Advantage로 표현

#### Trajectory Expectation으로 Performance Difference 증명

보이고 싶은 performance-difference identity는 다음과 같다.

$$
\eta(\pi)
=
\eta(\pi_{\mathrm{old}})
+
\mathbb{E}_{\tau\sim\pi}
\left[
\sum_{t=0}^{\infty}
\gamma^t A_{\pi_{\mathrm{old}}}(s_t,a_t)
\right]
$$

중요한 점은 trajectory는 새로운 policy $\pi$로 sampling하지만, advantage는 old policy $\pi_{\mathrm{old}}$를 기준으로 계산한다는 것이다. 이를 위해 먼저 old-policy advantage를 Bellman 식으로 다시 쓴다.

$$
\begin{aligned}
A_{\pi_{\mathrm{old}}}(s_t,a_t)
&=Q_{\pi_{\mathrm{old}}}(s_t,a_t)-V_{\pi_{\mathrm{old}}}(s_t)\\
&=r(s_t)
+\gamma\mathbb{E}_{s_{t+1}\sim P(\cdot\mid s_t,a_t)}
\left[V_{\pi_{\mathrm{old}}}(s_{t+1})\right]
-V_{\pi_{\mathrm{old}}}(s_t).
\end{aligned}
$$

두 번째 줄은 $Q_{\pi_{\mathrm{old}}}(s_t,a_t)$의 Bellman expectation 식에서 나온다. 즉, action $a_t$를 수행하면 immediate reward $r(s_t)$를 받고, 다음 state에서 old policy를 따를 때의 value에 discount factor $\gamma$가 곱해진다. transition expectation은 가능한 모든 $s_{t+1}$에 대한 transition probability를 적분하거나 합산하는 항이다. 여기서는 강의의 표기에 따라 reward를 $r(s_t)$로 썼으며, 일반적인 MDP에서는 $r(s_t,a_t)$로 쓸 수도 있다.

이를 trajectory expectation에 대입하면 다음과 같이 정리된다.

$$
\begin{aligned}
&\mathbb{E}_{\tau\sim\pi}
\left[
\sum_{t=0}^{\infty}\gamma^t
 A_{\pi_{\mathrm{old}}}(s_t,a_t)
\right]\\
&=\mathbb{E}_{\tau\sim\pi}
\left[
\sum_{t=0}^{\infty}\gamma^t r(s_t)
 +\sum_{t=0}^{\infty}\gamma^{t+1}V_{\pi_{\mathrm{old}}}(s_{t+1})
 -\sum_{t=0}^{\infty}\gamma^tV_{\pi_{\mathrm{old}}}(s_t)
\right]\\
&=\eta(\pi)
 +\mathbb{E}_{\tau\sim\pi}
\left[
\sum_{t=0}^{\infty}\gamma^{t+1}V_{\pi_{\mathrm{old}}}(s_{t+1})
 -\sum_{t=0}^{\infty}\gamma^tV_{\pi_{\mathrm{old}}}(s_t)
\right]\\
&=\eta(\pi)
 -\mathbb{E}_{s_0}
 \left[V_{\pi_{\mathrm{old}}}(s_0)\right]\\
&=\eta(\pi)-\eta(\pi_{\mathrm{old}}).
\end{aligned}
$$

각 변형이 성립하는 이유를 순서대로 보면 다음과 같다.

1. Objective definition에 의해
   {::nomarkdown}\(\mathbb{E}_{\tau\sim\pi}[\sum_{t=0}^{\infty}\gamma^t r(s_t)]=\eta(\pi)\){:/nomarkdown}이다.
2. Positive value sum의 index를 reindex하면 $\sum_{t=0}^{\infty}\gamma^{t+1}V_{\pi_{\mathrm{old}}}(s_{t+1})=\sum_{t=1}^{\infty}\gamma^tV_{\pi_{\mathrm{old}}}(s_t)$이다. 
   따라서 $\sum_{t=0}^{\infty}\gamma^tV_{\pi_{\mathrm{old}}}(s_t)$에서 $t\ge1$인 항은 모두 소거되고 $-V_{\pi_{\mathrm{old}}}(s_0)$만 남는다.
   여기서 $V_{\pi_{\mathrm{old}}}$가 bounded이고 $\gamma<1$이므로 tail도 0으로 사라진다.
3. 바깥 expectation은 $\tau\sim\pi$에 대해 취하지만, 남은 항은 $s_0$에만 의존한다. 모든 policy가 같은 $s_0\sim\rho_0$에서 시작하므로
   {::nomarkdown}\(\mathbb{E}_{\tau\sim\pi}[V_{\pi_{\mathrm{old}}}(s_0)]=\mathbb{E}_{s_0}[V_{\pi_{\mathrm{old}}}(s_0)]=\eta(\pi_{\mathrm{old}})\){:/nomarkdown}이다.

따라서 최종적으로

$$
\boxed{
\eta(\pi)-\eta(\pi_{\mathrm{old}})
=
\mathbb{E}_{\tau\sim\pi}
\left[
\sum_{t=0}^{\infty}
\gamma^t A_{\pi_{\mathrm{old}}}(s_t,a_t)
\right]
}
$$

를 얻는다. 즉, 새로운 policy $\pi$의 trajectory에서 old policy 기준 advantage의 discounted expectation이 양수이면 $\pi$의 expected return이 $\pi_{\mathrm{old}}$보다 높다.

#### State Visitation Frequency로 표현

앞에서 증명한 identity에서 출발하자.

$$
\eta(\pi)
=\eta(\pi_{\mathrm{old}})
+\mathbb{E}_{\tau\sim\pi}
\left[
\sum_{t=0}^{\infty}
\gamma^t A_{\pi_{\mathrm{old}}}(s_t,a_t)
\right].
$$

$t$를 고정하면 discrete state/action space에서 한 시점의 expectation은

$$
\mathbb{E}_{\tau\sim\pi}
\left[A_{\pi_{\mathrm{old}}}(S_t,A_t)\right]
=\sum_s P(S_t=s\mid\pi)
\sum_a \pi(a\mid s)A_{\pi_{\mathrm{old}}}(s,a)
$$

로 쓸 수 있다. 즉, time stamp $t$를 고정한 뒤 새로운 policy $\pi$를 따를 때 그 시점에 방문하는 모든 state와, 각 state에서 새로운 policy가 선택하는 모든 action에 대해 old-policy advantage를 평균낸다. 그런 다음 각 time stamp의 expectation에 $\gamma^t$를 곱하고 모든 time stamp에 대해 합산한다.

이제 trajectory expectation을 시점별 state/action expectation으로 전개하면

$$
\begin{aligned}
&\mathbb{E}_{\tau\sim\pi}
\left[
\sum_{t=0}^{\infty}
\gamma^t A_{\pi_{\mathrm{old}}}(s_t,a_t)
\right]\\
&=\sum_{t=0}^{\infty}\gamma^t
\sum_s P(S_t=s\mid\pi)
\sum_a \pi(a\mid s)A_{\pi_{\mathrm{old}}}(s,a)\\
&=\sum_s
\left[\sum_{t=0}^{\infty}\gamma^tP(S_t=s\mid\pi)\right]
\sum_a \pi(a\mid s)A_{\pi_{\mathrm{old}}}(s,a)\\
&=\sum_s \rho_\pi(s)
\sum_a \pi(a\mid s)A_{\pi_{\mathrm{old}}}(s,a).
\end{aligned}
$$

여기서 summation의 순서를 바꾼 것은 expectation의 linearity와 수렴하는 discounted sum의 재배열에 따른 것이다. 별도의 measure theory를 사용할 필요는 없다. Section 03에서 정의한 discounted state visitation frequency는

$$
\rho_\pi(s)
=\sum_{t=0}^{\infty}\gamma^tP(S_t=s\mid\pi)
$$

이며, 이는 policy $\pi$가 state $s$를 방문하는 횟수를 discount하여 합친 unnormalized discounted state visitation frequency이다. Continuous state/action space에서는 각각의 summation을 corresponding integral로 바꾸면 된다. 따라서 최종적으로

$$
\boxed{
\eta(\pi)
=\eta(\pi_{\mathrm{old}})
+\sum_s\rho_\pi(s)\sum_a\pi(a\mid s)A_{\pi_{\mathrm{old}}}(s,a)
}
$$

를 얻는다. 즉, performance improvement는 새로운 policy가 선택하는 action의 old-policy advantage expectation에 각 state를 새로운 policy가 얼마나 자주 방문하는지를 가중한 값이다.

#### Monotonic Improvement 조건

여기서 $\rho_\pi(s)$는 normalized probability가 아니라 unnormalized discounted state visitation frequency이지만, $\gamma^tP(S_t=s\mid\pi)$의 합이므로 항상 nonnegative이다. 상태별 advantage expectation을 $g_\pi(s)\mathrel{:=}\sum_a\pi(a\mid s)A_{\pi_{\mathrm{old}}}(s,a)$로 두면, 다음 조건은 performance가 감소하지 않기 위한 충분조건이다.

$$
g_\pi(s)\ge 0\ \ \text{for every }s\text{ with }\rho_\pi(s)>0
\quad\Longrightarrow\quad
\eta(\pi)-\eta(\pi_{\mathrm{old}})
=\sum_s\rho_\pi(s)g_\pi(s)\ge 0.
$$

방문 state 중 어떤 $s^\star$에서 $\rho_\pi(s^\star)>0$이고 $g_\pi(s^\star)>0$이며 나머지 statewise term도 모두 nonnegative이면 strict improvement가 된다. 다만 이 조건은 sufficient이지 necessary는 아니다. 일부 state에서 $g_\pi(s)<0$이어도 다른 state의 positive term이 visitation weight를 적용한 뒤 더 크면 전체 합은 여전히 positive일 수 있다.

이는 exact mathematics에서의 결론이다. 실제 구현에서는 모든 state/action의 값을 정확히 계산할 수 없어 sampled trajectory, approximate value/advantage function, finite data를 사용한다. 따라서 estimated advantage의 sign이 실제와 달라질 수 있고, statewise 조건을 만족한다고 추정해도 true performance가 하락할 수 있다. TRPO가 policy change를 trust region의 KL bound 안에 제한하는 이유가 여기에 있다.

#### Direct Optimization이 어려운 이유

정확한 performance-difference 식을 직접 optimize하기 어려운 이유는 $\rho_\pi(s)$ 자체가 새로운 policy $\pi$를 따른 전체 future trajectory와 state distribution에 의존하기 때문이다. $\pi$를 바꾸면 action probability뿐 아니라 앞으로 방문할 state도 함께 바뀌므로 두 항 사이에 복잡한 dependency가 생긴다. TRPO의 local surrogate는 이를 완화하기 위해 새로운 visitation $\rho_\pi$를 old-policy visitation $\rho_{\pi_{\mathrm{old}}}$로 대체하고, old-policy trajectory에서 이를 추정한다. 또한 작은 KL trust region으로 두 visitation distribution의 mismatch를 제한한다.

### 2. Local Approximation

앞에서 얻은 exact performance-difference 식은 다음과 같다.

$$
\eta(\pi)=\eta(\pi_{\mathrm{old}})
+\sum_s\rho_\pi(s)\sum_a\pi(a\mid s)A_{\pi_{\mathrm{old}}}(s,a).
$$

새 policy에 의존하는 state visitation $\rho_\pi$를 old policy의 visitation으로 바꾸면 local surrogate를 정의할 수 있다.

$$
L_{\pi_{\mathrm{old}}}(\pi)
=\eta(\pi_{\mathrm{old}})
+\sum_s\rho_{\pi_{\mathrm{old}}}(s)\sum_a\pi(a\mid s)A_{\pi_{\mathrm{old}}}(s,a).
$$

이렇게 하면 $\rho_\pi$가 새로운 $\pi$에 복잡하게 의존하는 문제가 사라진다. $\rho_{\pi_{\mathrm{old}}}$는 old-policy로 수집한 trajectory에서 추정할 수 있으므로 실제 optimize가 가능해진다.

이제 policy를 미분 가능한 parameterized policy $\pi_\theta$로 쓰고, old policy를 $\pi_{\theta_0}$로 두자. 편의를 위해

$$
L_{\theta_0}(\theta)\mathrel{:=} L_{\pi_{\theta_0}}(\pi_\theta)
$$

로 표기한다. 같은 policy를 대입한 matching point $\theta=\theta_0$에서는 statewise expected old advantage가

$$
\sum_a\pi_{\theta_0}(a\mid s)A_{\pi_{\theta_0}}(s,a)
=\sum_a\pi_{\theta_0}(a\mid s)Q_{\pi_{\theta_0}}(s,a)-V_{\pi_{\theta_0}}(s)
=V_{\pi_{\theta_0}}(s)-V_{\pi_{\theta_0}}(s)=0
$$

이므로

$$
L_{\theta_0}(\theta_0)=\eta(\theta_0)
$$

가 된다. 또한 $f_\theta(s)\mathrel{:=}\sum_a\pi_\theta(a\mid s)A_{\pi_{\theta_0}}(s,a)$라고 하면 $f_{\theta_0}(s)=0$이다. Exact expression을 $\theta$에 대해 미분하면

$$
\left.\nabla_\theta\eta(\theta)\right\vert_{\theta=\theta_0}
=\sum_s\left[\left.\nabla_\theta\rho_{\pi_\theta}(s)\right\vert_{\theta=\theta_0}f_{\theta_0}(s)
+\rho_{\pi_{\theta_0}}(s)\left.\nabla_\theta f_\theta(s)\right\vert_{\theta=\theta_0}\right].
$$

첫 번째 항은 $f_{\theta_0}(s)=0$ 때문에 사라지고, 남는 항은 local surrogate의 gradient와 같다.

$$
\left.\nabla_\theta L_{\theta_0}(\theta)\right\vert_{\theta=\theta_0}
=\left.\nabla_\theta\eta(\theta)\right\vert_{\theta=\theta_0}.
$$

즉, $L$은 matching point에서 $\eta$와 같은 value와 gradient를 가지므로 $\eta$의 first-order local approximation이다. 따라서 positive directional derivative를 따라 충분히 작은 step을 취하면 $L$의 improvement가 local하게 $\eta$의 improvement로 이어진다. 반면 큰 step에서는 higher-order difference와 달라진 visitation $\rho_\pi$ 때문에 이 근사가 깨질 수 있으므로, TRPO는 KL trust region으로 policy step을 제한한다.

### 3. Conservative Policy Iteration의 Policy Improvement Bound

Local approximation은 sufficiently small step에서 $L$의 개선이 expected return $\eta$의 개선으로 이어진다는 점을 설명하지만, step을 얼마나 크게 취해도 되는지는 알려주지 않는다. Conservative Policy Iteration(CPI)은 이 문제에 대해 improved candidate policy와 old policy를 섞어 policy change를 보수적으로 만드는 explicit guidance를 제공한다. 먼저 local surrogate를 가장 크게 만드는 candidate를

$$
\pi'=\operatorname*{arg\,max}_{\pi}L_{\pi_{\mathrm{old}}}(\pi)
$$

로 정의한다. 그런 다음 실제 update policy를 다음 mixture로 둔다.

$$
\pi_{\mathrm{new}}(a\mid s)
=(1-\alpha)\pi_{\mathrm{old}}(a\mid s)
+\alpha\pi'(a\mid s),
\qquad \alpha\in[0,1].
$$

$\alpha=0$이면 old policy를 그대로 유지하고, $\alpha=1$이면 candidate policy로 fully switch한다. 그 사이의 값은 candidate를 일부만 반영하는 conservative update이며, step size 역할을 한다.

CPI는 다음과 같은 reward-form lower bound를 제공한다.

$$
\eta(\pi_{\mathrm{new}})
\ge
L_{\pi_{\mathrm{old}}}(\pi_{\mathrm{new}})
-\frac{2\epsilon\gamma}{(1-\gamma)^2}\alpha^2,
$$

where

$$
\epsilon
=\max_s
\left|
\mathbb{E}_{a\sim\pi'(\cdot\mid s)}
\left[A_{\pi_{\mathrm{old}}}(s,a)\right]
\right|.
$$

즉, surrogate improvement에서 policy mixture 때문에 생기는 mismatch를 quadratic penalty로 빼어도 실제 return의 lower bound가 남는다. 따라서 $\alpha$가 커질수록 penalty가 $\alpha^2$에 비례해 빠르게 증가하고, $\gamma\to1$이면 coefficient $2\epsilon\gamma/(1-\gamma)^2$가 커져 long-horizon에서 누적되는 visitation mismatch의 영향이 더 커진다. $\epsilon$은 모든 state에서 candidate policy가 만드는 expected old-policy advantage의 magnitude 중 최댓값인 worst-case quantity이다.

하지만 이 bound를 그대로 practical deep-RL update에 사용하기는 어렵다. 우선 large 또는 continuous state space에서는 모든 state에 대한 exact maximum을 계산하는 것이 어렵거나 불가능하다. 또한 {::nomarkdown}\(\pi'=\operatorname*{arg\,max}_{\pi}L_{\pi_{\mathrm{old}}}(\pi)\){:/nomarkdown}를 정확히 구하는 일과, 그 candidate와 old policy의 mixture를 반복적으로 표현하고 적용하는 일도 까다로운 일이다. {::nomarkdown}\(\epsilon\){:/nomarkdown}, {::nomarkdown}\(\rho_{\pi_{\mathrm{old}}}\){:/nomarkdown}, advantage 등 bound에 필요한 quantities 역시 finite samples와 function approximation만으로 정확히 알기 어렵다. 따라서 CPI는 step size가 왜 중요하고 어떤 penalty가 생기는지 이론적으로 보여주지만, 그대로 구현하기에는 어려운 점이 많이 존재한다.

### 4. General Stochastic Policy로 확장

CPI의 mixture update는 new policy가 old policy와 candidate policy의 convex combination이어야 한다는 점에서 restrictive하다. 따라서 policy를 이 mixture 형태로 제한하지 않고, arbitrary한 general stochastic old/new policy 사이의 policy distance를 사용해 policy-improvement bound를 확장한다.

Subsection 3에서 $\alpha$는 선택하는 mixture ratio, 즉 tunable한 step size였다. 여기서는 이를 policy distribution 사이의 worst-case distance로 새롭게 정의한다.

$$
\alpha
=D_{\mathrm{TV}}^{\max}(\pi_{\mathrm{old}},\pi)
=\max_sD_{\mathrm{TV}}
\left(\pi_{\mathrm{old}}(\cdot\mid s)\,\|\,\pi(\cdot\mid s)\right).
$$

Discrete action space에서 total variation distance는

$$
D_{\mathrm{TV}}(p\|q)
=\frac{1}{2}\sum_a\left|p(a)-q(a)\right|
$$

로 정의한다. 여기서 $\alpha$는 모든 state에서의 policy-distribution change 중 최댓값을 나타내며, 이 subsection에서 mixture coefficient로 조절하는 hyperparameter가 아니다. 또한 advantage의 worst-case magnitude를

$$
\epsilon=\max_{s,a}\left|A_{\pi_{\mathrm{old}}}(s,a)\right|
$$

로 두면, reward-maximization에 대한 policy-improvement bound는

$$
\eta(\pi)
\ge
L_{\pi_{\mathrm{old}}}(\pi)
-\frac{4\epsilon\gamma}{(1-\gamma)^2}\alpha^2
$$

가 된다. 즉, surrogate improvement에서 policy distance로 인한 mismatch penalty를 뺀 값이 true expected return의 lower bound이다. Worst-case TV distance가 커질수록 penalty는 quadratic하게 증가하고, $\gamma\to1$이면 coefficient $4\epsilon\gamma/(1-\gamma)^2$가 커져 long-horizon에서 bound가 더 느슨해진다.

이제 TV distance를 KL divergence로 바꿀 수 있다. 강의와 논문의 derivation에서 사용하는 다음의 충분조건은

$$
D_{\mathrm{TV}}(p\|q)^2\le D_{\mathrm{KL}}(p\|q)
$$

이다. State별 KL divergence의 최댓값을

$$
D_{\mathrm{KL}}^{\max}(\pi_{\mathrm{old}},\pi)
=\max_sD_{\mathrm{KL}}
\left(\pi_{\mathrm{old}}(\cdot\mid s)\,\|\,\pi(\cdot\mid s)\right)
$$

로 정의하면 $\alpha^2\le D_{\mathrm{KL}}^{\max}(\pi_{\mathrm{old}},\pi)$이므로, $C=4\epsilon\gamma/(1-\gamma)^2$에 대해

$$
\eta(\pi)
\ge
L_{\pi_{\mathrm{old}}}(\pi)
-C D_{\mathrm{KL}}^{\max}(\pi_{\mathrm{old}},\pi)
$$

를 얻는다. 따라서 general stochastic policy에서는 이 lower bound를 maximize할 때 surrogate improvement와 policy-distance penalty 사이의 balance가 중요하다. 이는 mixture update에 의존하지 않는 MM/policy-improvement reasoning을 제공한다. 다만 실제로는 모든 state에 대한 maximum을 계산해야 한다는 어려움이 남으며, 다음 trust-region approximation에서 이를 다룰 수 있다. 여기서는 아직 average KL로 바꾸어 유도하지 않는다.

### 5. Minorization–Maximization Algorithm

{% capture trpo_mm_callout %}
Minorization–Maximization(MM) algorithm은 매 iteration마다 current policy $\pi_i$ 주변에서 objective $\eta$보다 다루기 쉬운 surrogate minorizer를 만들고, 그 surrogate를 optimize해 더 나은 policy/parameter를 찾는 iterative method이다.

Iteration $i$에서 current policy $\pi_i$에 맞추어 $M_i(\pi)$를 구성한다. $M_i$는 모든 policy에서 $\eta$의 lower bound이고, current point에서는 objective와 touch한다.

$$
M_i(\pi)\le\eta(\pi)\quad\text{for every }\pi,
\qquad
M_i(\pi_i)=\eta(\pi_i),
$$

또한 $M_i$는 $\eta$보다 optimize하기 쉽다. Surrogate의 maximizer를 next policy로 update한다.

$$
\pi_{i+1}=\operatorname*{arg\,max}_{\pi}M_i(\pi).
$$

그러면

$$
\eta(\pi_{i+1})
\ge M_i(\pi_{i+1})
\ge M_i(\pi_i)
=\eta(\pi_i)
$$

이다. 첫 번째 부등식은 $M_i$가 lower bound이기 때문이고, 두 번째 부등식은 $\pi_{i+1}$가 $M_i$를 maximize했기 때문이다. 마지막 등식은 $M_i$가 $\pi_i$에서 $\eta$에 touch한다는 조건에서 나온다. 이후 $\pi_{i+1}$에서 $M_{i+1}$를 다시 만들고 같은 과정을 반복한다.
{% endcapture %}

{% include callout.html type="idea" title="Minorization–Maximization(MM) Algorithm이란?" content=trpo_mm_callout %}

아래 animation은 MM의 monotonic improvement를 $\theta$ 공간에서 보여준다. Blue curve는 true objective $\eta(\theta)$, orange curve는 current iterate에서 만든 surrogate $M_i(\theta)$이며, 각 surrogate는 current iterate에서 true objective에 touch하고 그 maximizer가 next iterate가 된다. Animation은 scalar parameter $\theta$를 사용하지만, same idea applies to policy $\pi$에도 적용된다.

![MM optimization의 monotonic improvement를 보여주는 animation](/assets/img/blog/deep-reinforcement-learning-summary-6/mm-optimization.gif)

#### MM Algorithm을 TRPO Bound에 적용

Subsection 4에서 얻은 general stochastic policy bound를 MM surrogate(minorizer)로 사용하자. Iteration $i$에서 old policy를 $\pi_i$로 두고 다음과 같이 정의한다.

$$
M_i(\pi)
=L_{\pi_i}(\pi)-C_iD_{\mathrm{KL}}^{\max}(\pi_i,\pi),
$$

where

$$
L_{\pi_i}(\pi)
=\eta(\pi_i)
+\sum_s\rho_{\pi_i}(s)\sum_a\pi(a\mid s)A_{\pi_i}(s,a),
$$

$$
\epsilon_i=\max_{s,a}\left|A_{\pi_i}(s,a)\right|,
\qquad
C_i=\frac{4\epsilon_i\gamma}{(1-\gamma)^2}.
$$

Lecture에서는 iteration이 명확할 때 $C_i$를 간단히 $C$로 표기하기도 한다.

먼저 $M_i$가 $\pi_i$에서 objective에 touch하는지 확인한다. 같은 policy 사이의 KL divergence는 0이므로

$$
D_{\mathrm{KL}}^{\max}(\pi_i,\pi_i)=0.
$$

또한 각 state에서 advantage의 정의에 의해

$$
\sum_a\pi_i(a\mid s)A_{\pi_i}(s,a)=0,
$$

이므로 $L_{\pi_i}(\pi_i)=\eta(\pi_i)$이다. 따라서

$$
M_i(\pi_i)=\eta(\pi_i).
$$

Subsection 4의 general stochastic policy bound에 따르면, bound가 적용되는 모든 policy $\pi$에 대해

$$
\eta(\pi)\ge M_i(\pi)
$$

이다. 즉, $M_i$는 $\eta$의 global lower bound이면서 현재 policy $\pi_i$에서 $\eta$와 일치하는 surrogate objective이다.

이제 surrogate를 maximize하여 next policy를 정한다.

$$
\pi_{i+1}=\operatorname*{arg\,max}_{\pi}M_i(\pi).
$$

그러면 다음의 monotonic improvement chain을 얻는다.

$$
\boxed{
\eta(\pi_i)=M_i(\pi_i)
\le M_i(\pi_{i+1})
\le \eta(\pi_{i+1})
}
$$

첫 번째 등식은 $\pi_i$에서의 touching property에서 나온다. 첫 번째 부등식은 $\pi_{i+1}$가 $M_i$의 maximizer이기 때문이고, 두 번째 부등식은 $M_i$가 $\eta$의 lower bound이기 때문이다. 따라서 idealized exact MM update는

$$
\eta(\pi_{i+1})\ge\eta(\pi_i)
$$

를 보장하며, 매 iteration마다 policy performance가 monotonic하게 향상된다. Practical TRPO에서는 max KL과 expectation을 sample-based approximation으로 계산한다.

#### Parameterized MM Update의 Practical 문제

앞의 MM 적용에서 유도한 것은 idealized하고 theoretically justified한 MM policy update이다. 따라서 아직 practical TRPO algorithm 자체는 아니다. Policy를 $\pi_\theta$로 parameterize하고, old parameter를 $\theta_{\mathrm{old}}$로 표기하자. 편의를 위해 $\eta(\theta)=\eta(\pi_\theta)$, $L_{\theta_{\mathrm{old}}}(\theta)=L_{\pi_{\theta_{\mathrm{old}}}}(\pi_\theta)$로 쓰면 bound는

$$
\eta(\theta)
\ge
L_{\theta_{\mathrm{old}}}(\theta)
-C D_{\mathrm{KL}}^{\max}(\theta_{\mathrm{old}},\theta),
\qquad
\text{with equality at } \theta=\theta_{\mathrm{old}},
$$

이다. 여기서 theoretical constant는

$$
C=\frac{4\epsilon\gamma}{(1-\gamma)^2},
\qquad
\epsilon=\max_{s,a}|A_{\pi_{\theta_{\mathrm{old}}}}(s,a)|
$$

이다. 그러므로 ideal MM update는 current surrogate의 maximum을 찾아

$$
\theta_{\mathrm{new}}
=
\operatorname*{arg\,max}_{\theta}
\left[
L_{\theta_{\mathrm{old}}}(\theta)
-C D_{\mathrm{KL}}^{\max}(\theta_{\mathrm{old}},\theta)
\right]
$$

로 정하는 과정이다. 하지만 이 update가 찾는 것은 current surrogate(minorizer)의 maximum뿐이다. 따라서 $\theta_{\mathrm{new}}$를 얻은 뒤에는 이를 새로운 old parameter로 삼아 surrogate를 다시 만들고, 매 outer iteration마다 inner maximization을 다시 풀어야 한다.

이처럼 $C D_{\mathrm{KL}}^{\max}$를 objective 안에 직접 두면 surrogate improvement와 nonlinear worst-case KL penalty가 하나의 최적화 문제에서 coupling되어 penalized problem 자체를 안정적으로 optimize하기 어렵고, penalty의 크기를 결정하는 $C$를 미리 정해 tuning하기도 어렵다. KL을 objective 밖의 explicit constraint로 분리하면 reward improvement와 허용할 policy change를 따로 조절할 수 있고, 뒤에서 사용할 local constrained approximation으로도 자연스럽게 이어진다.

이 idealized formulation에는 다음과 같은 practical 문제가 있다. 먼저 exact inner maximization 자체가 computationally expensive하다. 또한 $D_{\mathrm{KL}}^{\max}$는 모든 state에 대한 worst-case KL divergence를 계산해야 하므로 실제 환경에서 직접 평가하기 어렵다. 더구나 $\gamma\approx1$이면

$$
C=\frac{4\epsilon\gamma}{(1-\gamma)^2}
$$

가 매우 커질 수 있다. 여기서 $\epsilon$도 worst-case advantage라서 penalty가 더욱 보수적으로 커지고, surrogate objective에서 KL penalty가 improvement term을 압도할 수 있다. 이 큰 penalty를 피하려면 $\theta$가 policy space에서 $\theta_{\mathrm{old}}$에 매우 가까이 있어야 하므로, step이 지나치게 작고 conservative해져 learning이 느려진다.

이 문제들을 해결하기 위해 practical TRPO에서는 fixed theoretical KL penalty를 그대로 optimize하는 대신, chosen radius $\delta$를 사용하는 explicit trust-region KL constraint로 전환한다.

### 6. Trust Region Constraint

앞 절의 ideal MM update에서 optimize하는

$$
\max_{\theta}
\left[
L_{\theta_{\mathrm{old}}}(\theta)
-CD_{\mathrm{KL}}^{\max}(\theta_{\mathrm{old}},\theta)
\right]
$$

를 KL-penalized objective라고 부른다. 하지만 $\gamma\approx1$이거나 worst-case advantage bound인 $\epsilon$이 큰 경우 theoretical constant $C$가 매우 커질 수 있다. 그러면 KL penalty가 surrogate improvement를 압도하여 update가 지나치게 작아진다. Useful하면서도 controlled한 larger step을 얻기 위해, fixed penalty 대신 다음 KL-constrained objective를 사용한다.

$$
\max_{\theta}\ L_{\theta_{\mathrm{old}}}(\theta)
\qquad\text{subject to}\qquad
D_{\mathrm{KL}}^{\max}(\theta_{\mathrm{old}},\theta)\le\delta.
$$

여기서 $\delta$는 trust-region radius로서 old policy와 new policy의 action distribution이 state별로 얼마나 달라질 수 있는지를 제한한다. 이처럼 theoretical penalty coefficient $C$ 대신 KL radius $\delta$를 직접 지정하면 update size를 더 직관적으로 해석하고 비교적 쉽게 tuning할 수 있다. 다만 constraint를 도입했다고 해서 별도의 tuning이 불필요해지는 것은 아니다. $\delta$ 역시 적절히 선택해야 하는 hyperparameter이며, 너무 작으면 update가 지나치게 보수적이고 너무 크면 policy 변화가 커질 수 있다.

구체적으로,

$$
D_{\mathrm{KL}}^{\max}(\pi_{\mathrm{old}},\pi)
=\max_s D_{\mathrm{KL}}\bigl(\pi_{\mathrm{old}}(\cdot\mid s)\,\|\,\pi(\cdot\mid s)\bigr)\le\delta
$$

는 모든 state $s$에 대해 $D_{\mathrm{KL}}(\pi_{\mathrm{old}}(\cdot\mid s)\|\pi(\cdot\mid s))\le\delta$가 성립해야 한다는 뜻이다. 따라서 large/continuous state space에서는 모든 state를 열거하고 확인할 수 없어 이 worst-case constraint를 직접 만족시키기 어렵다. 특히 대부분의 state에서 KL이 작더라도 단 하나의 rare 또는 outlier state에서 KL이 크면 maximum이 그 state에 의해 결정되어, 전체적으로 유용한 update까지 reject될 수 있다. $\delta$ 자체가 의도적으로 작은 값이라는 점까지 고려하면, worst-case constraint는 실제 학습에서 지나치게 conservative해질 수 있다.

Penalty form과 constrained form은 Lagrangian 관점에서 연결된다. 예를 들어 constraint의 Lagrangian은

$$
\mathcal{L}(\theta,\lambda)
=L_{\theta_{\mathrm{old}}}(\theta)
-\lambda\left(
D_{\mathrm{KL}}^{\max}(\theta_{\mathrm{old}},\theta)-\delta
\right),
\qquad \lambda\ge0,
$$

로 쓸 수 있으므로, penalty coefficient $C$는 Lagrange multiplier와 같은 역할을 한다. 적절한 regularity assumption과 constraint qualification 아래에서는 두 formulation이 Lagrangian duality를 통해 관계를 갖는다. 그러나 neural policy optimization은 generally nonconvex이므로, 이 사실이 unconditional convergence나 두 objective의 exact equivalence를 보장하는 것은 아니다.

직관적으로는 fixed하고 매우 큰 $C$가 policy를 거의 움직이지 못하게 하는 대신, $\delta$를 직접 정해 명시적으로 bounded된 KL neighborhood 안에서 surrogate improvement가 가장 큰 policy를 찾는다. 따라서 excessive한 policy change는 막으면서도 useful한 larger step을 허용할 수 있다. 다만 모든 state에 대한 worst-case $D_{\mathrm{KL}}^{\max}$를 여전히 계산해야 하므로, practical TRPO에서는 다음 단계에서 이를 sampled average KL constraint로 대체한다.

### 7. Heuristic Approximation

앞서의 hard constraint

$$
D_{\mathrm{KL}}^{\max}(\pi_{\mathrm{old}},\pi_\theta)
=\max_sD_{\mathrm{KL}}
\left(\pi_{\mathrm{old}}(\cdot\mid s)\,\|\,\pi_\theta(\cdot\mid s)\right)
\le\delta
$$

는 모든 state에서 KL bound를 만족해야 하므로 large/continuous state space에서 직접 계산하기 어렵다. 따라서 practical TRPO에서는 worst-case maximum을 old policy의 normalized discounted visitation에 대한 average로 바꾸는 heuristic approximation을 사용한다.

$$
\max_{\theta}L_{\theta_{\mathrm{old}}}(\theta)
\qquad\text{subject to}\qquad
\mathbb{E}_{s\sim d_{\pi_{\mathrm{old}}}}
\left[
D_{\mathrm{KL}}\left(
\pi_{\mathrm{old}}(\cdot\mid s)\,\|\,\pi_\theta(\cdot\mid s)
\right)
\right]\le\delta.
$$

여기서 $d_{\pi_{\mathrm{old}}}(s)=(1-\gamma)\rho_{\pi_{\mathrm{old}}}(s)$는 Section 03에서 정의한 normalized discounted state-visitation probability이다. 강의나 논문에서는 expectation 안에서도 $\rho$를 probability처럼 overload하는 경우가 있지만, 이 post에서는 unnormalized measure인 $\rho$와 구분하기 위해 probability expectation에는 $d$를 사용한다. 이 relaxation은 old-policy trajectory에서 average KL을 쉽게 estimate할 수 있게 해 주지만, rare state에서 발생하는 큰 KL을 더 이상 control하지 못한다. 따라서 exact max-KL bound가 제공하던 theoretical guarantee도 약해진다.

### 8. Monte Carlo Simulation과 Sample-Based Estimation

Average-KL constraint를 실제 trajectory sample로 계산할 수 있는 형태로 차례대로 바꿔 보자.

1. 먼저 old visitation을 사용한 local surrogate를 전개한다. $L_{\theta_{\mathrm{old}}}(\theta)$의 앞부분인 $\eta(\theta_{\mathrm{old}})$는 $\theta$와 무관한 constant이므로, $\operatorname*{arg\,max}_\theta$를 찾을 때 제거할 수 있다.

$$
\max_{\theta}
\sum_s\rho_{\pi_{\mathrm{old}}}(s)
\sum_a\pi_\theta(a\mid s)A_{\pi_{\mathrm{old}}}(s,a)
$$

subject to

$$
\mathbb{E}_{s\sim d_{\pi_{\mathrm{old}}}}
\left[
D_{\mathrm{KL}}\left(
\pi_{\mathrm{old}}(\cdot\mid s)\,\|\,\pi_\theta(\cdot\mid s)
\right)
\right]\le\delta.
$$

2. Section 03의 normalized visitation 관계

$$
\sum_s\rho_{\pi_{\mathrm{old}}}(s)f(s)
=\frac{1}{1-\gamma}
\mathbb{E}_{s\sim d_{\pi_{\mathrm{old}}}}[f(s)]
$$

를 적용한다. $1/(1-\gamma)>0$는 positive constant이므로 argmax의 maximizing $\theta$를 바꾸지 않아 제거할 수 있다. 이제 old policy로 수집한 trajectory의 state samples를 사용해 state expectation을 estimate할 수 있다.

3. Advantage를 Q-value로 바꿔도 maximizing $\theta$는 변하지 않는다.

$$
\sum_a\pi_\theta(a\mid s)A_{\pi_{\mathrm{old}}}(s,a)
=\sum_a\pi_\theta(a\mid s)Q_{\pi_{\mathrm{old}}}(s,a)
-V_{\pi_{\mathrm{old}}}(s).
$$

마지막 항 $V_{\pi_{\mathrm{old}}}(s)$는 $\theta$와 무관한 state-dependent constant이므로 objective에서 제거해도 maximizing $\theta$에는 영향을 주지 않는다.

4. Collected action은 $\pi_{\mathrm{old}}$에서 sampling되지만 objective의 action expectation은 $\pi_\theta$ 아래에 있다. 따라서 importance sampling을 적용한다.

$$
\sum_a\pi_\theta(a\mid s)Q_{\pi_{\mathrm{old}}}(s,a)
=\mathbb{E}_{a\sim\pi_{\mathrm{old}}(\cdot\mid s)}
\left[
\frac{\pi_\theta(a\mid s)}{\pi_{\mathrm{old}}(a\mid s)}
Q_{\pi_{\mathrm{old}}}(s,a)
\right].
$$

이 식을 사용하려면 policy ratio가 정의되도록 $\pi_\theta(a\mid s)>0$인 action에 대해 $\pi_{\mathrm{old}}(a\mid s)>0$이어야 한다는 support 조건이 필요하다. Continuous action에서는 probability 대신 corresponding density ratio를 사용한다.

5. 위 변환은 다음의 일반적인 importance-sampling identity에 해당한다.

$$
\mathbb{E}_{x\sim p}[f(x)]
=\mathbb{E}_{x\sim q}
\left[\frac{p(x)}{q(x)}f(x)\right]
\approx
\frac{1}{N}\sum_{n=1}^{N}
\frac{p(x_n)}{q(x_n)}f(x_n),
\qquad x_n\sim q.
$$

같은 importance-sampling correction은 [요약 4의 Prioritized Experience Replay](/blog/2026/deep-reinforcement-learning-summary-4/#prioritized-experience-replay)에서도 등장하지만, 그곳은 replay sampling distribution을 보정하는 다른 application이며 현재 TRPO의 old/new policy ratio와 동일한 setup은 아니다.

6. 따라서 sample-estimable한 constrained objective는 다음과 같이 쓸 수 있다.

$$
\max_{\theta}
\mathbb{E}_{\substack{s\sim d_{\pi_{\mathrm{old}}}\\
a\sim\pi_{\mathrm{old}}(\cdot\mid s)}}
\left[
\frac{\pi_\theta(a\mid s)}{\pi_{\mathrm{old}}(a\mid s)}
Q_{\pi_{\mathrm{old}}}(s,a)
\right]
$$

subject to

$$
\mathbb{E}_{s\sim d_{\pi_{\mathrm{old}}}}
\left[
D_{\mathrm{KL}}\left(
\pi_{\mathrm{old}}(\cdot\mid s)\,\|\,\pi_\theta(\cdot\mid s)
\right)
\right]\le\delta.
$$

Old-policy single-path trajectories $(s_n,a_n)\sim(\pi_{\mathrm{old}},d_{\pi_{\mathrm{old}}})$를 모으면, $Q_{\pi_{\mathrm{old}}}$를 discounted future return으로 추정해 다음 Monte Carlo objective를 계산할 수 있다.

$$
\max_{\theta}\quad
\frac{1}{N}\sum_{n=1}^{N}
\frac{\pi_\theta(a_n\mid s_n)}{\pi_{\mathrm{old}}(a_n\mid s_n)}
\widehat Q_{\pi_{\mathrm{old}}}(s_n,a_n)
$$

where the sampled average-KL constraint is

$$
\frac{1}{N}\sum_{n=1}^{N}
D_{\mathrm{KL}}\left(
\pi_{\mathrm{old}}(\cdot\mid s_n)\,\|\,\pi_\theta(\cdot\mid s_n)
\right)\le\delta.
$$

즉, 각 trajectory에서 action은 old policy로 실제 수집하고, 그 action의 discounted future reward로 $\widehat Q_{\pi_{\mathrm{old}}}$를 만든다. Common TRPO implementations에서는 같은 역할의 baseline-reduced $\widehat A_{\pi_{\mathrm{old}}}$를 사용해 variance를 낮추기도 한다.

### 9. Practical TRPO Algorithm

앞 절의 sample-based objective와 average-KL constraint를 실제 policy update로 구현하면 다음과 같은 practical TRPO algorithm이 된다. 하나의 outer iteration은 policy를 $\pi_{\mathrm{old}}$에서 새로운 policy로 한 번 업데이트하는 과정이며, update가 끝나면 새 policy를 다음 iteration의 $\pi_{\mathrm{old}}$로 설정한다.

#### 한 Iteration의 세 단계

각 iteration에서는 다음 세 단계를 반복한다.

1. $\pi_{\mathrm{old}}$로 trajectories를 수집하고, 그 안의 state-action pairs $(s_n,a_n)$와 discounted future returns를 사용해 $\widehat Q_{\pi_{\mathrm{old}}}$ 또는 advantage의 Monte Carlo estimate를 구한다.
2. 수집한 trajectories에 objective와 average-KL constraint를 적용해 sample-based constrained optimization problem을 만든다.
3. trust-region natural policy gradient로 policy를 업데이트한 뒤, resulting policy를 새로운 $\pi_{\mathrm{old}}$로 설정하고 다음 iteration을 시작한다.

#### Natural Policy Gradient 근사

Trajectory states $s_1,\ldots,s_N$에 대한 sampled average KL을 다음과 같이 간단히 쓰자.

$$
\bar D_{\mathrm{KL}}(\theta_{\mathrm{old}}\|\theta)
=
\frac{1}{N}\sum_{n=1}^{N}
D_{\mathrm{KL}}
\left(
\pi_{\theta_{\mathrm{old}}}(\cdot\mid s_n)\,
\middle\|\,
\pi_{\theta}(\cdot\mid s_n)
\right).
$$

이제

$$
g=\left.\nabla_\theta L_{\theta_{\mathrm{old}}}(\theta)\right|_{\theta=\theta_{\mathrm{old}}},
\qquad
x=\theta-\theta_{\mathrm{old}}
$$

로 두면, policy update를 old parameter 주변의 local constrained problem으로 근사할 수 있다.

$$
\max_x\quad g^\mathsf{T}x
\qquad\text{subject to}\qquad
\frac{1}{2}x^\mathsf{T}Hx\le\delta.
$$

여기서 KL constraint의 curvature를 나타내는 Hessian은

$$
H=
\left.\nabla_\theta^2
\bar D_{\mathrm{KL}}(\theta_{\mathrm{old}}\|\theta)
\right|_{\theta=\theta_{\mathrm{old}}}
$$

이고, $N$개의 sampled states를 사용하면 empirical Hessian은

$$
H\approx
\frac{1}{N}\sum_{n=1}^{N}
\left.
\nabla_\theta^2
D_{\mathrm{KL}}
\left(
\pi_{\theta_{\mathrm{old}}}(\cdot\mid s_n)\,
\middle\|\,
\pi_\theta(\cdot\mid s_n)
\right)
\right|_{\theta=\theta_{\mathrm{old}}}.
$$

Standard regularity conditions 아래에서는 이 KL Hessian이 policy distribution의 Fisher information matrix에 해당한다. 따라서 이 update는 ordinary policy gradient의 parameter-space geometry 대신 policy-distribution geometry를 반영하는 Natural Policy Gradient가 된다.

#### Hessian을 사용하는 이유

Hessian은 한 함수가 전역적으로 다른 함수보다 항상 더 빠르게 휘어진다는 뜻이 아니라, 현재 parameter 주변의 local curvature를 나타낸다. 따라서 gradient가 알려 주는 현재의 증가 방향에 curvature 정보를 함께 반영하면, parameter space에서 같은 크기로 움직이는 것이 policy 변화량 측면에서도 적절한지 보정할 수 있다.

![Hessian이 local curvature와 gradient 방향을 보정하는 직관을 보여주는 그림](/assets/img/blog/deep-reinforcement-learning-summary-6/trpo-hessian-natural-gradient-intuition.png)

등고선이 원형이고 모든 방향의 curvature가 비슷하다면 vanilla gradient는 효율적인 수렴 방향과 비교적 잘 맞는다. 반면 등고선이 길게 늘어진 anisotropic한 경우에는 Euclidean steepest-gradient 방향이 좁은 방향을 가로질러 zigzag하거나, minimum으로 가는 효율적인 경로와 잘 맞지 않을 수 있다. KL Hessian, 즉 Fisher information matrix는 objective의 일반적인 curvature가 아니라 policy distribution의 local geometry를 정의한다. Policy distribution이 민감하게 변하는 방향의 step은 줄이고, 상대적으로 덜 민감한 방향은 더 크게 움직이도록 precondition하여 optimization의 conditioning과 convergence를 개선할 수 있다.

다만 TRPO에서 Hessian의 주된 역할은 generic objective-Hessian Newton optimization을 수행하는 것이 아니라, KL geometry에 맞는 trust-region constraint를 만족시키는 것이다. Hessian 또는 그 inverse를 직접 계산하는 것은 비싸기 때문에 일반적인 optimizer에서는 잘 사용하지 않는다. TRPO도 $H$나 $H^{-1}$을 직접 구성하지 않고 Hessian-vector product와 conjugate gradient를 사용해 필요한 $H^{-1}g$만 계산한다.

#### Taylor Expansion

Old parameter 주변에서 objective를 1차 Taylor expansion하면

$$
L_{\theta_{\mathrm{old}}}(\theta)
\approx
L_{\theta_{\mathrm{old}}}(\theta_{\mathrm{old}})+g^\mathsf{T}x.
$$

작은 local step을 전제로 higher-order objective terms를 생략한 근사이며, objective의 2차항이 항상 intrinsically 작다는 뜻은 아니다. 반면 average KL은

$$
\bar D_{\mathrm{KL}}(\theta_{\mathrm{old}}\|\theta)
\approx
\bar D_{\mathrm{KL}}(\theta_{\mathrm{old}}\|\theta_{\mathrm{old}})
+\left.\nabla_\theta\bar D_{\mathrm{KL}}(\theta_{\mathrm{old}}\|\theta)\right|_{\theta=\theta_{\mathrm{old}}}^{\mathsf{T}}x
+\frac{1}{2}x^\mathsf{T}Hx
=\frac{1}{2}x^\mathsf{T}Hx.
$$

이는 $\bar D_{\mathrm{KL}}(\theta_{\mathrm{old}}\|\theta_{\mathrm{old}})=0$이고 KL divergence가 항상 0 이상이며 $\theta=\theta_{\mathrm{old}}$에서 local minimum을 갖기 때문이다. 따라서 그 지점의 first derivative는 0이고, constraint의 leading term은 second-order quadratic form으로 남는다.

이 local problem의 방향은 단순한 gradient $g$가 아니라 natural gradient $H^{-1}g$이다. Natural-gradient direction에 scalar step size를 두어

$$
x=\beta H^{-1}g,
\qquad \beta\ge0
$$

로 놓고 trust-region constraint에 대입하면

$$
\frac{1}{2}
\left(\beta H^{-1}g\right)^{\mathsf{T}}
H
\left(\beta H^{-1}g\right)
=
\frac{\beta^2}{2}g^{\mathsf{T}}H^{-1}g
\le\delta.
$$

따라서 $g^{\mathsf{T}}H^{-1}g>0$인 경우 largest feasible step size는

$$
\beta^*
=
\sqrt{\frac{2\delta}{g^{\mathsf{T}}H^{-1}g}}
$$

이다. 양의 natural-gradient 방향에서는 linearized objective가 $g^{\mathsf{T}}x=\beta g^{\mathsf{T}}H^{-1}g$로 증가하므로, 이 $\beta^*$는 KL boundary를 넘지 않으면서 해당 방향의 linearized improvement를 가장 크게 만든다. 이를 $x=\beta H^{-1}g$에 대입하면 trust-region boundary까지 scaling한 해는

$$
x^*
=
\sqrt{\frac{2\delta}{g^\mathsf{T}H^{-1}g}}\,H^{-1}g.
$$

따라서 $H^{-1}g$는 KL geometry를 반영한 update direction이다. 이제 이 방향을 직접 inverse를 계산하지 않고 구하는 방법과, 근사 update를 실제 sample 기준으로 검증하는 방법을 살펴보자.

#### Conjugate Gradient

Natural-gradient direction은

$$
x=H^{-1}g
$$

이지만, 고차원 policy parameter에 대해 $H^{-1}$을 직접 만드는 것은 매우 비싸므로 실제로 inverse matrix를 구성하지 않는다. 대신 다음의 equivalent linear system을 푼다.

$$
Hx=g.
$$

이는 다음 quadratic minimization problem의 first-order condition과 같다.

$$
\min_x f(x)
=\frac{1}{2}x^\mathsf{T}Hx-g^\mathsf{T}x,
\qquad
\nabla f(x)=Hx-g.
$$

Conjugate gradient(CG)는 이 문제를 풀면서 $H$ 자체가 아니라 Hessian-vector product $Hv$만 사용한다. 따라서 필요한 것은 임의의 vector $v$에 대해 $Hv$를 계산하는 함수이며, $H^{-1}$을 명시적으로 저장할 필요가 없다.

여기서 KL/Fisher Hessian $H$는 대칭 positive semidefinite(PSD)이지, 항상 positive definite(PD)인 것은 아니다. 일부 parameter 방향의 curvature가 0이면 $H$가 singular할 수 있다. 실용적인 TRPO에서는 보통 damping을 적용해

$$
H_d=H+\lambda I,
\qquad \lambda>0
$$

로 만들며, 이는 system의 conditioning을 개선하고 CG가 사실상 positive definite인 행렬을 다루도록 한다. 이하에서는 이 damping이 반영된 행렬을 편의상 다시 $H$로 표기한다.

CG를 $n_{\mathrm{cg}}$번 수행하면

$$
x\approx H^{-1}g
$$

를 얻는다. 이때 trust-region boundary까지의 proposed full step은

$$
\Delta
=\sqrt{\frac{2\delta}{x^\mathsf{T}Hx}}\,x.
$$

CG가 정확히 $x=H^{-1}g$를 구했다면 $x^\mathsf{T}Hx=g^\mathsf{T}H^{-1}g$이므로, 앞서 Taylor Expansion에서 얻은 exact scaling과 동일하다. HVP와 CG는 큰 Hessian을 직접 다루는 비용을 줄이고 conditioning과 수렴을 개선할 수 있지만, 모든 문제에서 vanilla gradient보다 항상 빠른 수렴을 보장하지는 않는다. 또한 HVP와 CG를 안정적으로 구현하는 일 자체가 여전히 복잡하다.

#### Backtracking Line Search

위의 $\Delta$는 sampled objective, sampled advantage, sampled average KL, 그리고 근사 CG 해를 바탕으로 계산된다. 따라서 제안된 full step이 실제 sampled surrogate objective를 개선하지 못하거나 average-KL constraint를 위반할 수 있다.

후보 policy를

$$
\theta_{\mathrm{candidate}}^{(j)}
=\theta_{\mathrm{old}}+\alpha^j\Delta,
\qquad
0<\alpha<1,
\qquad
j=0,1,\ldots,j_{\max}
$$

로 만들고, sampled surrogate가 개선되면서 sampled average KL constraint를 만족하는 첫 후보를 선택한다.

$$
\widehat L(\theta_{\mathrm{candidate}}^{(j)})
>
\widehat L(\theta_{\mathrm{old}}),
\qquad
\bar D_{\mathrm{KL}}(\theta_{\mathrm{old}}\|\theta_{\mathrm{candidate}}^{(j)})
\le\delta.
$$

$\alpha$를 곱해 step을 줄이면 보통 KL도 줄어들지만, 근사와 비선형성 때문에 어떤 유한 횟수 안에 항상 조건을 만족한다고 보장할 수는 없다. $j_{\max}$번의 trial 안에 accepted candidate가 없으면 update를 거부하고 $\theta_{\mathrm{new}}=\theta_{\mathrm{old}}$로 둔다. Line search가 없으면 approximate full step이 KL bound를 넘거나 실제 성능을 낮출 수 있다.

#### TRPO Algorithm

아래 pseudocode에서 {::nomarkdown}\(\widehat L_k\){:/nomarkdown}는 trajectory set {::nomarkdown}\(\mathcal{D}_k\){:/nomarkdown}로 계산한 sampled surrogate이고, {::nomarkdown}\(\bar D_{\mathrm{KL},k}\){:/nomarkdown}는 같은 data에서 계산한 sampled average KL이다.

{% capture trpo_algorithm %}
$$
\begin{array}{l}
\textbf{Initialize }\theta_0 \\
\textbf{for }k=0,1,2,\ldots\textbf{ do} \\
\quad\quad\text{Collect on-policy trajectories }\mathcal{D}_k\text{ under }\pi_{\theta_k} \\
\quad\quad\text{Estimate advantages }\widehat A_k\text{ from }\mathcal{D}_k \\
\quad\quad\text{Form sampled policy gradient }\widehat g_k \\
\quad\quad\text{and KL HVP function }v\mapsto\widehat H_kv \\
\quad\quad\text{Run CG for }n_{\mathrm{cg}}\text{ iterations} \\
\quad\quad\text{to obtain }x_k\approx\widehat H_k^{-1}\widehat g_k \\
\quad\quad\text{Set }\Delta_k=\sqrt{\frac{2\delta}{x_k^\mathsf{T}\widehat H_kx_k}}\,x_k \\
\quad\quad\text{For }j=0,\ldots,j_{\max}\text{, test }\theta_{\mathrm{candidate}}^{(j)} \\
\quad\quad\quad\quad=\theta_k+\alpha^j\Delta_k,\quad 0<\alpha<1 \\
\quad\quad\text{Accept the first candidate with sampled objective improvement} \\
\quad\quad\quad\quad\widehat L_k(\theta_{\mathrm{candidate}}^{(j)})>\widehat L_k(\theta_k) \\
\quad\quad\quad\quad\text{and }\bar D_{\mathrm{KL},k}(\theta_k\|\theta_{\mathrm{candidate}}^{(j)})\le\delta \\
\quad\quad\text{If accepted, set }\theta_{k+1}=\theta_{\mathrm{candidate}}^{(j)} \\
\quad\quad\text{otherwise set }\theta_{k+1}=\theta_k \\
\textbf{end for}
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Algorithm 2. TRPO" label="algorithm:trpo" math=trpo_algorithm %}

즉, 각 iteration에서 old policy로 data를 모아 gradient와 KL Hessian-vector product를 추정하고, CG로 natural direction을 구한 뒤 trust-region 크기에 맞게 scaling한다. 마지막으로 backtracking line search가 sampled objective improvement와 KL constraint를 함께 확인하므로, 조건을 만족하는 경우에만 policy를 업데이트한다.

### 10. TRPO의 장단점

#### 장점

- Idealized theory에서는 policy update가 지나치게 크지 않을 때 monotonic-improvement bound를 제공한다. 실제 TRPO에서도 보통 안정적이고 꾸준한 improvement가 관찰되지만, 모든 update에서 성능 향상을 절대적으로 보장하는 것은 아니다.
- KL trust region이 policy distribution의 변화량을 제한하므로, raw parameter-space learning rate에 대한 민감도를 줄이고 지나치게 큰 policy update를 방지한다.
- Nonlinear stochastic policy를 지원하며, continuous control과 Atari의 CNN policy에서도 좋은 성능을 보였다.

#### 단점

- Natural-gradient와 second-order local approximation을 사용하므로 first-order policy gradient보다 이론과 구현이 복잡하다.
- $H^{-1}g$를 근사하기 위해
  $$
  \min_x\;\frac{1}{2}x^\mathsf{T}Hx-g^\mathsf{T}x
  $$
  를 풀어야 한다. 이를 위해 Hessian-vector product(HVP), conjugate gradient, damping, backtracking line search를 반복적으로 사용하므로 계산량과 구현 비용이 커진다.
- On-policy trajectory를 사용하므로 data reuse가 제한되고 sample efficiency가 낮을 수 있다.
- CNN이나 RNN을 기술적으로 지원하지만, 매우 큰 CNN이나 recurrent model에서는 반복적인 HVP/CG와 line-search evaluation 비용 때문에 실무에서 상대적으로 덜 사용되며 scalability와 구현 부담이 더 커진다.

## 08_Proximal Policy Optimization (PPO)

### TRPO에서 PPO로

Practical TRPO는 surrogate objective를 maximize하면서 old policy와 new policy 사이의 sampled average-KL constraint를 함께 만족시키는 방식이다. 이를 구현하려면 natural policy gradient에 가까운 second-order machinery가 필요하다. Policy gradient와 KL Hessian-vector product(HVP)를 계산하고, conjugate gradient(CG)로 natural-gradient direction을 근사한 뒤, backtracking line search로 objective improvement와 KL constraint를 다시 확인한다.

PPO는 OpenAI 저자들이 2017년에 제안한 on-policy first-order policy optimization family다. Policy update를 한 번에 너무 크게 만들지 않는다는 TRPO의 proximal idea는 유지하면서, 구현과 tuning을 단순하게 하고 계산 비용을 줄이는 것을 목표로 한다. 하나의 rollout batch에서 minibatch SGD 또는 Adam을 여러 epoch 수행하므로, Fisher inverse나 CG를 반복해서 계산해야 하는 TRPO보다 update를 쉽게 구성할 수 있다.

특히 PPO-Clip은 optimization problem에서 explicit KL constraint를 제거하고 policy ratio의 변화에 clipping을 적용한다. 이 clipping은 ratio가 과도하게 변할 때의 update incentive를 간접적으로 줄이지만, 원하는 KL 범위를 정확히 enforce하거나 KL trust region을 수학적으로 대체하는 것은 아니다. 따라서 실제 KL이 커질 수 있으며, 구현에 따라 empirical KL을 monitor하고 일정 수준을 넘으면 early stopping을 적용하기도 한다.

PPO는 2017년 공개될 당시 OpenAI에서 default RL algorithm으로 자리 잡았고, 현재도 널리 사용되는 baseline이다. 다만 모든 RL 문제에서 universal default라는 뜻은 아니다.

### Clipped Surrogate Objective

Old policy $\pi_{\theta_{\mathrm{old}}}$로 수집한 sample $(s_t,a_t)$에 대해 policy ratio를 다음과 같이 정의한다.

$$
r_t(\theta)
=
\frac{\pi_\theta(a_t\mid s_t)}
{\pi_{\theta_{\mathrm{old}}}(a_t\mid s_t)}.
$$

$\theta=\theta_{\mathrm{old}}$이면 numerator와 denominator가 같으므로, old-policy sample에서 $r_t(\theta)=1$이다. PPO-Clip의 clipped surrogate objective는

$$
L^{\mathrm{CLIP}}(\theta)
=
\mathbb{E}_t\left[
\min\left(
r_t(\theta)\widehat A_t,
\operatorname{clip}\left(r_t(\theta),1-\epsilon,1+\epsilon\right)\widehat A_t
\right)
\right]
$$

로 쓴다. 여기서 $\operatorname{clip}$은 probability ratio가 $[1-\epsilon,1+\epsilon]$ 밖으로 이동할 때 그 항이 주는 incentive를 제한한다. 이는 실제 ratio나 policy distribution의 변화를 항상 해당 구간 안에 묶는 hard bound는 아니다.

각 sample에서 $\min$은 unclipped term과 clipped term 중 더 pessimistic한 값을 선택한다. 따라서

$$
L^{\mathrm{CLIP}}(\theta)
\le
\mathbb{E}_t\left[r_t(\theta)\widehat A_t\right]
$$

이며, 이 의미에서 clipped surrogate는 unclipped surrogate의 lower bound 역할을 한다. 그러나 이것이 true performance $\eta$의 formal lower bound이거나, TRPO constrained optimum의 lower bound라는 뜻은 아니다. 또한 이 식만으로 PPO가 formal MM algorithm이 되거나 모든 iteration에서 monotonic improvement를 보장하는 것도 아니다.

계산 측면에서 PPO-Clip은 Fisher inverse, HVP, CG를 사용하지 않고 ordinary first-order gradient method로 optimize한다. 따라서 PPO의 핵심은 KL constraint를 정확히 만족시키는 것이 아니라, ratio clipping으로 지나치게 큰 policy update의 incentive를 줄이면서 rollout data를 minibatch와 여러 epoch에 재사용하는 데 있다.

[PPO 원 논문](https://arxiv.org/abs/1707.06347), [OpenAI PPO 소개](https://openai.com/index/openai-baselines-ppo/)

### Advantage 부호에 따른 Clipping

Clipping의 samplewise 동작은 advantage 추정치의 부호에 따라 달라진다. $\widehat A_t\ge 0$이면 해당 action이 유리하므로, objective에서

$$
\min\left(r_t(\theta)\widehat A_t,
\operatorname{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\widehat A_t\right)
=
\min\left(r_t(\theta),1+\epsilon\right)\widehat A_t
$$

로 단순화된다. 따라서 좋은 action의 probability를 높이는 update는 ratio가 $1+\epsilon$에 도달할 때까지만 objective를 개선하고, 그보다 커진 뒤에는 추가적인 incentive가 없다. 다만 실제 ratio를 $1+\epsilon$에서 hard-clamp하는 것은 아니며, 다른 loss 항이나 다음 update에 의해 ratio가 더 커질 수 있다.

$\widehat A_t<0$이면 해당 action이 불리하므로,

$$
\min\left(r_t(\theta)\widehat A_t,
\operatorname{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\widehat A_t\right)
=
\max\left(r_t(\theta),1-\epsilon\right)\widehat A_t
$$

가 된다. 음수인 $\widehat A_t$를 곱하면 값의 대소관계가 뒤집히므로, 바깥의 $\min$이 $\max$ 형태로 보인다. 나쁜 action의 probability를 낮추는 update는 ratio가 $1-\epsilon$까지 내려갈 때까지만 objective를 개선하고, 그보다 낮아진 뒤에는 추가적인 incentive가 없다. Original PPO paper의 실험에서는 흔히 $\epsilon=0.2$를 사용했지만, $\epsilon$은 문제와 구현에 따라 조정하는 hyperparameter다. 즉 clipping은 pessimistic plateau를 만들어 update incentive를 줄이는 장치이며, probability나 KL divergence에 대한 strict constraint는 아니다.

### PPO의 Practical Objective

실제 구현에서는 policy objective에 value-function error와 entropy bonus를 함께 넣어 다음과 같은 maximize convention을 사용한다.

$$
L^{\mathrm{CLIP+VF+S}}(\theta)
=
\mathbb{E}_t\left[
L_t^{\mathrm{CLIP}}(\theta)
-c_1L_t^{\mathrm{VF}}(\theta)
+c_2 S[\pi_\theta](s_t)
\right].
$$

Value error는

$$
L_t^{\mathrm{VF}}(\theta)
=
\left(V_\theta(s_t)-V_t^{\mathrm{target}}\right)^2
$$

로 둔다. Policy와 value network가 shared backbone을 사용하면 이 combined objective가 공유 parameter와 각 head를 함께 학습시킨다. Actor와 critic을 separate network로 두면 value network의 parameter를 $\phi$로 표기해 $V_\phi(s_t)$와 $L_t^{\mathrm{VF}}(\phi)$를 policy loss와 별도로 optimize할 수 있다.

이때 이론적으로 $A(s,a)=Q(s,a)-V(s)$이지만, PPO가 별도의 $Q$ network를 반드시 요구하는 것은 아니다. Sampled reward로 계산한 reward-to-go, bootstrapped return, 또는 GAE로 $Q$ 또는 return과 advantage를 추정하고, value network인 critic을 함께 학습하는 방식이 일반적이다.

{::nomarkdown}\(S[\pi_\theta](s_t)\){:/nomarkdown}는 policy distribution의 entropy bonus로, stochasticity와 exploration을 장려하고 policy가 너무 일찍 deterministic policy로 collapse하는 것을 막는다. 이는 action에 외부 noise를 더하는 항이 아니다. Maximize convention에서 {::nomarkdown}\(-c_1L^{\mathrm{VF}}\){:/nomarkdown}는 value error를 minimize하게 만들고, {::nomarkdown}\(+c_2S\){:/nomarkdown}는 entropy를 maximize하게 만든다. {::nomarkdown}\(c_1\){:/nomarkdown}과 {::nomarkdown}\(c_2\){:/nomarkdown}는 두 항의 가중치다.

## 09_DRL Algorithm 비교

| Algorithm | Model | State space | Action space | Data policy | 주요 학습 신호 |
|---|---|---|---|---|---|
| SARSA | model-free RL | discrete in tabular form, function approximation can extend | discrete in standard form | on-policy | TD action-value $Q$ |
| Q-Learning | model-free RL | discrete in tabular form, function approximation can extend | discrete in standard form | off-policy | TD optimal $Q$ or value target |
| DQN | model-free DRL | high-dimensional or continuous-valued observation/state input | discrete | off-policy replay | Q-value |
| A3C | model-free DRL | high-dimensional or continuous-valued state | discrete or continuous | on-policy | n-step return and advantage actor-critic |
| DDPG | model-free DRL | high-dimensional or continuous-valued state | continuous | off-policy replay | Q critic and deterministic actor gradient |
| TRPO | model-free DRL | high-dimensional or continuous-valued state | discrete or continuous | on-policy | advantage surrogate with KL trust region |
| PPO | model-free DRL | high-dimensional or continuous-valued state | discrete or continuous | on-policy rollout with minibatch reuse | clipped advantage surrogate |
{: .policy-comparison-table}

표의 state space와 action space 표기는 대표적인 사용 설정이며, 수학적으로 가능한 범위를 엄격히 배제하는 분류는 아니다. 특히 function approximation을 사용하면 state 처리 범위가 확장될 수 있다. A3C, TRPO, PPO는 기본적으로 on-policy 알고리즘이다. Importance sampling으로 제한적인 distribution mismatch를 보정할 수 있지만, ratio나 replay를 추가하는 것만으로 robust한 off-policy 알고리즘이 되는 것은 아니다. PPO의 ratio는 현재 rollout batch에서 여러 번 update할 때 old policy와 new policy의 mismatch를 보정하며, PPO 자체는 여전히 on-policy로 분류된다. Truly off-policy actor-critic은 보통 별도의 correction과 stability mechanism을 필요로 한다.

## 참고 강의

- [고려대 오승상 강화학습 26 — DDPG](https://www.youtube.com/watch?v=Ukloo2xtayQ)
- [고려대 오승상 강화학습 27 — TRPO 1](https://www.youtube.com/watch?v=c15b9AjHxBA)
- [고려대 오승상 강화학습 28 — TRPO 2](https://www.youtube.com/watch?v=ojgn1xBWfGo)
- [고려대 오승상 강화학습 29 — TRPO 3](https://www.youtube.com/watch?v=Q3_mJFKiEwc)
- [고려대 오승상 강화학습 30 — PPO](https://www.youtube.com/watch?v=5fHbx33bqBc)
