---
layout: post
title: Reinforcement Learning 4 - Deep Q-Network
date: 2026-08-27 00:00:00 +0900
slug: deep-reinforcement-learning-summary-4
render_with_liquid: true
use_math: true
categories:
- 공부
- 강화학습
tags:
- reinforcement-learning
---

## 00_Deep Reinforcement Learning 개요

강화학습은 Bellman의 Dynamic Programming과 optimal control에서 출발해 Q-learning, neural network 기반 function approximation, policy gradient와 actor-critic 방법으로 발전해 왔다.

강화학습과 딥러닝은 처음에는 서로 다른 줄기로 발전했다. 이후 DeepMind가 Q-learning의 Q-table을 CNN 기반 neural network로 대체한 **DQN**을 제안하면서 두 분야가 결합되었다. DQN은 이미지처럼 큰 state space에서도 Q-learning을 적용할 수 있음을 보여주었고, 이후의 Deep Reinforcement Learning 연구는 tabular RL의 table 크기 문제, Q-learning의 discrete action 제약, 학습 불안정성, sample 효율 문제 등을 개선하는 방향으로 발전했다.

![Reinforcement Learning과 Deep Reinforcement Learning의 주요 milestones](/assets/img/blog/deep-reinforcement-learning-summary-4/rl-drl-milestones.png)

그림의 흐름을 간단히 정리하면 다음과 같다.

- **Dynamic Programming**: Bellman equation을 이용해 MDP와 optimal control을 수학적으로 다룬다.
- **Q-learning**: Q-table을 이용하는 현대적인 tabular RL의 대표적인 방법이다.
- **DQN**: Q-learning과 CNN을 결합하여 Atari 게임처럼 큰 state space를 다룬다.
- **DDPG**: Q-learning과 deterministic policy gradient를 결합하여 continuous action에 대응한다.
- **A3C와 AlphaGo**: actor-critic, MCTS, policy gradient 등의 방법이 대규모 문제에 적용된다.
- **PPO와 MPO**: policy optimization을 안정적으로 수행하기 위한 대표적인 modern DRL 방법이다.


### Tabular RL과 Deep RL

#### Tabular Reinforcement Learning

기본적인 Reinforcement Learning에서는 각 state-action pair의 value를 Q-table에 저장하고, Q값을 update하면서 optimal policy를 찾는다.

$$
Q:\mathcal{S}\times\mathcal{A}\rightarrow\mathbb{R}
$$

이 방식은 state와 action이 유한하고 개수가 많지 않은 tabular 환경에서 직관적이고 효과적이다. 하지만 table의 크기가 $|\mathcal{S}|\,|\mathcal{A}|$에 비례하므로 다음과 같은 한계가 있다.

- state 또는 action의 개수가 매우 커지면 table을 저장하고 탐색하기 어렵다.
- state나 action space가 연속적이면 모든 값을 table에 미리 만들 수 없다.
- 비슷한 state 사이의 관계를 공유하지 못하므로, 각 state-action pair를 별도로 학습해야 한다.

#### Deep Reinforcement Learning

Deep Reinforcement Learning(DRL)은 Q function, value function 또는 policy를 neural network로 근사하는 방법이다.

$$
Q(s,a)\approx Q_\theta(s,a),
\qquad
\pi(a\mid s)\approx\pi_\theta(a\mid s)
$$

여기서 $\theta$는 neural network의 parameter이다. 모든 state-action pair를 table에 저장하는 대신, network가 입력 state를 보고 value나 policy를 출력하도록 학습한다.

DRL은 state 또는 action space가 매우 크거나 연속적인 문제에도 적용할 수 있다. 예를 들어 이미지, 위치, 속도, 관절각처럼 높은 차원의 state를 neural network 입력으로 사용할 수 있고, 연속적인 action을 출력하는 policy도 학습할 수 있다. 다만 function approximation을 사용하면 학습이 불안정해질 수 있고, 충분한 sample과 적절한 network 구조가 필요하다.

| 구분 | Tabular RL | Deep RL |
| --- | --- | --- |
| Value/policy 표현 | Q-table 또는 value table | Neural network |
| State/action space | 작고 유한한 경우에 적합 | 크거나 연속적인 경우에도 적용 가능 |
| 일반화 | state-action pair 사이의 일반화가 거의 없음 | 유사한 입력 사이의 일반화 가능 |
| 주요 한계 | table 크기와 차원의 저주 | 학습 불안정성, sample 효율, hyperparameter 의존성 |
{: .policy-comparison-table}

## 01_Deep Q-Network

DQN은 Q-learning과 Convolutional Neural Network(CNN)를 결합한 모델이다. Q-table을 직접 저장하는 대신 CNN 기반 neural network가 state를 입력받아 각 action의 Q-value를 출력한다.

$$
Q(s,a;\theta) \approx Q_*(s,a)
$$

여기서 $\theta$는 neural network parameter이다. 네트워크는 입력 state에서 유용한 feature를 추출하고, 출력층에서는 가능한 action마다 하나의 Q-value를 계산한다.

![DQN의 CNN 기반 Q-value 근사 구조](/assets/img/blog/deep-reinforcement-learning-summary-4/dqn-cnn-architecture.png)

그림의 Atari 예시에서는 연속된 frame 4장을 쌓은 $84\times84\times4$ 입력을 CNN에 넣는다. CNN을 거치면서 이미지의 공간 정보를 작은 feature representation으로 줄이고, fully connected layer를 거쳐 action 개수만큼의 Q-value를 출력한다.

$$
\text{stacked frames}
\rightarrow \text{CNN feature extraction}
\rightarrow \text{fully connected layers}
\rightarrow \left[Q(s,a^1),\ldots,Q(s,a^m)\right]
$$

행동을 선택할 때는 출력된 Q-value 중 가장 큰 값을 갖는 action을 선택한다.

$$
a_t = \arg\max_a Q(s_t,a;\theta)
$$

