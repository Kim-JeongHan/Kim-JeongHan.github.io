---
layout: post
title: 'Monte-Carlo Tree Search (MCTS) 개념'
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

Monte-Carlo Tree Search, 줄여서 MCTS는 AlphaGo에서 다음 수를 선택하기 위한 search/planning 방법으로 사용되며 유명해졌다. 물론 내가 그때 처음 들어봤을 수도 있다.

강화학습에서 주로 쓰이는 알고리즘이고 빈번하게 등장하니까 이번 기회에 한번 다루어보고자 한다.

## MCTS가 필요한 이유

MCTS를 사용하는 이유는 AlphaGo 논문을 생각하면 이해하기 쉽다. 바둑처럼 가능한 경우의 수가 매우 많은 문제에서는 탐색 깊이가 증가할수록 가능한 상태와 action의 조합이 지수적으로 폭발한다. 그래서 모든 경우를 완전 탐색하는 것은 거의 불가능하다.

MCTS는 모든 경우의 수를 전부 탐색하는 대신, 현재 상태에서 가능한 미래를 여러 번 샘플링하고 rollout한 뒤, 그 결과로 얻은 보상을 평균내어 각 선택의 가치를 추정한다. 즉, 모든 미래를 정확히 계산하는 것이 아니라 일부 미래를 무작위로 경험해보고, 어느 선택이 더 좋은지를 통계적으로 판단하는 방식이다.

## MCTS의 문제 설정

MCTS를 적용하려면 먼저 문제를 state, action, transition, reward 관점에서 바라볼 수 있어야 한다. 이때 자주 사용하는 표현 방식이 Markov Decision Process(MDP)이다. MDP는 다음 상태가 과거 전체 history가 아니라 현재 state와 현재 action에만 의존한다고 가정한다.

MDP는 보통 다음 네 가지 요소로 모델링된다.

$$
(\mathcal{S}, \mathcal{A}, P, r)
$$

