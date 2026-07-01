---
layout: post
title: 'Monte-Carlo Tree Search (MCTS) 개념 및 실습'
date: 2026-06-27 00:34:30 +0900
slug: monte-carlo-tree-search-concept-practice
render_with_liquid: true
use_math: true
categories:
- 공부
- 알고리즘
tags:
- algorithm
- planning
- monte-carlo-tree-search
- mcts
---

## 개요

Monte-Carlo Tree Search, 줄여서 MCTS는 AlphaGo 논문에서 AlphaGo를 학습시킨 방법으로 유명해졌다. 물론 내가 그때 처음 들어봤을 수도 있다. 

강화학습에서 주로 쓰이는 알고리즘이고 빈번하게 등장하니까 이번 기회에 한번 다루어보고자 한다.

## MCTS가 필요한 이유

MCTS를 사용하는 이유는 AlphaGo 논문을 생각하면 이해하기 쉽다. 바둑처럼 가능한 경우의 수가 매우 많은 문제에서는 탐색 깊이가 증가할수록 가능한 상태와 action의 조합이 지수적으로 폭발한다. 그래서 모든 경우를 완전 탐색하는 것은 거의 불가능하다.

MCTS는 모든 경우의 수를 전부 탐색하는 대신, 현재 상태에서 가능한 미래를 여러 번 샘플링하고 rollout한 뒤, 그 결과로 얻은 보상을 평균내어 각 선택의 가치를 추정한다. 즉, 모든 미래를 정확히 계산하는 것이 아니라 일부 미래를 무작위로 경험해보고, 어느 선택이 더 좋은지를 통계적으로 판단하는 방식이다.

## MCTS의 문제 설정

MCTS를 적용하려면 먼저 문제를 state, action, transition, reward 관점에서 바라볼 수 있어야 한다. 이때 자주 사용하는 표현 방식이 Markov Decision Process(MDP)이다. MDP는 다음 상태가 과거 전체 history가 아니라 현재 state와 현재 action에만 의존한다고 가정한다.

MDP는 보통 다음 네 가지 요소로 모델링된다.

$$
(\mathcal{S}, \mathcal{A}_s, P_a, R_a)
$$