따라서 DQN은 이미지처럼 크거나 연속적인 state space에서도 Q-learning을 적용할 수 있게 해준다. 반면 기본 DQN의 출력층은 가능한 action마다 하나의 Q-value를 출력하므로 action space는 discrete해야 한다. 즉, DQN은 state space의 크기나 연속성에는 비교적 유연하지만, continuous action space를 직접 처리하지는 못한다. Continuous action space에서는 DDPG, TD3, SAC와 같은 다른 접근이 필요하다.

### Naive DQN

Naive DQN은 Q-learning의 Q-table을 neural network로 단순히 대체한 초기 형태의 DQN이다. 이때 target policy와 behavior policy는 Q-learning의 방식에 따라 다를 수 있지만, 현재 Q network 하나를 사용해 Q값과 target을 함께 계산한다.

#### Q-learning update와 loss

Naive DQN의 Q-learning update는 다음과 같이 표현할 수 있다.

$$
Q(S_t,A_t)\leftarrow Q(S_t,A_t)
+\alpha\left[R_{t+1}+\gamma\max_aQ(S_{t+1},a)-Q(S_t,A_t)\right]
$$

Target은 다음과 같다.

$$
y_t=R_{t+1}+\gamma\max_aQ(S_{t+1},a)
$$

Q network의 출력과 target의 차이를 줄이기 위해 Mean Squared Error(MSE) loss를 사용한다.

$$
L(\theta)=\left[y_t-Q(S_t,A_t;\theta)\right]^2
$$

여기서 $\theta$는 network parameter이고, SGD를 통해 $L(\theta)$가 작아지도록 network를 update한다. Naive DQN에서는 3개의 convolutional layer와 2개의 fully connected layer를 사용해 Q-value를 추정했지만, 간단한 1개의 fully connected layer를 사용하는 linear model과 성능 차이가 크지 않은 문제가 있었다.

#### Naive DQN의 문제

1. **Temporal correlation between samples**: environment에서 연속적으로 얻는 sample은 서로 독립적이지 않다.
2. **Non-stationary target**: Q network가 update될 때 target을 계산하는 Q값도 함께 변하므로 target이 계속 움직인다.

##### Temporal correlation

Agent가 연속된 time step에서 얻는 transition은 서로 강한 상관관계를 가진다. 예를 들어 agent가 넘어지기 시작한 상황에서는 비슷한 state와 action이 연속해서 관측될 수 있다.

![연속된 transition에서 발생하는 temporal correlation](/assets/img/blog/deep-reinforcement-learning-summary-4/temporal-correlation.png)

이러한 data를 순서대로 바로 학습하면 neural network가 다양한 상황을 고르게 학습하지 못하고, i.i.d. sample을 가정하는 일반적인 SGD의 장점도 약해진다.

##### Non-stationary target

현재 Q network로 prediction과 target을 모두 계산하면 network parameter가 바뀔 때 target도 함께 바뀐다. 즉, network가 따라가야 하는 정답이 update 과정에서 계속 움직이므로 학습이 불안정해질 수 있다.

이 두 문제를 완화하기 위해 DQN에서는 reward clipping과 Experience Replay 같은 기법을 사용한다. Target network는 non-stationary target 문제를 완화하기 위한 또 다른 핵심 기법이며, 이후에 별도로 다룬다.

#### Target network

Naive DQN에서는 현재 Q-network 하나를 사용해 prediction과 target을 모두 계산한다.

$$
y_t=R_{t+1}+\gamma\max_a Q(S_{t+1},a;\theta)
$$

이때 behavior 또는 online Q-network의 parameter $\theta$를 update하면 target을 만드는 Q값도 같이 바뀐다. Network가 쫓아가야 하는 target이 계속 변하므로 non-stationary target problem이 발생한다.

이를 완화하기 위해 DQN은 Q-network를 두 개로 나눈다.

- **Online Q-network**: parameter $\theta$를 사용하며, 매 update마다 학습된다. action을 선택할 때도 사용한다.
- **Target Q-network**: parameter $\hat{\theta}$를 사용하며, 일정 기간 동안 고정된다. Q-learning target을 계산할 때 사용한다.

Replay buffer에서 크기 $B$인 minibatch를 뽑았을 때 target network를 사용하는 loss는 다음과 같다.

$$
L(\theta)
= \frac{1}{2B}\sum_{i\in B}
\left[
r_{i+1}+\gamma\max_a\hat{Q}(s_{i+1},a;\hat{\theta})
-Q(s_i,a_i;\theta)
\right]^2
$$

여기서 $\hat{Q}$는 target Q-network의 출력이다. 한 번의 gradient update 동안에는 $\hat{\theta}$를 고정된 상수처럼 취급하고, online Q-network의 parameter $\theta$만 update한다.

Target을

$$
y_i=r_{i+1}+\gamma\max_a\hat{Q}(s_{i+1},a;\hat{\theta})
$$

라고 쓰면 gradient descent 방향은 다음과 같이 표현할 수 있다.

$$
-\nabla_\theta L(\theta)
= \frac{1}{B}\sum_{i\in B}
\left[y_i-Q(s_i,a_i;\theta)\right]
\nabla_\theta Q(s_i,a_i;\theta)
$$

Target network의 parameter $\hat{\theta}$는 매 step update하지 않고, 일정한 주기 $K$마다 online network의 parameter를 복사한다.

$$
\hat{\theta}\leftarrow\theta
\qquad\text{every }K\text{ update steps}
$$

따라서 $K$번의 update 동안 target network는 고정되어 있고, 그동안 online Q-network만 target에 가까워지도록 학습한다. 일정 시간이 지나 target network를 다시 복사하면 새로운 target이 만들어진다. 이처럼 target을 일정 기간 고정하면 target이 online network의 모든 변화에 즉시 따라 움직이는 문제를 줄여 학습을 안정화할 수 있다.

### DQN의 개선

#### Reward clipping

Atari 게임처럼 게임마다 score의 크기와 단위가 다르면 reward scale도 서로 달라진다. 이를 통일하고 큰 reward가 gradient를 과도하게 키우는 문제를 줄이기 위해 reward의 부호만 사용하는 clipping을 적용할 수 있다.

