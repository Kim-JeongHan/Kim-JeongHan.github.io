---
layout: post
title: '[논문리뷰] Monte Carlo Tree Diffusion for System 2 Planning'
date: 2026-06-27 00:22:22 +0900
slug: paper-review-monte-carlo-tree-diffusion-system-2-planning
render_with_liquid: true
use_math: true
categories:
- 공부
- 인공지능
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

그러나 diffusion planner가 planning 정확도를 효율적으로 향상시키는 방식은 아직 제한적이다.

| 접근 | 의도 | 한계 |
| --- | --- | --- |
| denoising step 수 증가 | 더 많은 refinement를 통해 trajectory quality를 높인다. | 초반에는 성능이 향상되지만, 일정 수준 이후에는 빠르게 plateau에 도달한다. |
| sample 수 증가 | 여러 trajectory 후보를 생성한 뒤 더 좋은 sample을 선택한다. | inference cost가 크게 증가하고, long-horizon task에서는 sample을 많이 뽑아도 여전히 실패할 수 있다. |
| diffusion inference만 사용 | 전체 trajectory를 한 번에 생성한다. | 어느 정도 새로운 trajectory를 탐색하고, 어느 정도 이미 좋아 보이는 trajectory를 개선할 것인지에 대한 exploration-exploitation tradeoff를 효율적으로 관리하기 어렵다. |

반대로 MCTS는 simulation을 반복적으로 활용하면서 exploratory feedback을 얻고, 이를 바탕으로 더 좋은 선택을 찾아갈 수 있다. 충분한 계산이 주어진다면 MCTS는 여러 System 2 reasoning task나 program synthesis에서 강력한 search 방법으로 사용할 수 있다.

그러나 전통적인 MCTS는 tree rollout을 수행하기 위해 forward model에 의존한다. 이 방식은 step-by-step rollout 과정에서 long-horizon trajectory의 global consistency를 잃기 쉽고, action space가 discrete하게 제한되는 경우가 많다. 또한 search tree가 깊고 넓어지기 때문에 중요한 계산 비용 문제를 만든다.

따라서 이 논문은 다음 질문에서 출발한다. diffusion-based planner의 trajectory-level generation 능력과 MCTS의 exploration-exploitation search 능력을 어떻게 결합할 수 있을까? 그리고 이를 통해 inference-time scalability를 어떻게 향상시킬 수 있을까?

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

### Overall Pipeline

-

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

Diffusion Forcing은 trajectory $\mathbf{x}$를 여러 token으로 나누어 다룰 수 있게 확장한다. 이러한 tokenization을 사용하면 각 token이 서로 다른 noise level에서 denoising될 수 있다. 따라서 uncertainty가 높은 상황에서 전체 trajectory를 full noise에서 no noise까지 한 번에 완성할 필요 없이, 필요한 segment만 부분적으로 denoise하면서 trajectory를 구성할 수 있다. 이러한 token-level control은 long-horizon planning처럼 causal consistency가 중요한 문제에서 특히 유용하다.

### Monte Carlo Tree Diffusion

#### Denoising as Tree-Rollout

전통적인 MCTS는 개별 state를 node로 두고 search tree를 확장한다. 각 node가 단일 state를 표현하기 때문에 tree의 깊이는 planning horizon에 따라 선형적으로 증가하고, 가능한 action이 누적되면서 search space는 지수적으로 커진다. 이 때문에 long-horizon planning에서는 깊은 탐색과 확장성 문제가 크게 나타난다.

또한 전통적인 MCTS는 step-by-step rollout을 수행하기 때문에 diffusion-based planner처럼 전체 trajectory를 하나의 단위로 바라보는 trajectory-level 관점을 갖기 어렵다. MCTD는 이 문제를 해결하기 위해 denoising process 자체를 tree rollout으로 해석한다.

반면 Diffuser는 전체 trajectory를 생성할 수 있지만, 중간 decision point에서 탐색을 수행하기 위한 tree structure를 제공하지 않는다. 따라서 이미 좋아 보이는 선택을 더 깊게 확인하는 exploitation과, 충분히 보지 않은 새로운 선택지를 탐색하는 exploration 사이의 균형을 효과적으로 맞추기 어렵다.

이 문제를 다루기 위해 MCTD는 먼저 denoising을 semi-autoregressive denoising process로 활용한 tree rollout으로 재정의한다. 전체 trajectory를 다음과 같이 $S$개의 서로 겹치지 않는 subplan으로 나눈다.

$$
\mathbf{x}
=
(\mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_S),
\qquad
\mathbf{x}_i \cap \mathbf{x}_j = \emptyset
\quad
(i \ne j)
$$

모든 subplan이 같은 global denoising schedule을 공유하는 standard Diffuser와 달리, MCTD는 각 subplan에 독립적인 denoising schedule을 할당한다. 초기 subplan에는 더 빠른 denoising을 적용하고, 후반 subplan에는 더 느린 denoising을 적용함으로써 전체 process를 더 효율적인 semi-autoregressive 형태로 만든다.

이렇게 하면 denoising process는 이미 결정된 과거 subplan에 조건화된 상태에서 미래 subplan을 결정하게 된다. 즉, 전체 trajectory를 한 번에 완성하는 것이 아니라, 앞부분을 먼저 상대적으로 확정하고 그 결과를 바탕으로 뒤쪽 trajectory를 점진적으로 refine하는 방식이다.

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

따라서 전체 plan $\mathbf{x}$의 denoising은 diffuser의 single denoising process 안에서 이러한 subplan node들의 순서를 rollout하는 과정으로 볼 수 있다.

### System 2 Planning

-

## Experiments

### 실험 설정

-

### 비교 대상

-

### 실험 결과

-

## 한계 및 아쉬운 점

1.
2.

## 내가 이해한 핵심

-