- $\mathcal{S}$는 환경에서 가능한 state의 집합이다. 초기 state는 $s_0 \in \mathcal{S}$로 표현한다.
- $\mathcal{A}_s$는 특정 state $s$에서 사용할 수 있는 action의 집합이다.
- $P_a(s, s')$는 state $s$에서 action $a$를 수행했을 때 다음 state $s'$로 transition될 확률을 나타낸다.
- $R_a(s)$는 action $a$에 의해 state $s$에 도달했을 때 받는 reward를 나타낸다.

## 주요 특징

1. $Q(s, a)$는 state $s$에서 action $a$를 선택했을 때의 가치를 의미한다. MCTS에서는 이 값을 모든 미래를 정확히 계산해서 구하지 않고, 여러 번의 random simulation을 통해 근사한다.
2. Single-agent problem에서는 ExpectiMax search tree를 점진적으로 구성한다. 여기서 ExpectiMax tree란, 현재 선택 이후 가능한 미래 state들을 tree로 펼치고, simulation 결과의 평균을 통해 각 action의 기대값을 추정하는 구조를 의미한다.
3. Search는 미리 정의한 연산 시간이나 최대 확장 node 수에 도달하면 종료된다. 탐색을 끝까지 완료하지 못하더라도, 지금까지의 simulation 결과로 근사한 $Q(s, a)$를 기준으로 현재까지 가장 좋은 action $a^{*} = \arg\max_{a \in \mathcal{A}(s)} Q(s, a)$를 얻을 수 있다.
4. 탐색이 끝나면 가장 성능이 좋은 action $a^{*}$를 return한다.

## 알고리즘 흐름

기본적인 MCTS 알고리즘은 다음 단계를 반복적으로 수행한다.

- Selection: 자식 node가 하나 이상 있는 상황에서, 자식 node 중 하나를 선택한다.
- Expansion: 선택된 node에서 가능한 action을 사용해 새로운 child node로 확장한다.
- Simulation / Rollout: 확장된 node에서 terminal state에 도달할 때까지 simulation한다.
- Backpropagation: simulation 결과로 얻은 value를 root node 방향으로 전달한다.

![MCTS phases](/assets/img/blog/monte-carlo-tree-search-concept-practice/mcts-phases.png)

기본적으로 MCTS tree 안의 각 node는 다음 정보를 저장한다.

1. 자식 node의 집합
2. parent node와 parent에서 현재 node로 이동할 때 사용한 action에 대한 pointer
3. 해당 node를 몇 번 방문했는지 나타내는 visit count
4. simulation 결과로부터 누적된 value 또는 reward 통계

전체 흐름을 pseudocode로 쓰면 다음과 같다.

{% capture mcts_algorithm %}
$$
\begin{array}{l}
\textbf{Input : } M = \langle \mathcal{S}, s_0, \mathcal{A}, P_a(s' \mid s), r(s,a,s') \rangle,\ Q,\ B \\
\textbf{Output : } Q \\[1mm]
\textbf{while } \mathrm{current\_time} < B\ \textbf{do} \\
\quad\quad v \leftarrow \operatorname{Select}(s_0) \\
\quad\quad v' \leftarrow \operatorname{Expand}(v) \\[1mm]
\quad\quad \textbf{if } v'\ \text{is terminal}\ \textbf{then} \\
\quad\quad\quad\quad T \leftarrow v' \\
\quad\quad \textbf{else} \\
\quad\quad\quad\quad T \leftarrow \operatorname{Simulate}(v') \\[1mm]
\quad\quad G \leftarrow R(T) \\
\quad\quad \operatorname{Backpropagate}(v, v', Q, G) \\[1mm]
\textbf{return } Q
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Algorithm 1. Monte-Carlo Tree Search" label="algorithm:single-agent-mcts" math=mcts_algorithm %}

### Selection

![Selection](/assets/img/blog/monte-carlo-tree-search-concept-practice/selection.png)

{% capture mcts_select_algorithm %}
$$
\begin{array}{l}
\textbf{Input : } \text{state } s \in \mathcal{S} \\
\textbf{Output : } \text{unexpanded state } s \\[1mm]
\textbf{while } s\ \text{is fully expanded and non-terminal}\ \textbf{do} \\
\quad\quad \text{Select action } a\ \text{using a multi-armed bandit algorithm} \\
\quad\quad \text{Choose one outcome } s'\ \text{according to } P_a(s' \mid s) \\
\quad\quad s \leftarrow s' \\[1mm]
\textbf{return } s
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Function -- Select(s)" label="algorithm:mcts:select" math=mcts_select_algorithm %}

Selection은 root node에서 시작한다. 현재 node에서 이미 확장된 child node가 있다면, selection policy에 따라 다음 child node를 선택하면서 tree 아래로 내려간다. 이때 다음 node를 선택한다는 말은 실제로는 그 방향으로 이어지는 action 또는 branch를 선택한다는 의미에 가깝다. 선택한 action을 적용한 뒤 도달하는 다음 state $s'$는 transition probability $P_a(s' \mid s)$에 의해 결정된다.
이 과정은 terminal state에 도달하거나, 아직 확장하지 않은 action이 남아 있는 node에 도착했을 때 종료된다. 즉 Selection은 이미 만들어진 tree 안에서 어디까지 내려갈지를 결정하는 단계이다.

{% capture multi_armed_bandit_callout %}
슬롯 머신이 여러 대 있다고 생각해보자. 각 머신은 누를 때마다 결과가 조금씩 다르고, 평균적으로 어느 머신이 좋은지는 처음에 알 수 없다.

이때 좋은 선택을 하기 위해서는 두 가지를 함께 고려해야 한다.

1. 좋아 보이는 머신을 더 눌러서 이득을 얻는다.
2. 아직 충분히 눌러보지 않은 머신도 확인한다.

첫 번째는 exploitation이고, 두 번째는 exploration이다. Multi-Armed Bandit은 이 둘의 균형을 잡는 문제로 볼 수 있다.

MCTS에서는 보통 Upper Confidence bounds applied to Trees, 즉 UCT를 사용한다. UCT는 뒤에서 좀 더 자세히 다룰 예정이다.
{% endcapture %}

{% include callout.html type="note" title="Multi-Armed Bandit이란" content=multi_armed_bandit_callout %}

### Expansion

![Expansion](/assets/img/blog/monte-carlo-tree-search-concept-practice/expansion.png)

Expansion은 Selection에서 branch를 선택한 뒤, 해당 action을 적용해 새로운 state $s'$를 확장하는 단계이다. 이때 다음 state $s'$는 transition probability $P_a(s' \mid s)$에 따라 결정된다. 이렇게 도달한 next state는 tree memory 안에 child node로 추가된다.
새로 추가된 node가 terminal state라면 별도의 simulation 없이 바로 Backpropagation으로 넘어갈 수 있다. 그렇지 않다면 이 node에서 Simulation / Rollout을 시작한다.

{% capture mcts_expand_algorithm %}
$$
\begin{array}{l}
\textbf{Input : } \text{state } s \in \mathcal{S} \\
\textbf{Output : } \text{expanded state } s' \\[1mm]
\textbf{if } s\ \text{is not fully expanded}\ \textbf{then} \\
\quad\quad \text{Randomly select an untried action } a\ \text{to apply in } s \\
\quad\quad \text{Expand one outcome } s'\ \text{according to } P_a(s' \mid s) \\
\quad\quad \text{Observe reward } r \\[1mm]
\textbf{return } s'
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Function -- Expand(s)" label="algorithm:mcts:expand" math=mcts_expand_algorithm %}

### Simulation / Rollout

![Simulation](/assets/img/blog/monte-carlo-tree-search-concept-practice/simulation.png)

Simulation은 Expansion으로 새로 추가된 node의 state $s'$에서 시작해 terminal state $T$에 도달할 때까지 진행된다. 이 단계에서는 현재 state $s_t$에서 action $a_t$를 선택하고, 해당 action에 대한 transition probability

$$
P_{a_t}(s_{t+1} \mid s_t)
$$

에 따라 다음 state $s_{t+1}$를 샘플링하는 과정을 반복한다.

$$
s'
\xrightarrow{a_0}
s_1
\xrightarrow{a_1}
s_2
\rightarrow \cdots \rightarrow T
$$

기본적인 MCTS에서는 rollout 중 action을 무작위로 선택하는 random policy를 사용한다. 따라서 rollout은 새로 확장된 선택이 이후에 어떤 결과로 이어질지를 하나의 sample path로 만들어 보는 과정이다.

다만 simulation은 반드시 완전히 무작위로 수행될 필요는 없다. 예를 들어 목표에 가까워지는 action, 충돌 가능성이 낮은 action, 비용이 낮을 것으로 예상되는 action을 더 자주 선택하도록 heuristic policy를 사용할 수 있다. 이 경우에도 simulation의 본질은 동일하다. 즉, 아직 탐색 tree에 명시적으로 저장되지 않은 미래를 하나 샘플링하여 현재 선택의 결과를 추정하는 단계이다.

그림의 $T$는 rollout이 도달한 terminal state를 의미한다. Simulation이 끝나면 시작 state $s'$부터 terminal state $T$까지 얻은 누적 결과를 return $G$로 계산한다. rollout 길이를 $K$라고 하면 다음과 같이 쓸 수 있다.

$$
G = \sum_{t=0}^{K-1} r_t
$$

할인율 $\gamma^t$ 을 사용하는 경우에는 다음과 같이 계산할 수 있다.

$$
G
=
\sum_{t=0}^{K-1}
\gamma^t r_t
$$

이 값은 현재 선택이 얼마나 좋은지를 추정하기 위한 하나의 sample로 사용된다.

또한 simulation 과정에서 생성되는 임시 state들은 기본적인 MCTS에서는 tree memory에 저장하지 않는다. Simulation이 끝나면 rollout 결과인 $G$만 새로 확장된 node $s'$와 그 조상 node들에 전달되어 Backpropagation에 사용된다.

### Backpropagation

![Backpropagation](/assets/img/blog/monte-carlo-tree-search-concept-practice/backpropagation.png)



{% capture mcts_backpropagation_algorithm %}
$$
\begin{array}{l}
\textbf{Input : } \text{state-action pair } (s,a),\ Q:\mathcal{S}\times\mathcal{A}\rightarrow\mathbb{R},\ G\in\mathbb{R} \\
\textbf{Output : } \text{none} \\[1mm]
\textbf{do} \\
\quad\quad N(s,a) \leftarrow N(s,a) + 1 \\
\quad\quad G \leftarrow r + \gamma G \\
\quad\quad Q(s,a) \leftarrow Q(s,a) + \frac{1}{N(s,a)}\left[G - Q(s,a)\right] \\
\quad\quad s \leftarrow \text{parent of } s \\
\quad\quad a \leftarrow \text{parent action of } s \\[1mm]
\textbf{while } s \ne s_0
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Function -- Backpropagation(s, a, Q, G)" label="algorithm:mcts:backpropagation" math=mcts_backpropagation_algorithm %}

Backpropagation은 Simulation에서 얻은 return $G$를 현재 node에서 root node 방향으로 거슬러 올라가며 반복적으로 반영하는 단계이다. 이때 discount factor $\gamma$를 함께 고려해야 한다. terminal state에서 얻은 결과를 그대로 올리는 것이 아니라, 한 단계 위로 올라갈 때마다 현재 step의 reward와 discounted future return을 합쳐서 전달한다.

각 state $s$와 action $a$는 Selection 단계에서 선택된 state-action pair이다. Backpropagation에서는 이 pair의 visit count $N(s,a)$를 증가시키고, 해당 선택에서 관측된 누적 return을 이용해 $Q(s,a)$를 업데이트한다. 같은 state-action pair가 여러 번 방문되면 $Q(s,a)$는 여러 rollout에서 얻은 return의 평균값에 가까워진다.

action의 결과는 transition probability $P_a(s' \mid s)$에 따라 샘플링된다. 따라서 rollout을 충분히 반복하면 $Q(s,a)$는 해당 action을 선택했을 때 얻을 수 있는 return의 기댓값, 즉 expected return을 추정하게 된다. 이 관점에서 MCTS가 점진적으로 만드는 tree를 ExpectiMax tree의 sampling-based approximation으로 볼 수 있다. 최종적으로는 각 state에서 expected return이 큰 action을 선택하는 방향으로 탐색이 진행된다.

## UCT

-

## 간단한 예제

-

## 구현 실습

-

## 정리

-

## Reference

- [Monte Carlo Tree Search: A Review of Recent Modifications and Applications](https://arxiv.org/pdf/2103.04931)
- [Monte-Carlo Tree Search (MCTS)](https://gibberblot.github.io/rl-notes/single-agent/mcts.html)