$$
\tilde R_t=
\begin{cases}
1, & R_t>0 \\
0, & R_t=0 \\
-1, & R_t<0
\end{cases}
$$

Reward clipping은 서로 다른 게임에 동일한 학습 설정을 적용하기 쉽게 해주지만, 원래 reward의 크기 정보가 사라진다는 trade-off가 있다.

#### Experience Replay

Experience Replay는 agent가 경험한 transition을 replay buffer에 저장한 뒤, 저장된 경험에서 random minibatch를 뽑아 학습하는 방법이다.

![DQN의 replay buffer workflow](/assets/img/blog/deep-reinforcement-learning-summary-4/replay-buffer-workflow.png)

Replay buffer를 적용하는 과정은 다음과 같다.

1. 현재 state $s_t$에서 Q-network를 이용해 action을 선택한다. 보통 $\epsilon$-greedy policy를 사용하며, greedy action은 다음과 같이 정한다.

$$
a_t^* = \arg\max_a Q(s_t,a;\theta)
$$

2. 선택한 action을 environment에 적용하여 reward $r_{t+1}$과 next state $s_{t+1}$을 얻는다.
3. transition $(s_t,a_t,r_{t+1},s_{t+1})$을 Q-network에 바로 학습시키지 않고 replay buffer에 저장한다. Buffer가 가득 차면 오래된 transition부터 삭제한다.
4. Replay buffer에서 random minibatch를 sampling하고, 그 batch를 이용해 Q-network parameter $\theta$를 update한다.

즉, agent는 새 transition을 계속 수집하고, 학습은 현재 방금 얻은 transition 하나가 아니라 replay buffer에서 무작위로 뽑은 과거 transition들의 minibatch를 사용해 수행한다.

하나의 transition은 다음 네 가지로 저장한다.

$$
(S_t,A_t,R_{t+1},S_{t+1})
$$

Replay buffer를 $\mathcal{D}$라고 하면,

$$
\mathcal{D}=\left\{(S_i,A_i,R_{i+1},S_{i+1})\right\}_{i=1}^{N}
$$

와 같이 경험을 저장하고, 그중 일부를 random sampling하여 minibatch를 구성한다.

![시간에 따라 변하는 replay buffer와 드문 사건의 재사용](/assets/img/blog/deep-reinforcement-learning-summary-4/replay-buffer-rare-events.png)

Replay buffer를 사용하면 다음과 같은 효과가 있다.

1. **Temporal correlation 완화**: 연속된 time step의 sample을 그대로 사용하지 않고 buffer에서 random하게 섞어 뽑으므로 sample 사이의 상관관계를 줄인다.
2. **Learning 효율 증가**: minibatch를 사용해 여러 transition을 한 번의 update에서 처리하고, vectorized computation을 활용할 수 있다.
3. **Sample 재사용**: 한 번 얻은 transition을 여러 번 학습에 사용할 수 있어 data efficiency가 높아진다. 특히 드물게 발생하는 중요한 event도 buffer에 남아 있는 동안 반복해서 사용할 수 있다.

Experience Replay가 temporal correlation을 줄여주기는 하지만, buffer가 가득 차면 오래된 transition은 삭제된다. 따라서 드문 event가 영원히 보존되는 것은 아니며, 이후에는 중요한 경험을 더 자주 뽑는 Prioritized Experience Replay와 같은 방법도 사용된다.

### DQN 전체 구조

DQN은 online Q-network와 target Q-network, replay buffer를 함께 사용하여 다음과 같은 순서로 학습한다.

![DQN의 전체 구조](/assets/img/blog/deep-reinforcement-learning-summary-4/dqn-overall-structure.png)

1. Online Q-network $Q(s_t,a;\theta)$를 이용해 $\epsilon$-greedy 방식으로 action $a_t$를 선택한다.
2. Environment에 action을 적용하고 reward $r_{t+1}$과 next state $s_{t+1}$을 관측한다.
3. transition $(s_t,a_t,r_{t+1},s_{t+1})$을 replay buffer에 저장한다.
4. Replay buffer에서 random minibatch를 sampling한다.
5. Target Q-network $\hat{Q}(s_{t+1},a;\hat{\theta})$를 이용해 target value를 계산하고, online Q-network의 parameter $\theta$를 update한다.
6. 일정한 update 주기마다 target network의 parameter를 online network에서 복사한다.

{% capture dqn_algorithm %}
$$
\begin{array}{l}
\textbf{Initialize online Q-network }Q\text{ with random weights }\theta \\
\textbf{Initialize target Q-network }\hat{Q}\text{ with weights }\hat{\theta}=\theta \\
\textbf{Initialize replay buffer }\mathcal{D}\text{ with capacity }N \\
\textbf{For each episode:} \\
\quad\quad \text{Initialize state }s_t \\
\quad\quad \textbf{For each time step }t\textbf{:} \\
\quad\quad\quad\quad \text{With probability }\epsilon\text{ choose a random action }a_t \\
\quad\quad\quad\quad \text{Otherwise choose }a_t\leftarrow\operatorname*{arg\,max}_a Q(s_t,a;\theta) \\
\quad\quad\quad\quad \text{Execute }a_t\text{ and observe }r_{t+1},s_{t+1} \\
\quad\quad\quad\quad \mathcal{D}\leftarrow\mathcal{D}\cup\{(s_t,a_t,r_{t+1},s_{t+1})\} \\
\quad\quad\quad\quad \text{Sample minibatch }B\text{ from }\mathcal{D} \\
\quad\quad\quad\quad y_i\leftarrow r_{i+1}+\gamma\max_a\hat{Q}(s_{i+1},a;\hat{\theta})\text{ for }i\in B \\
\quad\quad\quad\quad \text{Update }\theta\text{ by gradient descent on }\frac{1}{2|B|}\sum_{i\in B}[y_i-Q(s_i,a_i;\theta)]^2 \\
\quad\quad\quad\quad \text{Every }C\text{ updates set }\hat{\theta}\leftarrow\theta
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Algorithm 1. Deep Q-Network" label="algorithm:dqn" math=dqn_algorithm %}