- $\mathcal{S}$는 환경에서 가능한 state의 집합이다. 초기 state는 $s_0 \in \mathcal{S}$로 표현한다.
- $\mathcal{A}(s)$는 특정 state $s$에서 사용할 수 있는 action의 집합이다.
- $P(s' \mid s,a)$는 state $s$에서 action $a$를 수행했을 때 다음 state $s'$로 transition될 확률을 나타낸다.
- $r(s,a,s')$는 state $s$에서 action $a$를 수행해 state $s'$에 도달했을 때 받는 reward를 나타낸다.

## 주요 특징

1. $Q(s, a)$는 state $s$에서 action $a$를 선택했을 때의 가치를 의미한다. MCTS에서는 이 값을 구할때, 모든 미래를 정확히 계산해서 구하지 않고, 여러 번의 random simulation을 통해 근사한다.
2. 이 글에서는 우선 single-agent problem 관점에서 MCTS를 설명한다. 이 경우 MCTS는 ExpectiMax search tree를 점진적으로 구성한다고 볼 수 있다. 여기서 ExpectiMax tree란, 현재 선택 이후 가능한 미래 state들을 tree로 펼치고, simulation 결과의 평균을 통해 각 action의 기대값을 추정하는 구조를 의미한다.
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
\textbf{Input : } M = \langle \mathcal{S}, s_0, \mathcal{A}, P(s' \mid s,a), r(s,a,s') \rangle,\ Q,\ B \\
\textbf{Output : } Q \\[1mm]
\textbf{while } \mathrm{current\_time} < B\ \textbf{do} \\
\quad\quad v \leftarrow \operatorname{Select}(s_0) \\
\quad\quad v' \leftarrow \operatorname{Expand}(v) \\
\quad\quad G \leftarrow \operatorname{Simulate}(v') \\
\quad\quad \operatorname{Backpropagate}(v', Q, G) \\[1mm]
\textbf{return } Q
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Algorithm 1. Monte-Carlo Tree Search" label="algorithm:single-agent-mcts" math=mcts_algorithm %}

여기서 $\operatorname{Simulate}(v')$는 $v'$에서 terminal state까지 rollout을 수행하고, 그 과정에서 얻은 누적 return $G$를 반환한다고 보면 된다. 만약 $v'$가 이미 terminal node라면 별도의 rollout 없이 terminal reward로부터 $G$를 계산할 수 있다.

### Selection

![Selection](/assets/img/blog/monte-carlo-tree-search-concept-practice/selection.png)

{% capture mcts_select_algorithm %}
$$
\begin{array}{l}
\textbf{Input : } \text{state } s \in \mathcal{S} \\
\textbf{Output : } \text{unexpanded state } s \\[1mm]
\textbf{while } s\ \text{is fully expanded and non-terminal}\ \textbf{do} \\
\quad\quad \text{Select action } a\ \text{using a multi-armed bandit algorithm} \\
\quad\quad \text{Choose one outcome } s'\ \text{according to } P(s' \mid s,a) \\
\quad\quad s \leftarrow s' \\[1mm]
\textbf{return } s
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Function -- Select(s)" label="algorithm:mcts:select" math=mcts_select_algorithm %}

Selection은 root node에서 시작한다. 현재 node에서 이미 확장된 child node가 있다면, selection policy에 따라 다음 child node를 선택하면서 tree 아래로 내려간다. 이때 다음 node를 선택한다는 말은 실제로는 그 방향으로 이어지는 action 또는 branch를 선택한다는 의미에 가깝다. 선택한 action을 적용한 뒤 도달하는 다음 state $s'$는 transition probability $P(s' \mid s,a)$에 의해 결정된다.
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

Expansion은 Selection에서 branch를 선택한 뒤, 해당 action을 적용해 새로운 state $s'$를 확장하는 단계이다. 이때 다음 state $s'$는 transition probability $P(s' \mid s,a)$에 따라 결정된다. 이렇게 도달한 next state는 tree memory 안에 child node로 추가된다.
새로 추가된 node가 terminal state라면 별도의 simulation 없이 바로 Backpropagation으로 넘어갈 수 있다. 그렇지 않다면 이 node에서 Simulation / Rollout을 시작한다.

{% capture mcts_expand_algorithm %}
$$
\begin{array}{l}
\textbf{Input : } \text{state } s \in \mathcal{S} \\
\textbf{Output : } \text{expanded state } s' \\[1mm]
\textbf{if } s\ \text{is not fully expanded}\ \textbf{then} \\
\quad\quad \text{Randomly select an untried action } a\ \text{to apply in } s \\
\quad\quad \text{Expand one outcome } s'\ \text{according to } P(s' \mid s,a) \\
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
P(s_{t+1} \mid s_t, a_t)
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
\textbf{Input : } \text{expanded node } v,\ Q:\mathcal{S}\times\mathcal{A}\rightarrow\mathbb{R},\ G\in\mathbb{R} \\
\textbf{Output : } \text{none} \\[1mm]
\textbf{while } v\ \text{has parent}\ \textbf{do} \\
\quad\quad s \leftarrow \operatorname{state}(\operatorname{parent}(v)) \\
\quad\quad s' \leftarrow \operatorname{state}(v) \\
\quad\quad a \leftarrow \operatorname{action}(\operatorname{parent}(v), v) \\
\quad\quad G \leftarrow r(s,a,s') + \gamma G \\
\quad\quad N(s,a) \leftarrow N(s,a) + 1 \\
\quad\quad Q(s,a) \leftarrow Q(s,a) + \frac{1}{N(s,a)}\left[G - Q(s,a)\right] \\
\quad\quad v \leftarrow \operatorname{parent}(v)
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Function -- Backpropagation(v, Q, G)" label="algorithm:mcts:backpropagation" math=mcts_backpropagation_algorithm %}

Backpropagation은 Simulation에서 얻은 return $G$를 확장된 node $v'$에서 root node 방향으로 거슬러 올라가며 반복적으로 반영하는 단계이다. 이때 discount factor $\gamma$를 함께 고려해야 한다. terminal state에서 얻은 결과를 그대로 올리는 것이 아니라, 한 단계 위로 올라갈 때마다 해당 edge의 immediate reward와 discounted future return을 합쳐서 전달한다.

각 state $s$와 action $a$는 tree 안에서 parent node에서 child node로 이동할 때 실제로 사용된 state-action pair이다. Backpropagation에서는 이 pair의 visit count $N(s,a)$를 증가시키고, 해당 선택에서 관측된 누적 return을 이용해 $Q(s,a)$를 업데이트한다. 같은 state-action pair가 여러 번 방문되면 $Q(s,a)$는 여러 rollout에서 얻은 return의 평균값에 가까워진다.

action의 결과는 transition probability $P(s' \mid s,a)$에 따라 샘플링된다. 따라서 rollout을 충분히 반복하면 $Q(s,a)$는 해당 action을 선택했을 때 얻을 수 있는 return의 기댓값, 즉 expected return을 추정하게 된다. 이 관점에서 MCTS가 점진적으로 만드는 tree를 ExpectiMax tree의 sampling-based approximation으로 볼 수 있다. 최종적으로는 각 state에서 expected return이 큰 action을 선택하는 방향으로 탐색이 진행된다.

## Upper Confidence bounds applied to Trees (UCT)

앞서 Selection 단계에서 multi-armed bandit algorithm을 사용한다고 말했다. 실제 MCTS에서는 UCB1을 tree search에 맞게 약간 변형한 방식이 성능이 좋아서 많이 사용된다. 이 방법을 UCT라고 부른다. 즉, UCT는 MCTS의 Selection 단계에서 어떤 action 또는 branch를 선택할지를 결정하기 위해 UCB 계열의 기준을 사용하는 방법이다.

UCT에서는 현재 state $s$에서 다음 action을 다음과 같이 선택한다.

$$
a^*
=
\arg\max_{a \in A(s)}
\left[
Q(s,a)
+
C_p
\sqrt{
\frac{ \ln N(s)}
{N(s,a)}
}
\right]
$$

여기서 첫 번째 항 $Q(s,a)$는 지금까지의 rollout을 통해 추정한 expected return이다. 이미 좋은 결과를 보인 action을 더 선택하려는 exploitation 항으로 볼 수 있다. 두 번째 항은 아직 충분히 선택되지 않은 action에 더 큰 값을 주는 exploration 항이다.

- $N(s)$는 state node $s$가 방문된 횟수이다.
- $N(s,a)$는 state $s$에서 action $a$가 선택된 횟수이다.
- $C_p > 0$는 exploration을 얼마나 강하게 할지를 결정하는 상수이다. 보통 초기값은 $\sqrt{2}$로 두고, 문제에 따라 조정한다.

$C_p$가 크면 아직 덜 탐색한 action을 더 자주 선택하고, $C_p$가 작으면 현재까지 $Q(s,a)$가 크게 추정된 action을 더 자주 선택한다. 따라서 UCT는 exploitation과 exploration 사이의 균형을 조절하는 Selection policy로 볼 수 있다.

이러한 sampling 기반 탐색과 exploration 항이 함께 작동하기 때문에, MCTS는 minimax와 같은 전통적인 tree search 방법과 달리 tree를 균일하게 펼치지 않는다. 더 유망하거나 더 불확실한 branch에 더 많은 simulation을 할당하면서 tree를 비대칭적으로 확장한다.
즉, 기댓값이 높아 보이는 branch에는 더 많은 계산을 할당하고, 기댓값이 낮아 보이는 branch에는 더 적은 계산을 할당하기 때문에 tree가 불균등한 모양으로 커져 나간다.

### UCB1-Tuned

기존 UCT 수식보다 더 정교한 방법으로 UCB1-Tuned를 사용할 수도 있다. UCB1-Tuned는 기존 UCB1 계열의 식에 action별 reward 분산을 반영하는 항을 추가한다. 직관적으로는 평균 return이 높은 action만 보는 것이 아니라, 해당 action의 rollout 결과가 얼마나 불안정한지도 함께 고려하는 방식이다.

$$
a^*
=
\arg\max_{a \in A(s)}
\left\{
Q(s,a)
+
C
\sqrt{
\frac{\ln N(s)}{N(s,a)}
\,
\min\!\left(
\frac{1}{4},
\sigma_a
+
\frac{2\ln N(s)}{N(s,a)}
\right)
}
\right\}
$$

여기서 $\sigma_a$는 action $a$를 선택했을 때 관측된 rollout return의 분산을 반영하는 항이다. 따라서 UCB1-Tuned는 단순히 방문 횟수만으로 exploration bonus를 정하는 것이 아니라, reward 또는 return의 변동성까지 고려해 exploration 정도를 조절한다.

### Exponential-weight algorithm for Exploration and Exploitation(EXP3)

UCB1이나 UCB1-Tuned는 기본적으로 각 action의 reward distribution이 비교적 안정적이고, 여러 번 시도하면 평균 return이 점점 믿을 만해지는 상황에 잘 맞는다. 반대로 결과가 더 불안정하거나, 선택지의 품질이 시간에 따라 달라질 수 있는 상황에서는 EXP3 같은 adversarial bandit 알고리즘을 사용할 수도 있다.

유한한 횟수의 선택 horizon이 정해져 있을 때, 지금까지 내가 선택한 action들의 누적 성능과 사후적으로 가장 좋았던 단일 action을 계속 선택했을 때의 성능 차이를 regret으로 본다. EXP3는 이 regret이 일정 수준 이상 커지지 않도록 이론적 보장을 제공하는 알고리즘이다.

예를 들어 바둑에서는 내가 둔 수에 따라 상대방의 대응도 달라진다. 초반 rollout에서는 action $A$가 좋아 보였더라도, 이후 상대의 대응이나 탐색 상황이 바뀌면서 action $B$가 더 좋아질 수 있다. 기존 UCT가 누적 평균 return을 강하게 믿는다면 이런 변화에 둔감할 수 있다. EXP3 계열의 방법은 이런 불안정한 reward 상황에 좀 더 강하게 대응하기 위한 선택지로 볼 수 있다.

## 정리

이번 게시글에서 MCTS 알고리즘에 대해 다루어보았다. MCTS는 모든 경우를 완전 탐색하여 최적해를 직접 찾는 방식이 아니다. 대신 현재까지 얻은 rollout 결과를 바탕으로 어떤 선택이 더 좋아 보이는지를 점진적으로 추정하고, 더 유망한 방향에 계산을 더 많이 할당한다.

이를 위해 MCTS는 Selection, Expansion, Simulation, Backpropagation의 네 단계로 구성된다. Selection과 Expansion을 통해 tree에서 탐색할 위치를 정하고, Simulation을 통해 그 선택이 미래에 어떤 결과로 이어질지 샘플링한다. 이후 Backpropagation 단계에서 rollout 결과를 tree의 node들에 반영하여 각 state-action pair의 value estimate를 갱신한다.

MCTS를 사용하려면 선택한 action 이후의 다음 state를 샘플링하고 reward를 계산할 수 있어야 한다. 즉, transition과 reward를 제공하는 simulator 또는 model이 필요하다는 점에서 model-based 방식으로 볼 수 있다.

simulation에 필요한 transition과 reward를 대략적으로라도 모델링할 수 있고, 가능한 미래의 경우의 수가 매우 큰 환경에서는 MCTS가 기존의 완전 탐색이나 단순 sampling 기반 탐색보다 효율적일 수 있다. 결국 MCTS는 반복적인 rollout과 평균화를 통해 $Q(s,a)$를 추정하고, expected return이 큰 action을 선택하는 방향으로 탐색을 진행하는 알고리즘이다.

## Reference

- [Monte Carlo Tree Search: A Review of Recent Modifications and Applications](https://arxiv.org/pdf/2103.04931)
- [Monte-Carlo Tree Search (MCTS)](https://gibberblot.github.io/rl-notes/single-agent/mcts.html)
