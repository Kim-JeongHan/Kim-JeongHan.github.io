---
layout: post
title: '[논문리뷰] Monte Carlo Tree Diffusion for System 2 Planning'
date: 2026-06-27 00:22:22 +0900
slug: paper-review-monte-carlo-tree-diffusion-system-2-planning
render_with_liquid: true
use_math: true
categories:
- 논문리뷰
- diffusion
tags:
- ai
- planning
- diffusion-model
- paper-review
---

## 논문 정보

- Title: Monte Carlo Tree Diffusion for System 2 Planning (ICML 2025 Spotlight)
- Authors: Jaesik Yoon, Hyeonseo Cho, Doojin Baek, Yoshua Bengio, Sungjin Ahn
- Links: [Project](https://jaesikyoon.com/mctd-page/), [Paper](https://arxiv.org/abs/2502.07202), [Code](https://github.com/ahn-ml/mctd)

## 한 줄 요약

- diffusion inference 과정에 MCTS의 exploration-exploitation search를 결합해 long-horizon task에서 기존 diffusion planner보다 좋은 성능을 보인 방법

## 문제 정의

diffusion-based planner는 denoising step을 통해 전체 trajectory를 한 번에 생성하는 방식을 사용한다. 이 접근은 planning 과정에서 forward dynamics model을 명시적으로 rollout할 필요를 줄이고, forward model을 반복적으로 사용할 때 long-term horizon에서 error가 축적되는 문제를 효과적으로 완화한다.

### 기존 방식의 한계

diffusion-based planner와 MCTS는 서로 다른 장점을 갖지만, long-horizon planning에서는 각각 다른 병목을 갖는다. 먼저 diffusion 계열 방법은 trajectory-level generation에는 강하지만, inference-time search를 구조적으로 활용하기 어렵다.

| Diffusion 계열 접근 | 장점 | 한계 |
| --- | --- | --- |
| diffusion-based planner | 전체 trajectory를 한 번에 생성해 forward model rollout에 따른 error accumulation을 줄인다. | reward나 task objective를 직접 반영하기 어렵고, 중간 decision point에서 exploration-exploitation을 구조적으로 다루기 어렵다. |
| denoising step 수 증가 | 더 많은 refinement로 trajectory quality를 높이려 한다. | 초반에는 성능이 좋아지지만 빠르게 plateau에 도달하고 inference cost가 증가한다. |
| sample 수 증가 | 여러 trajectory 후보를 만들고 좋은 sample을 선택할 수 있다. | sample 간 feedback을 공유하지 못하고, long-horizon task에서는 많은 sample을 뽑아도 실패할 수 있다. |

반면 MCTS는 search feedback을 활용해 exploration과 exploitation을 조절할 수 있지만, 전통적인 형태 그대로는 long-horizon continuous planning에 적용하기 어렵다.

| Search 계열 접근 | 장점 | 한계 |
| --- | --- | --- |
| 전통적인 MCTS | simulation feedback을 통해 좋은 선택지를 더 깊게 탐색하고, 덜 탐색한 선택지도 확인할 수 있다. | forward model에 의존하고, step-by-step rollout 때문에 global trajectory consistency를 유지하기 어렵다. |
| discrete action tree search | action branch를 명시적으로 펼쳐 decision point마다 선택을 비교할 수 있다. | action space가 크거나 continuous하면 tree가 깊고 넓어져 계산 비용이 커진다. |

따라서 이 논문은 diffusion model의 trajectory-level generation 능력은 유지하면서, MCTS의 exploration-exploitation search를 denoising process 안에 넣는 방향으로 문제를 설정한다. 핵심 질문은 전체 trajectory를 생성하는 diffusion framework 안에서 어떻게 tree search 구조를 만들고, 이를 통해 inference-time scalability를 높일 수 있는가이다.

## 핵심 아이디어

이 논문은 위 문제를 Monte Carlo Tree Diffusion(MCTD) framework로 해결한다. MCTD는 diffusion denoising 과정을 단순한 iterative refinement가 아니라, MCTS와 유사한 tree-based rollout process로 재구성한다.

핵심 아이디어는 다음 세 가지로 정리할 수 있다.

1. Denoising process를 tree-based rollout process로 재구성한다.
2. Meta-action과 guidance level을 도입해 exploration과 exploitation을 동적으로 조절한다. 이를 통해 diffusion framework 안에서 실행 가능하고 유연한 trajectory refinement를 수행할 수 있다.
3. 빠른 jumpy denoising simulation을 사용해 forward model rollout 없이도 효율적으로 trajectory quality를 평가하고 개선한다.

### Contribution

1. MCTS의 네 단계인 selection, expansion, simulation, backpropagation을 diffusion inference 과정에 결합해 planning 성능을 향상시킨 첫 번째 framework를 제안한다.
2. Denoising as tree rollout, guidance level meta-action, jumpy denoising 기반 fast simulation이라는 세 가지 요소를 도입한다.
3. 이를 통해 long-horizon planning task에서 MCTD가 기존 diffusion planner보다 효율적인 inference-time scaling을 제공함을 보인다.

## Method

### Monte Carlo Tree Search

MCTS는 stochastic simulation을 반복하면서 exploration과 exploitation을 균형 있게 사용하는 planning 알고리즘이다. 전형적인 MCTS는 selection, expansion, simulation, backpropagation의 네 단계로 구성된다.

MCTS의 기본 개념과 알고리즘 흐름은 이전에 작성한 [Monte-Carlo Tree Search (MCTS) 개념](/blog/2026/monte-carlo-tree-search-concept-practice/) 글에서 정리했다.

### Diffusion Model

diffusion model의 trajectory distribution $p_{\theta}$는 그 자체만으로 reward나 task objective를 명시적으로 encode하기 어렵다. 따라서 Diffuser는 선택적으로 heuristic하거나 학습 가능한 guidance function $J_{\phi}(\mathbf{x})$를 함께 사용한다.

$J_{\phi}(\mathbf{x})$는 denoised trajectory $\mathbf{x}$의 value나 return을 예측하는 함수로 볼 수 있다. 이 guidance function을 사용하면 sampling distribution을 다음과 같이 bias할 수 있다.

$$
\tilde{p}_{\theta}(\mathbf{x})
\propto
p_{\theta}(\mathbf{x})
\exp\!\left(J_{\phi}(\mathbf{x})\right)
$$

따라서 각 denoising step에서 $J_{\phi}(\mathbf{x})$의 gradient information은 diffusion model이 생성하는 trajectory를 더 실행 가능하고 높은 return을 갖는 방향으로 조금씩 밀어주는 역할을 한다.

이것은 Diffuser에서 사용하는 일반적인 trajectory-level guidance이고, 뒤에서 설명할 MCTD는 이 guidance 개념을 subplan 단위의 조건부 guidance로 확장한다.

Diffusion Forcing은 trajectory $\mathbf{x}$를 여러 token으로 나누어 다룰 수 있게 확장한다. 이러한 tokenization을 사용하면 각 token이 서로 다른 noise level에서 denoising될 수 있다. 따라서 uncertainty가 높은 상황에서 전체 trajectory를 full noise에서 no noise까지 한 번에 완성할 필요 없이, 필요한 segment만 부분적으로 denoise하면서 trajectory를 구성할 수 있다. 이러한 token-level control은 long-horizon planning처럼 causal consistency가 중요한 문제에서 특히 유용하다.

### Monte Carlo Tree Diffusion

#### Denoising as Tree-Rollout

MCTD는 diffusion model의 trajectory-level generation 능력과 MCTS의 tree search 구조를 연결하기 위해, denoising process를 semi-autoregressive tree rollout으로 재정의한다. 전체 trajectory를 다음과 같이 $S$개의 서로 겹치지 않는 subplan으로 나눈다.

$$
\mathbf{x}
=
(\mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_S),
\qquad
\mathbf{x}_i \cap \mathbf{x}_j = \emptyset
\quad
(i \ne j)
$$

모든 subplan이 같은 global denoising schedule을 공유하는 standard Diffuser와 달리, MCTD는 각 subplan에 독립적인 denoising schedule을 할당한다. 시간적으로 앞선 subplan은 더 낮은 noise level로 먼저 구체화되고, 뒤쪽 subplan은 더 높은 noise level을 유지한 채 앞선 subplan에 조건화되어 점진적으로 denoise된다. 이 구조 덕분에 denoising process는 causal ordering을 따르는 semi-autoregressive tree rollout으로 해석된다.

즉, 전체 trajectory를 한 번에 독립적으로 완성하는 것이 아니라, 먼저 구체화된 앞부분을 조건으로 뒤쪽 trajectory를 점진적으로 refine하는 방식이다.

이를 확률적으로 표현하면 다음과 같이 쓸 수 있다.

$$
p(\mathbf{x})
\approx
\prod_{s=1}^{S}
p\!\left(\mathbf{x}_s \mid \mathbf{x}_{1:s-1}\right)
$$

형식적으로는 autoregressive factorization처럼 보이지만, 실제 구현에서 subplan들을 순차적으로 여러 번 생성하는 것은 아니다. 대신 각 subplan에 서로 다른 noise level을 부여한 하나의 denoising process 안에서 전체 trajectory를 함께 생성한다.

이때 각 subplan $\mathbf{x}_s$는 temporally extended state로 볼 수 있으며, MCTD에서는 개별 state가 아니라 이러한 subplan 단위가 search tree 안의 node로 처리된다.

이 덕분에 search tree는 low-level state transition을 하나씩 펼치는 구조가 아니라, 더 high-level abstraction 위에서 작동할 수 있다. 특히 subplan 수 $S$가 전체 low-level step 수 $N$보다 훨씬 작기 때문에, $S \ll N$, tree depth는 기존 MCTS보다 크게 작아질 수 있다. 예를 들어 논문에서는 경험적으로 $S=5$, $N=500$을 사용한다. 결과적으로 tree depth와 branching 부담을 줄여 효율성과 확장성을 향상시킨다.

따라서 전체 plan $\mathbf{x}$를 denoising하는 과정은, diffuser의 single denoising process 안에서 subplan node들을 순서대로 rollout하는 과정으로 해석할 수 있다.

#### Selection

Selection 단계에서는 UCB를 사용해 현재 node의 child node 중 다음으로 탐색할 node를 선택한다. 전통적인 MCTS와 달리 MCTD의 node는 단일 state가 아니라 temporally extended state인 subplan에 대응된다. 따라서 더 high-level reasoning이 가능하고, tree depth를 줄여 scalability를 개선할 수 있다.

이때 MCTD에서 child branch는 primitive action이 아니라 subplan에 적용된 guidance schedule에 의해 만들어진다. 따라서 UCB는 guidance schedule로 생성된 child branch들의 value와 visit count를 기준으로 다음에 탐색할 branch를 선택한다.

#### Expansion

Expansion 단계에서는 선택된 node에서 새로운 child node를 확장한다. MCTD에서 각 child node는 diffusion model로 생성된 subplan에 대응된다.

이때 어떤 distribution에서 subplan을 sample할지는 meta-action에 의해 결정된다. guidance가 없는 meta-action을 선택하면 subplan은 prior distribution에서 sample되고, guidance가 있는 meta-action을 선택하면 goal-seeking distribution에서 sample된다.

여기서 guidance는 반드시 binary choice일 필요는 없다. $\mathrm{GUIDE}$와 $\mathrm{NO\_GUIDE}$처럼 단순히 둘로 나눌 수도 있지만, 더 다양한 guidance level을 정의해 exploration과 exploitation 사이의 강도를 세밀하게 조절할 수도 있다.

#### Guidance Level as Meta-Action

MCTD는 primitive action을 직접 탐색하지 않는다. 대신 exploration-exploitation tradeoff를 denoising process 안의 meta-action으로 재정의하고, 이를 guidance level로 구현한다. 가장 단순하게 보면 meta-action은 guidance를 사용할지 여부로 나눌 수 있다.

| meta-action | 의미 | 역할 |
| --- | --- | --- |
| guidance 없음 | 데이터만으로 학습된 prior distribution $p_{\theta}(\mathbf{x})$에서 sampling한다. | 새로운 trajectory 후보를 넓게 탐색하는 exploration에 가깝다. |
| guidance 있음 | reward function $r_g(\mathbf{x})$가 정의한 목표를 반영한 goal-directed distribution $p_g(\mathbf{x})$에서 sampling한다. | 이미 좋아 보이는 방향으로 trajectory를 더 강하게 밀어주는 exploitation에 가깝다. |

meta-action과 tree-rollout denoising process를 통합하기 위해, MCTD는 subplan별 guidance schedule $\mathbf{g}$를 정의한다.

$$
\mathbf{g}
=
(g_1, g_2, \ldots, g_S),
\qquad
g_s \in \{\mathrm{GUIDE}, \mathrm{NO\_GUIDE}\}
$$

여기서 각 $g_s$는 subplan $\mathbf{x}_s$에 대응되며, 해당 subplan을 denoise할 때 guidance를 적용할지 여부를 결정한다.

guidance schedule $\mathbf{g}$를 동적으로 조절하면 subplan level에서 exploration과 exploitation의 균형을 맞출 수 있다. 이는 복잡하고 continuous한 action space에서 primitive action을 직접 모두 확장하지 않고도 효율적이고 확장 가능한 planning을 가능하게 한다.

$$
p(\mathbf{x} \mid \mathbf{g})
\approx
\prod_{s=1}^{S}
p\!\left(\mathbf{x}_s \mid \mathbf{x}_{1:s-1},\, g_s\right)
$$

구체적으로 $g_s=\mathrm{NO\_GUIDE}$가 선택되면 subplan $\mathbf{x}_s$는 exploratory tree-rollout prior를 따른다.

$$
p(\mathbf{x}_s \mid \mathbf{x}_{1:s-1})
$$

반대로 $g_s=\mathrm{GUIDE}$가 선택되면 reward-guided distribution을 따른다.

$$
p_g(\mathbf{x}_s \mid \mathbf{x}_{1:s-1})
$$

guided meta-action은 subplan level에서 다음과 같이 표현할 수 있다.

$$
p_g(\mathbf{x}_s \mid \mathbf{x}_{1:s-1})
\propto
p_{\theta}(\mathbf{x}_s \mid \mathbf{x}_{1:s-1})
\exp\!\left(r_g(\mathbf{x}_s)\right)
$$

즉 guidance가 없는 경우에는 diffusion prior를 따라 다양한 trajectory를 탐색하고, guidance가 있는 경우에는 구체적인 reward function이 정의한 목표에 도달하도록 sampling process를 조종한다.

#### Simulation

MCTS에서 simulation step은 선택된 node 이후의 미래가 얼마나 좋은지를 빠르게 평가하는 역할을 한다. MCTD의 simulation 단계에서는 DDIM을 사용한 fast jumpy denoising을 통해 subplan 이후의 future trajectory를 빠르게 생성하고 평가한다. 가능한 평가 방식은 크게 두 가지가 있다.

| 평가 방식 | 장점 | 한계 |
| --- | --- | --- |
| forward dynamics model 사용 | 실제 rollout에 가까운 평가가 가능하다. | long-horizon rollout이 필요해 computationally expensive하다. |
| bootstrapping 기반 추정 | 빠르게 value를 추정할 수 있다. | 미래 trajectory를 충분히 반영하지 못해 부정확할 수 있다. |

MCTD는 이 문제를 DDIM 기반 jumpy denoising simulation으로 다룬다. 선택된 subplan $\mathbf{x}_{1:s}$가 주어졌을 때, 남은 future subplan $\mathbf{x}_{s+1:S}$를 빠르게 denoise하여 future trajectory를 샘플링한다.

$$
\tilde{\mathbf{x}}_{s+1:S}
\sim
p\!\left(
\mathbf{x}_{s+1:S}
\mid
\mathbf{x}_{1:s},
\mathbf{g}
\right)
$$

이 fast denoising process는 더 큰 approximation error를 만들 수 있지만, 계산 효율이 높기 때문에 MCTD의 simulation step에 잘 맞는다. 즉 forward dynamics model rollout 없이도 future trajectory의 quality를 빠르게 평가할 수 있다.

#### Backpropagation

Backpropagation 단계에서는 simulation에서 얻은 평가 결과를 tree의 상위 node들로 전달한다. MCTD에서는 primitive action이 아니라 meta-action 기반 guidance schedule을 사용하므로, 각 subplan에서 선택된 guidance schedule에 대한 value와 visit count가 업데이트된다.

즉 어떤 subplan에서 $\mathrm{GUIDE}$를 사용하는 것이 좋았는지, 또는 $\mathrm{NO\_GUIDE}$를 통해 더 넓게 탐색하는 것이 좋았는지를 tree 안에 누적해 다음 selection 단계에서 활용한다.

### Prospective

![MCTD Two Perspectives](/assets/img/blog/paper-review-monte-carlo-tree-diffusion-system-2-planning/mctd-two-perspectives.png)

위 그림은 MCTD를 MCTS 관점과 diffusion 관점에서 각각 보여준다. MCTS 관점에서는 selection, expansion, simulation, backpropagation의 네 단계가 partial denoising tree 위에서 표현되며, 각 node는 partially denoised sub-trajectory에 대응된다. Diffusion 관점에서는 같은 과정이 denoising depth와 planning horizon 위에서 표현되며, 전체 row가 동시에 denoise되지만 subplan마다 서로 다른 denoising level을 갖는다.

![MCTD Search Tree Example](/assets/img/blog/paper-review-monte-carlo-tree-diffusion-system-2-planning/mctd-search-tree-example.png)

위 그림은 pointmaze-medium task에서 binary guidance set $\{\mathrm{NO\_GUIDE}, \mathrm{GUIDE}\}$를 사용한 MCTD tree-search 과정을 보여준다. 각 node는 partially denoised trajectory에 대응되며, 왼쪽 이미지는 noisy partial plan, 오른쪽 이미지는 fast denoising 이후의 plan을 나타낸다. Search는 $\mathrm{NO\_GUIDE}$ 또는 $\mathrm{GUIDE}$를 선택해 child node를 확장하고, 새로 생성된 plan을 평가하면서 최종적으로 reward가 높은 leaf로 수렴한다.


### 알고리즘

<img src="/assets/img/blog/paper-review-monte-carlo-tree-diffusion-system-2-planning/algorithm-1-mctd.png" alt="Algorithm 1. Monte Carlo Tree Diffusion" style="width: 50%; display: block; margin: 0 auto;">


## Experiments

### 실험 설정

실험은 Offline Goal-conditioned RL Benchmark(OGBench)를 기반으로 진행된다. 평가 task는 다음과 같다.

1. pointmaze navigation
2. antmaze navigation
3. multi-cube manipulation
4. visual pointmaze

### 비교 대상

이 논문에서는 다음 baseline들과 비교한다.

| Baseline | 설명 |
| --- | --- |
| Diffuser | 기본 diffusion-based planner이다. 전체 trajectory를 denoising으로 생성한다. |
| Diffuser Replanning | episode 중 fixed interval마다 다시 planning을 수행한다. 이를 통해 full tree search 없이 iterative replanning이 주는 이점을 확인한다. |
| Diffuser Random Search | 여러 trajectory를 병렬로 생성한 뒤, 동일한 reward function으로 score를 계산해 가장 높은 trajectory를 선택한다. |
| Diffusion Forcing | denoising schedule에 causal structure를 부여해 semi-autoregressive trajectory generation을 수행한다. |

### 실험 결과

![Long-Horizon Maze Results](/assets/img/blog/paper-review-monte-carlo-tree-diffusion-system-2-planning/long-horizon-maze-results.png)

![Planner Trajectory Comparison](/assets/img/blog/paper-review-monte-carlo-tree-diffusion-system-2-planning/planner-trajectory-comparison.png)

## Limitations & Discussion

MCTD는 inference-time computation을 더 많이 사용할수록 더 나은 plan을 찾을 수 있다는 점을 보인다. 그러나 이는 동시에 계산 비용이 여전히 크다는 의미이기도 하다. 따라서 모든 문제에서 항상 search를 강하게 사용하는 것보다, 쉬운 문제에서는 diffusion planner만 사용하고 어려운 문제에서만 search를 활성화하는 방식이 더 현실적일 수 있다.

search space가 커질수록 계산량이 증가하는 문제도 남아 있다. 이를 줄이기 위해 amortized search를 사용하는 방향이 의미 있을 것 같다. 매번 처음부터 random exploration을 수행하는 대신, 어떤 meta-action이나 trajectory branch가 유망했는지를 학습해 초기 탐색 방향을 더 잘 설정할 수 있다면 search 효율을 높일 수 있다.

sparse reward 환경에서는 trajectory의 좋고 나쁨을 판별하기 어렵다. 이 경우 self-supervised reward shaping을 사용해 충돌 위험, 목표와의 거리, 진행 방향 같은 중간 평가 신호를 만들면 더 안정적인 search가 가능할 수 있다.

추가적인 기술적 개선 방향은 다음과 같다.

1. Parallel denoising: 여러 denoising simulation을 병렬로 실행해 inference latency를 줄인다.
2. Differentiable tree search: search 과정을 미분 가능하게 만들어 diffusion model과 search policy를 함께 최적화한다.
3. Model-based rollout: 단순한 fast simulation 대신 learned dynamics model이나 world model을 사용해 future trajectory 평가를 개선한다.

## 나의 질문

1. MCTD는 subplan을 temporally extended state로 보고, 이를 MCTS의 node처럼 사용한다. 이 구조가 가능한 핵심 이유는 무엇인가? 단순히 DDIM 기반 jumpy denoising으로 future trajectory를 빠르게 샘플링하고 reward/value를 근사적으로 평가할 수 있기 때문인지, 아니면 subplan abstraction과 guidance schedule을 meta-action으로 정의한 점이 더 본질적인지 궁금하다.
2. MCTD는 low-level state가 아니라 subplan 단위로 tree를 구성하기 때문에 기존 MCTS보다 tree depth는 줄어든다. 하지만 search tree 안에 partial trajectory, value, visit count, guidance schedule 등을 저장해야 한다면 memory cost는 여전히 커질 수 있지 않은가?

## 내가 이해한 핵심

이 논문은 결국 diffusion의 denoising process에 MCTS를 적용한 방법으로 볼 수 있다. 여기서 subplan은 low-level action sequence를 직접 나누는 것이라기보다, diffusion denoising process 안에서 trajectory를 구간 단위로 나눈 것으로 이해할 수 있다.

diffusion은 inference 과정에서 Gaussian noise로부터 시작한 trajectory를 reverse denoising step을 통해 점점 더 실행 가능한 trajectory로 바꿔 간다. 기존 방식이 이 과정을 단순 sampling 또는 iterative refinement로 수행했다면, MCTD는 이 denoising 과정 위에 MCTS search를 얹는다. 즉, 후보 trajectory를 단순히 많이 뽑는 것이 아니라, 어떤 denoising branch를 더 탐색하고 어떤 branch를 덜 볼지를 tree search 방식으로 결정한다.

causal semi-autoregressive하다는 의미 역시 경로 자체를 일반적인 autoregressive generation으로 만든다는 뜻이 아니다. subplan별 noise level을 다르게 두어, denoising 과정에서 앞선 subplan이 먼저 구체화되고 뒤쪽 subplan이 그 결과에 조건화되는 구조를 만든다는 의미에 가깝다.

MCTS를 적용하기 위해 중요한 것은 simulation 단계와 exploration-exploitation 개념을 diffusion framework 안에 넣는 것이다. MCTD는 Guidance Levels as Meta-Actions 개념을 사용해, prior distribution을 따르는 선택과 goal-directed distribution을 따르는 선택을 구분한다. 이를 통해 denoising 과정 안에서 exploration과 exploitation을 조절한다.

simulation 단계에서는 설정해 둔 reward function으로 빠르게 trajectory를 평가하는 것이 중요하다. MCTD는 DDIM 기반 jumpy denoising을 사용해 full trajectory를 빠르게 생성하고, 이를 통해 선택된 subplan 이후의 future trajectory를 조기 평가할 수 있게 한다.

## 결론

이 논문은 diffusion planner에 MCTS를 결합하는 방법론을 제안한다. 이를 통해 기존 diffusion-based planning보다 long-horizon planning task에서 더 높은 성능을 보였다.

기존 연구에서는 단순히 denoising step 수를 늘리거나 sample 수를 늘리는 방식으로 계산량을 증가시켜도 성능 향상이 빠르게 plateau에 도달했다. 반면 MCTD는 증가한 inference-time computation을 tree search 형태로 활용함으로써, 더 많은 계산이 실제 planning 성능 향상으로 이어질 수 있음을 보여준다.