#### Replay period $K$

Replay period $K$는 새로운 transition을 replay buffer에 저장한 뒤, 몇 step마다 minibatch를 sampling하여 Q-network를 update할지를 정하는 주기이다.

$$
t\bmod K=0
\quad\Longrightarrow\quad
\text{sample a minibatch and update }Q\text{-network}
$$

알고리즘에서는 매 time step마다 새 transition을 먼저 buffer에 넣고, $K$번째 step마다 replay update를 수행한다. 따라서 $K=1$이면 새 transition을 매 step 바로 학습에 사용할 수 있고, $K$가 커지면 여러 transition을 먼저 수집한 뒤 한 번 update한다.

- **작은 $K$**: 새 transition이 빠르게 학습에 반영되지만 Q-network update 횟수와 계산량이 증가한다.
- **큰 $K$**: transition 수집과 network update를 분리해 계산량을 줄일 수 있지만, 새 경험이 학습에 반영되는 시점이 늦어진다.

여기서 $K$는 replay buffer의 최대 저장 개수 $N$, 한 번에 뽑는 minibatch 크기 $B$, target network를 복사하는 주기 $C$와 서로 다른 hyperparameter이다.

#### DQN의 성능과 CNN 구조

##### Replay와 Target Network의 효과

다음 표는 Replay Buffer와 Target Network를 각각 사용했을 때의 성능을 비교한 것이다. 두 기법을 함께 사용한 DQN이 Naive DQN이나 Linear NN보다 여러 Atari 게임에서 높은 점수를 얻는다.

![DQN, Naive DQN, Linear NN의 Atari 성능 비교](/assets/img/blog/deep-reinforcement-learning-summary-4/dqn-performance-comparison.png)

이 결과는 CNN을 사용해 state를 표현하는 것만으로 충분하지 않고, 안정적인 학습을 위해 Replay Buffer와 Target Network가 함께 필요하다는 점을 보여준다. Replay Buffer는 sample 간 temporal correlation을 줄이고, Target Network는 moving target 문제를 완화한다.

##### Max pooling을 사용하지 않는 이유

일반적인 CNN에서는 feature map의 크기를 줄이고 작은 위치 변화에 강건하게 만들기 위해 max pooling을 사용하기도 한다. Max pooling은 translation invariance를 높이는 장점이 있지만, Atari와 같이 frame별 위치와 이동 방향이 중요한 게임에서는 세밀한 spatial information을 잃게 만들 수 있다.

예를 들어 공이나 적이 한 칸 이동한 차이가 action 선택에 중요할 수 있는데, max pooling을 적용하면 두 위치가 비슷한 feature로 합쳐질 수 있다. 따라서 DQN에서는 max pooling 대신 convolution의 stride를 이용해 feature map의 크기를 줄이면서 위치 정보를 최대한 보존한다.

## 02_DQN Variants

### Prioritized Experience Replay

일반적인 Experience Replay는 replay buffer에서 transition을 uniform random sampling한다. 하지만 모든 transition이 학습에 똑같이 중요한 것은 아니다. 예측값과 실제 target의 차이가 큰 transition은 현재 Q-network가 많이 틀리고 있다는 뜻이므로, 이를 더 자주 학습하도록 priority를 부여할 수 있다.

Transition $i$의 TD error를 이용해 priority를 다음과 같이 정의한다.

$$
p_i
= \left|
r_{i+1}+\gamma\max_a\hat{Q}(s_{i+1},a;\hat{\theta})
-Q(s_i,a_i;\theta)
\right|+\epsilon
$$

여기서 $\epsilon>0$은 priority가 0이 되어 해당 transition이 영원히 선택되지 않는 것을 방지하는 작은 값이다. Priority를 sampling probability로 바꾸면 다음과 같다.

$$
P(i)=\frac{p_i^{\alpha_{\mathrm{PER}}}}
{\sum_k p_k^{\alpha_{\mathrm{PER}}}}
$$

$\alpha_{\mathrm{PER}}$는 priority를 sampling에 얼마나 반영할지 결정한다. $\alpha_{\mathrm{PER}}=0$이면 uniform sampling이고, $\alpha_{\mathrm{PER}}=1$이면 priority를 그대로 반영한다. 값이 커질수록 TD error가 큰 transition이 더 자주 선택된다. 이 값은 Q-network의 learning rate로 사용하는 $\alpha$와 다른 parameter이다.

모든 transition의 TD error를 매번 다시 계산하면 연산량이 커지므로, 실제로는 minibatch에 sampling된 transition의 TD error와 priority를 주로 update한다. Sampling되지 않은 transition의 priority는 다음에 선택될 때까지 이전 값으로 유지될 수 있다.

PER를 사용하면 TD error가 큰 transition, 즉 현재 network가 많이 틀리는 transition을 집중적으로 학습할 수 있다. 그러나 다음과 같은 문제가 생긴다.

1. **Loss of diversity**: priority가 큰 transition만 반복해서 선택되면 priority가 낮은 transition을 충분히 학습하지 못할 수 있다.
2. **Sampling bias**: uniform distribution이 아닌 $P(i)$로 sample을 뽑으므로, sample average나 gradient가 원래 data distribution을 편향되게 반영할 수 있다.

Sampling bias를 줄이기 위해 importance sampling weight를 사용할 수 있다.

$$
w_i=\left(\frac{1}{N}\frac{1}{P(i)}\right)^\beta
=\left(NP(i)\right)^{-\beta}
$$

여기서 $N$은 replay buffer의 transition 개수이고, $\beta$는 bias correction의 정도를 결정한다. $\beta=0$이면 weight가 모두 1이어서 priority sampling에 대한 보정을 하지 않고, $\beta=1$이면 priority sampling으로 생긴 bias를 이론적으로 완전히 보정하는 방향이다. 즉, $\beta$는 sampling probability 자체를 uniform하게 바꾸는 값이 아니라 sampling 이후 update에 적용하는 보정 강도이다.

TD error를 $\delta_i=y_i-Q(s_i,a_i;\theta)$라고 하면 importance sampling weight를 적용한 Q-learning update는 다음과 같이 표현할 수 있다.

$$
Q(s_i,a_i)\leftarrow Q(s_i,a_i)+\alpha\,w_i\,\delta_i
$$

실제 구현에서는 minibatch 안에서 가장 큰 weight로 나누어 update 크기를 안정화하기도 한다.

$$
\widetilde{w}_i=\frac{w_i}{\max_{j\in B}w_j}
$$

학습 초반에는 priority가 큰 transition을 집중적으로 학습하는 것이 유리할 수 있지만, 수렴에 가까워질수록 unbiased update가 중요해진다. 따라서 보통 $\beta$를 작은 값에서 시작해 학습이 진행될수록 1에 가깝게 증가시킨다.

### Multi-step Learning

기존 Q-learning은 한 step 뒤의 reward와 next state의 Q-value만 사용하는 one-step TD target을 사용한다. 하지만 어떤 문제에서는 현재 state에서 몇 step 동안 발생한 reward를 함께 고려하는 것이 더 유리할 수 있다. 이때 사용하는 방법이 multi-step learning이다.

#### Multi-step target

1-step부터 episode가 끝날 때까지의 target은 다음과 같이 연결된다.

$$
G_t^{(1)} = R_{t+1}+\gamma V(S_{t+1})
$$

$$
G_t^{(n)}
= R_{t+1}+\gamma R_{t+2}+\cdots+\gamma^{n-1}R_{t+n}
  +\gamma^n V(S_{t+n})
$$

$$
G_t^{(\infty)}
= R_{t+1}+\gamma R_{t+2}+\cdots+\gamma^{T-1}R_T
$$

여기서 $G_t^{(1)}$은 one-step TD target이고, $G_t^{(n)}$은 $n$개의 실제 reward를 사용한 뒤 $V(S_{t+n})$로 bootstrapping하는 truncated $n$-step return이다. $G_t^{(\infty)}$는 episode가 끝날 때까지의 실제 return이므로 Monte Carlo target에 해당한다.

| Target | 사용하는 정보 | 특징 |
| --- | --- | --- |
| $G_t^{(1)}$ | $R_{t+1}$과 $V(S_{t+1})$ | one-step TD, 강한 bootstrapping |
| $G_t^{(n)}$ | $R_{t+1},\ldots,R_{t+n}$과 $V(S_{t+n})$ | multi-step TD, truncated return |
| $G_t^{(\infty)}$ | episode 전체 reward | Monte Carlo, no bootstrapping |
{: .policy-comparison-table}

#### DQN의 multi-step loss

Q-learning에서는 $V(S_{t+n})$ 대신 next state에서의 최대 Q-value를 사용한다. $n$-step reward를 다음과 같이 정의하면,

$$
r_{t+1}^{(n)}
= \sum_{k=0}^{n-1}\gamma^k r_{t+k+1}
$$

DQN의 $n$-step target과 loss는 다음과 같이 쓸 수 있다.

$$
y_t^{(n)}
= r_{t+1}^{(n)}
  +\gamma^n\max_a\hat{Q}(s_{t+n},a;\hat{\theta})
$$

$$
L(\theta)
= \frac{1}{2B}\sum_{i\in B}
\left[
r_{i+1}^{(n)}+\gamma^n\max_a\hat{Q}(s_{i+n},a;\hat{\theta})
-Q(s_i,a_i;\theta)
\right]^2
$$

$n$이 커질수록 더 많은 실제 reward를 사용하므로 bootstrapping bias는 줄어들 수 있지만, sample return의 variance가 커지고 더 긴 transition sequence가 필요하다. 반대로 $n=1$이면 update가 빠르고 분산이 작지만 next value estimate에 더 크게 의존한다. 따라서 $n$의 선택에 따라 성능과 안정성이 달라진다.

### Double DQN

기본 Q-learning은 action selection과 action evaluation에 같은 Q function을 사용한다.

$$
Q(S,A)\leftarrow Q(S,A)
+\alpha\left[R+\gamma\max_a Q(S',a)-Q(S,A)\right]
$$

Q estimate에는 sample noise가 포함되어 있기 때문에, 여러 action 중 최댓값을 고르는 과정에서 실제 value보다 큰 값을 선택하는 **overestimation bias**가 발생할 수 있다. 같은 Q function으로 최댓값을 선택하고 그 값을 평가하기 때문에 생기는 문제이다.

#### Double Q-learning

Double Q-learning은 두 개의 Q estimate $Q_1,Q_2$를 사용하여 action selection과 action evaluation을 분리한다. 예를 들어 $Q_1$을 update할 때는 $Q_1$으로 action을 선택하고 $Q_2$로 그 action을 평가한다.

$$
Q_1(S,A)\leftarrow Q_1(S,A)
+\alpha\left[
R+\gamma Q_2\left(S',\arg\max_a Q_1(S',a)\right)-Q_1(S,A)
\right]
$$

반대로 $Q_2$를 update할 때는 $Q_2$로 action을 선택하고 $Q_1$으로 평가한다.

$$
Q_2(S,A)\leftarrow Q_2(S,A)
+\alpha\left[
R+\gamma Q_1\left(S',\arg\max_a Q_2(S',a)\right)-Q_2(S,A)
\right]
$$

보통 매 update에서 두 Q function 중 어느 것을 update할지 확률적으로 선택한다. 두 Q function을 분리하면 하나의 Q function이 우연히 크게 추정한 값을 그대로 target으로 평가하는 현상을 줄일 수 있다.

#### Double DQN의 target

Double DQN에서는 online Q-network가 next state에서 target action을 선택하고, target Q-network가 그 action의 value를 평가한다.

$$
a^* = \arg\max_a Q(s_{t+1},a;\theta)
$$

$$
y_t^{\mathrm{Double}}
= r_{t+1}+\gamma\hat{Q}(s_{t+1},a^*;\hat{\theta})
$$

따라서 target과 evaluation에 같은 network를 사용하는 기본 DQN보다 overestimation bias를 줄일 수 있다. Online network와 target network를 함께 사용하는 DQN의 구조를 action selection과 action evaluation의 분리에 활용한 것이다.

#### DQN에 Double Q-learning 아이디어 적용하기

Overestimation이 모든 action에 대해 동일하게 발생한다면 action 사이의 순서가 바뀌지 않으므로 greedy policy 선택에는 큰 영향을 주지 않는다. 반면 특정 action의 Q값만 크게 overestimate되면 실제로는 좋지 않은 action이 최댓값을 갖는 것처럼 보일 수 있고, policy가 잘못된 action을 선택하게 된다.

기본 DQN은 이미 online Q-network와 target Q-network를 따로 사용하고 있으므로, 이 두 network를 action selection과 action evaluation에 나누어 사용할 수 있다.

기본 DQN의 target과 loss는 다음과 같다.

$$
y_t^{\mathrm{DQN}}
= r_{t+1}+\gamma\max_a\hat{Q}(s_{t+1},a;\hat{\theta})
$$

$$
L_{\mathrm{DQN}}(\theta)
= \left[y_t^{\mathrm{DQN}}-Q(s_t,a_t;\theta)\right]^2
$$

이 식에서는 target Q-network가 action을 고르고 그 action의 value도 평가한다. Double DQN에서는 online Q-network가 action을 선택하고, target Q-network가 선택된 action의 value를 평가한다.

$$
a^*_{t+1}
= \arg\max_a Q(s_{t+1},a;\theta)
$$

$$
y_t^{\mathrm{Double}}
= r_{t+1}+\gamma\hat{Q}(s_{t+1},a^*_{t+1};\hat{\theta})
$$

따라서 Double DQN의 loss는 다음과 같다.

$$
L_{\mathrm{Double\ DQN}}(\theta)
= \left[
r_{t+1}+\gamma\hat{Q}\left(
s_{t+1},\arg\max_a Q(s_{t+1},a;\theta);\hat{\theta}
\right)
-Q(s_t,a_t;\theta)
\right]^2
$$

이렇게 action selection과 action evaluation을 서로 다른 network로 분리하면, 한 network의 우연한 overestimation이 선택과 평가에 동시에 반영되는 것을 줄일 수 있다.

#### Double DQN with Prioritized Experience Replay

Double DQN과 Prioritized Experience Replay를 함께 사용하면 action selection/evaluation을 분리하면서 동시에 TD error가 큰 transition을 더 자주 학습할 수 있다. 아래 알고리즘에서 기본 DQN과 달라진 부분은 색으로 표시했다.

- 파란색: Double DQN의 action selection과 action evaluation 분리
- 보라색: priority sampling과 importance sampling

{% capture double_dqn_per_algorithm %}
$$
\begin{array}{l}
\textbf{Hyperparameters: }B,K,N,\alpha_{\mathrm{PER}},\beta \\
\textbf{Initialize replay buffer }\mathcal{R}\text{ to capacity }N,\quad \Delta\leftarrow0,\quad p_1\leftarrow1 \\
\textbf{Observe state }s_1 \\
\textbf{For }t=1,\ldots,T\textbf{:} \\
\quad\quad \text{Select }a_t\text{ using }\epsilon\text{-greedy policy derived from }Q(s_t,a;\theta) \\
\quad\quad \text{Execute }a_t\text{ and observe }r_{t+1},s_{t+1} \\
\quad\quad {\color{purple}{\mathcal{R}\leftarrow\mathcal{R}\cup\{(s_t,a_t,r_{t+1},s_{t+1})\}\text{ with priority }p_t\leftarrow\max_{i<t}p_i}} \\
\quad\quad \textbf{If }t\equiv0\pmod K\textbf{ then:} \\
\quad\quad\quad\quad \textbf{For }i=1,\ldots,B\textbf{:} \\
\quad\quad\quad\quad\quad\quad {\color{purple}{i\sim P(i)=\dfrac{p_i^{\alpha_{\mathrm{PER}}}}{\sum_kp_k^{\alpha_{\mathrm{PER}}}}}} \\
\quad\quad\quad\quad\quad\quad {\color{purple}{w_i\leftarrow\dfrac{(NP(i))^{-\beta}}{\max_{j\in B}(NP(j))^{-\beta}}}} \\
\quad\quad\quad\quad\quad\quad {\color{blue}{\delta_i\leftarrow r_{i+1}+\gamma\hat{Q}\left(s_{i+1},\operatorname*{arg\,max}_aQ(s_{i+1},a;\theta);\hat{\theta}\right)-Q(s_i,a_i;\theta)}} \\
\quad\quad\quad\quad\quad\quad {\color{purple}{p_i\leftarrow\lvert\delta_i\rvert}} \\
\quad\quad\quad\quad\quad\quad {\color{purple}{\Delta\leftarrow\Delta+w_i\delta_i\nabla_\theta Q(s_i,a_i;\theta)}} \\
\quad\quad\quad\quad \textbf{Update }\theta\leftarrow\theta+\eta\Delta,\quad\Delta\leftarrow0 \\
\quad\quad\quad\quad \textbf{Every }C\text{ updates set }\hat{\theta}\leftarrow\theta
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Algorithm 2. Double DQN with Prioritized Experience Replay" label="algorithm:double-dqn-prioritized-replay" math=double_dqn_per_algorithm %}

### Dueling DQN

Dueling DQN은 기존 DQN의 Q-value 추정 구조를 개선한 방법이다. 기존 DQN은 state를 입력받아 각 action의 Q-value를 바로 출력하지만, Dueling DQN은 state의 가치와 action의 상대적인 이점을 분리해서 학습한다.

#### Dueling DQN을 사용하는 이유

어떤 state에서는 어떤 action을 선택해도 결과가 거의 달라지지 않을 수 있다. 이런 경우에는 action마다 Q-value를 별도로 학습하는 것보다, 현재 state 자체가 얼마나 좋은지를 나타내는 state value $V(s)$를 먼저 학습하는 것이 효율적이다.

반대로 action에 따라 결과가 크게 달라지는 state에서는 특정 action이 평균적인 action보다 얼마나 좋은지를 나타내는 advantage $A(s,a)$가 중요하다. Dueling DQN은 이 두 정보를 분리해 학습한다.

#### Network 구조

![DQN과 Dueling DQN의 network 구조 비교](/assets/img/blog/deep-reinforcement-learning-summary-4/dueling-dqn-architecture.png)

CNN feature extraction 부분은 기존 DQN과 공유하지만, 이후 fully connected layer를 두 개의 stream으로 나눈다.

- **Value stream**: state 자체의 가치 $V(s)$를 추정한다.
- **Advantage stream**: state $s$에서 action $a$를 선택하는 것이 평균적인 action보다 얼마나 좋은지 $A(s,a)$를 추정한다.

두 stream의 결과를 결합(aggregate)하여 Q-value를 계산한다.

$$
Q(s,a;\theta,\alpha,\beta)
= V(s;\theta,\beta)+A(s,a;\theta,\alpha)
$$

여기서 state $s$가 고정되었을 때 $V(s)$는 action에 관계없이 하나의 scalar 값이고, $A(s,a)$는 action마다 하나씩 존재하는 vector이다. action의 개수가 $m$개라면 다음과 같이 표현할 수 있다.

$$
\mathbf{A}(s)=
\begin{bmatrix}
A(s,a_1)\\
\vdots\\
A(s,a_m)
\end{bmatrix},
\qquad
\mathbf{1}_m=
\begin{bmatrix}
1\\
\vdots\\
1
\end{bmatrix}
$$

따라서 scalar인 $V(s)$를 action 개수만큼 복사하여 vector로 만든 뒤 advantage vector에 더한다.

$$
\mathbf{Q}(s)=V(s)\mathbf{1}_m+\mathbf{A}(s)
$$

Mean aggregation을 사용하는 경우에는 평균 advantage도 action 차원에 대해 broadcast하여 같은 방식으로 뺀다.

$$
\mathbf{Q}(s)
=V(s)\mathbf{1}_m
+\left[\mathbf{A}(s)-\overline{A}(s)\mathbf{1}_m\right]
$$

즉, $V(s)$는 state마다 달라지는 값이지만, 하나의 state 안에서는 모든 action에 공통으로 더해지는 값이다. 반면 $A(s,a)$는 각 action별로 다른 값을 가지며, action 간 상대적인 차이를 표현한다.

여기서 $\theta$는 CNN feature extractor의 parameter, $\beta$는 value stream의 parameter, $\alpha$는 advantage stream의 parameter이다.

#### Dueling DQN의 장점

다음은 Atari 게임 Enduro에서 value stream과 advantage stream이 집중하는 부분을 비교한 예시이다.

| 상황 | 시각화 | 해석 |
| --- | --- | --- |
| 차가 멀리 있는 상황 | ![Enduro에서의 value와 advantage 시각화 예시 1](/assets/img/blog/deep-reinforcement-learning-summary-4/dueling-dqn-enduro-value.png) | 어떤 action을 선택해도 결과가 크게 달라지지 않으므로 value stream이 현재 state와 도로의 전체적인 가치에 집중한다. |
| 차가 바로 앞에 있는 상황 | ![Enduro에서의 value와 advantage 시각화 예시 2](/assets/img/blog/deep-reinforcement-learning-summary-4/dueling-dqn-enduro-advantage.png) | action 선택이 중요하므로 advantage stream이 피해야 할 차와 action별 차이에 집중한다. |
{: .policy-comparison-table}

기존 DQN에서는 한 transition의 loss가 선택된 action $Q(s_t,a_t)$에 직접 연결된다. 반면 Dueling DQN에서는 여러 action의 Q-value가 공통 value stream $V(s)$와 결합되어 있으므로, action 선택과 무관하게 state value를 학습하는 데 유리하다.

#### Identifiability issue

단순히 $Q=V+A$로 두면 $V$와 $A$를 유일하게 구분할 수 없다. 임의의 상수 $c$에 대해 다음이 성립하기 때문이다.

$$
Q(s,a) = V(s)+A(s,a)
= \left(V(s)+c\right)+\left(A(s,a)-c\right)
$$

즉, $V$가 $c$만큼 증가하고 $A$가 $c$만큼 감소해도 최종 Q-value는 변하지 않는다. 이를 identifiability issue라고 한다. 따라서 network가 실제로 state value와 advantage를 올바르게 분리해서 학습했는지 보장하기 어렵다.

#### Advantage normalization

이 문제를 해결하기 위해 advantage에 기준을 두어 수렴하는 방법을 취한다. advantage를 optimal action에서 0이 되도록 고정면, identifiability issue를 해결할 수 있다. 이를 위해 Q-value를 다음과 같이 변경한 형태를 사용한다.

$$
Q(s,a;\theta,\alpha,\beta)
= V(s;\theta,\beta)
+\left[A(s,a;\theta,\alpha)
-\max_{a'}A(s,a';\theta,\alpha)\right]
$$

optimal action일때 

$$
a^* = \arg\max_{a'}Q(s,a';\theta,\alpha,\beta)
= \arg\max_{a'}A(s,a';\theta,\alpha)
$$

이 등식이 성립하는 이유는 $V(s;\theta,\beta)$가 action $a'$와 무관하기 때문이다. 특정 state $s$에서 두 action $a_1,a_2$의 Q-value 차이를 계산하면,

$$
\begin{aligned}
Q(s,a_1)-Q(s,a_2)
&=\left[V(s)+A(s,a_1)-\max_{a'}A(s,a')\right] \\
&\quad-\left[V(s)+A(s,a_2)-\max_{a'}A(s,a')\right] \\
&=A(s,a_1)-A(s,a_2)
\end{aligned}
$$

가 된다. 즉, 모든 action에 공통으로 더해지는 $V(s)$와 모든 action에서 공통으로 빼는 $\max_{a'}A(s,a')$는 action 사이의 순서를 바꾸지 않는다. 따라서 Q-value가 가장 큰 action과 advantage가 가장 큰 action은 동일하다.

이제

$$
A_{\max}(s)=\max_{a'}A(s,a';\theta,\alpha)
$$

라고 쓰면, $a^*$의 정의에 의해 $a^*$는 advantage의 최댓값을 만드는 action이다.

$$
A(s,a^*;\theta,\alpha)=A_{\max}(s)
$$

따라서 advantage를 정규화한 값은

$$
A(s,a^*;\theta,\alpha)
-\max_{a'}A(s,a';\theta,\alpha)=0
$$

이 된다. 이 결과를 Q aggregation 식에 대입하면 최적 action의 Q-value는 state value와 같아진다.

$$
Q(s,a^*;\theta,\alpha,\beta)=V(s;\theta,\beta)
$$

예를 들어 어떤 state에서 세 action의 advantage가 각각 $2,1,-1$이고 state value가 $5$라면,

$$
\max_a A(s,a)=2
$$

이고 normalized advantage는 $0,-1,-3$이 된다. 따라서 Q-value는 $5,4,2$가 되며, 가장 큰 advantage를 가진 action의 Q-value가 정확히 $V(s)=5$가 된다.

이 결합 방식은 advantage의 기준점을 고정하여 $V$와 $A$를 보다 안정적으로 분리하도록 돕는다. 앞서 본 max-centering과 달리, 원 논문과 실제 구현에서는 max 대신 action 평균을 빼는 방식이 주로 사용된다.

#### Mean aggregation을 사용하는 이유

실용적인 Dueling DQN에서는 max 대신 advantage의 평균을 빼는 방식을 주로 사용한다.

$$
Q(s,a;\theta,\alpha,\beta)
= V(s;\theta,\beta)
+\left[
A(s,a;\theta,\alpha)
-\frac{1}{|\mathcal{A}|}\sum_{a'}A(s,a';\theta,\alpha)
\right]
$$

Max를 사용하면 advantage를 정규화할 때 가장 큰 advantage를 가진 action 하나에 의존하게 된다. 또한 최댓값 연산은 현재 최댓값을 갖는 action이 바뀌는 지점에서 기준값이 갑자기 변할 수 있다. Mean aggregation은 모든 action의 advantage를 평균내므로 특정 action 하나에만 의존하지 않고, max보다 기준값이 부드럽게 변해 학습 안정성을 높이는 장점이 있다.

Mean aggregation을 사용하면 max-centering에서의 의미인 $A(s,a^*)=0$ 및 $Q(s,a^*)=V(s)$는 더 이상 일반적으로 성립하지 않는다. 대신 normalized advantage의 평균을 0으로 만들고, $V(s)$를 action들에 대한 Q-value의 평균으로 해석한다.

평균 advantage를 빼면 normalized advantage의 평균은 0이 된다.

$$
\frac{1}{|\mathcal{A}|}\sum_a
\left[A(s,a)-\frac{1}{|\mathcal{A}|}\sum_{a'}A(s,a')\right]=0
$$

따라서 mean aggregation에서는 $V(s)$가 action들에 대한 Q-value의 평균이 된다.

$$
V(s)=\frac{1}{|\mathcal{A}|}\sum_a Q(s,a)
$$

이를 직접 확인해 보자. 평균 advantage를

$$
\overline{A}(s)=\frac{1}{|\mathcal{A}|}\sum_{a'}A(s,a')
$$

라고 두면 Q aggregation은 $Q(s,a)=V(s)+A(s,a)-\overline{A}(s)$가 된다. 이 식을 모든 action에 대해 평균내면,

$$
\begin{aligned}
\frac{1}{|\mathcal{A}|}\sum_a Q(s,a)
&=\frac{1}{|\mathcal{A}|}\sum_a
\left[V(s)+A(s,a)-\overline{A}(s)\right] \\
&=V(s)+\overline{A}(s)-\overline{A}(s) \\
&=V(s)
\end{aligned}
$$

이 된다. 즉, 평균을 뺀 advantage들은 action 전체에 대해 평균이 0이 되고, 공통으로 더해져 있던 $V(s)$만 남는다. 그래서 mean aggregation에서 $V(s)$는 특정 action의 value가 아니라 해당 state에서 action들을 평균적으로 평가한 값으로 해석된다.

예를 들어 세 action의 raw advantage가 $3,2,1$이고 $V(s)=5$라면 평균 advantage는 $2$이다. 이를 빼면 normalized advantage는 $1,0,-1$이 되고, Q-value는 $6,5,4$가 된다. 이때 Q-value의 평균은 $5=V(s)$이지만, 최적 action의 Q-value는 $V(s)$와 같지 않다.

Mean을 사용하는 것은 max가 identifiability 문제를 해결하는 데 반드시 필요한 것은 아니라는 뜻이기도 하다. max-centering은 $\max_a A(s,a)=0$이라는 기준을 두고, mean-centering은 $\frac{1}{|\mathcal{A}|}\sum_a A(s,a)=0$이라는 기준을 둔다. 두 방식 모두 advantage에 기준점을 부여해 additive constant의 모호함을 제거한다.

또한 $V(s)$와 평균 advantage $\frac{1}{|\mathcal{A}|}\sum_{a'}A(s,a')$는 action $a$와 무관한 공통값이다. 따라서 모든 action에서 같은 값을 빼더라도 action의 relative rank는 바뀌지 않아 최적 action 자체는 변하지 않는다.

$$
\arg\max_a Q(s,a)=\arg\max_a A(s,a)
$$

## 참고 강의

- [고려대 오승상 강화학습 16 — Deep Reinforcement Learning](https://www.youtube.com/watch?v=TL1RavBMag8)
- [고려대 오승상 강화학습 17 — DQN 1](https://www.youtube.com/watch?v=eBIdI1hntf8)
- [고려대 오승상 강화학습 18 — DQN 2](https://www.youtube.com/watch?v=C-mfKSM0VFQ)
- [고려대 오승상 강화학습 19 — DQN variant](https://www.youtube.com/watch?v=hjXbfFeY1Ac)
- [고려대 오승상 강화학습 20 — Dueling DQN](https://www.youtube.com/watch?v=8E22UY6XXfc)
