---
layout: post
title: '[논문리뷰] State-Covering Trajectory Stitching for Diffusion Planners'
date: 2026-07-06 00:00:00 +0900
slug: paper-review-state-covering-trajectory-stitching-diffusion-planners
render_with_liquid: true
use_math: true
categories:
- 논문리뷰
- diffusion
tags:
- ai
- planning
- diffusion-model
- offline-rl
- trajectory-stitching
- paper-review
---

## 논문 정보

## 한 줄 요약

## 문제 정의

### 기존 방식의 한계

Model-based reinforcement learning은 dynamics model을 학습해 planning을 수행하기 때문에, 기존에 보지 못한 상황에 대한 generalization을 어느 정도 향상시킬 수 있다. 그러나 autoregressive하게 미래 state를 예측하는 과정에서는 prediction error가 누적될 수 있다. 이 오차가 커지면 물리적으로 불가능한 trajectory가 만들어지거나, 생성된 trajectory가 suboptimal해질 수 있다.

반면 diffusion planner는 trajectory를 한번에 생성한다. 전체 trajectory를 한 번에 만들기 때문에 autoregressive prediction error가 step마다 누적되는 문제를 줄일 수 있다. 또한 conditioning이나 guidance를 추가하여 goal이나 expected return이 더 큰 방향으로 trajectory generation을 유도할 수도 있다.

하지만 diffusion planner도 다음과 같은 한계를 가진다.

1. Effective planning horizon은 학습된 최대 trajectory length 안에서 coherent plan을 만들 수 있는지에 의해 제한된다. Long-horizon task에서는 여러 trajectory segment가 일관되게 연결되어야 하는데, 이를 안정적으로 만드는 것은 어렵다.
2. Generalization capability는 training data 안에 포함된 trajectory의 종류나 transition coverage에 의해 제한된다. 예를 들어 dataset이 특정 behavior pattern에 치우쳐 있다면, planner는 새로운 task에 필요한 transition을 조합하거나 연결하는 데 어려움을 겪을 수 있다. 이 한계는 논문에서 제시한 예시 그림에서도 확인할 수 있다.

<img src="/assets/img/blog/paper-review-state-covering-trajectory-stitching-diffusion-planners/state-coverage-comparison.png" alt="State Coverage Comparison" style="width: 50%; display: block; margin: 0 auto;">

위 그림은 SCoTS를 사용했을 때 generalization이 어떻게 개선되는지를 보여준다. (a)는 training dataset의 예시로, offline data의 coverage가 제한적임을 보여준다. (b)는 Hierarchical Diffuser(HD)가 생성한 plan으로, training data의 coverage가 부족하기 때문에 out-of-distribution task에 잘 일반화하지 못한다. (c)는 SCoTS-augmented data로 학습한 HD의 plan이며, unseen task에 대해 trajectory stitching capability와 generalization이 크게 개선된 것을 보여준다. 각 색상은 planner가 생성한 10개의 plan 중 하나를 의미한다.

가장 단순한 해결책은 다양한 task와 state를 포함하는 데이터를 극단적으로 많이 모으는 것이다. 그러나 실제 환경에서 이런 방식은 너무 비싸고, 필요한 모든 transition을 직접 수집하는 것도 현실적이지 않다.

그래서 이미 존재하는 짧은 trajectory segment들을 이어 붙여 더 긴 sequence를 만드는 stitching 접근이 제안되어 왔다. 하지만 기존 stitching 방식은 어떤 segment를 선택하고 연결할지 결정할 때 extrinsic reward에 강하게 의존하는 경우가 많다. 이 경우 reward가 명확하지 않거나 sparse한 환경에서는 좋은 stitching을 만들기 어렵고, 결국 diffusion planner의 generalization을 충분히 확장하는 데 한계가 남는다.

## 핵심 아이디어

이 논문은 reward-free trajectory augmentation framework를 제안한다. 다른 연구들이 diffusion planner의 architecture나 sampling 과정을 직접 개선하는 데 집중했다면, 이 논문은 augmented dataset $\mathcal{D}_{\mathrm{aug}}$ 자체에 집중한다. 핵심 목표는 latent directional exploration으로 짧은 trajectory segment들을 이어 붙여 다양하고 긴 trajectory를 만들고, 이를 통해 diffusion planner가 training distribution의 한계를 넘어서도록 만드는 것이다.

## Method

SCoTS의 전략은 크게 세 단계로 정리할 수 있다.

1. Temporal distance-preserving embedding을 학습해 trajectory segment를 효율적으로 retrieve한다.
2. Latent directional exploration과 novelty-based selection을 사용해 iterative trajectory stitching을 수행한다.
3. Diffusion-based refinement를 통해 stitched trajectory의 transition이 dynamics consistency를 유지하도록 정제한다.

### Temporal Distance-Preserving Representation

Trajectory segment들을 식별하고 분류하기 위해서는 state 사이의 temporal closeness를 정확하게 측정할 수 있어야 한다. 단순히 raw state-space distance를 사용하면 두 state가 공간적으로 가까워 보이더라도 실제 dynamics 관점에서는 서로 도달하기 어려운 경우를 구분하지 못할 수 있다. 즉 state reachability를 무시하면 potential dynamics inconsistency가 발생하고, 결과적으로 incoherent한 stitching으로 이어질 수 있다.

이를 해결하기 위해 temporal distance-preserving embedding을 학습한다. 이 embedding은 raw state를 latent space $\mathcal{Z}$로 mapping한다.

$$
\phi : \mathcal{S} \to \mathcal{Z}
$$

이후 latent space에서 state $s$와 goal $g$ 사이의 거리를 사용해 goal-conditioned value를 다음과 같이 정의한다.

$$
V(s,g)
:=
-\left\|
\phi(s)-\phi(g)
\right\|_2
$$

이 goal-conditioned value function을 학습하기 위해 offline dataset $\mathcal{D}$를 사용한다. 학습 objective는 Implicit Q-Learning에서 영감을 받은 temporal difference objective로 정의된다.

$$
\mathcal{L}_{\phi}
:=
\mathbb{E}_{(s,a,s',g)\sim\mathcal{D}}
\left[
\ell_{\xi}^{2}
\!\left(
- \mathbb{1}(s \neq g)
-
\gamma
\left\|
\bar{\phi}(s')
-
\bar{\phi}(g)
\right\|_{2}
+
\left\|
\phi(s)
-
\phi(g)
\right\|_{2}
\right)
\right]
$$

여기서 $\bar{\phi}$는 target network이고, $\gamma$는 discount factor이며, $\ell_{\xi}^{2}$는 expectile loss를 의미한다.

Temporal distance-preserving embedding을 학습하기 위해서는 non-parametric particle-based estimator를 사용한다. 이 estimator는 state 사이의 temporal distance signal을 구성하고, 이를 통해 latent embedding이 단순한 raw state similarity가 아니라 reachability를 반영하도록 만든다.

즉 $\phi$는 state를 단순한 geometric similarity가 아니라 learned optimal temporal distance를 기준으로 encode하는 방식이다. 이렇게 학습된 latent space에서는 서로 이어 붙일 수 있는 trajectory segment를 더 효율적으로 찾을 수 있다.

{% capture raw_state_distance_callout %}
raw states의 Euclidean distance를 그대로 쓰면, 벽을 사이에 둔 $s$와 $g$처럼 공간적으로는 가까워도 실제로 바로 이동하기 어려운 경우를 구분하지 못한다.

SCoTS는 이를 반영하기 위해 latent space $\mathcal{Z}$에서의 Euclidean distance가 optimal temporal distance $d^*(s,g)$를 근사하도록 embedding을 학습한다.

$$
d^*(s,g)
\approx
\left\|
\phi(s)-\phi(g)
\right\|_2
$$
{% endcapture %}

{% include callout.html type="note" title="왜 raw state distance를 쓰지 않는가" content=raw_state_distance_callout %}

{% capture latent_metric_callout %}
학습된 latent space가 MDP의 정확한 metric representation일 필요는 없다. SCoTS는 temporal distance metric이 globally 정확하다고 가정하지 않도록 설계되어 있다.

대신 이 metric은 전체 경로를 한 번에 계획하기 위한 전역 planning metric으로 쓰이는 것이 아니라, iterative stitching의 각 단계에서 경로 품질이 좋고 실제로 도달 가능한 candidate segment를 찾기 위해 사용된다.
{% endcapture %}

{% include callout.html type="note" title="Latent metric의 역할" content=latent_metric_callout %}

### Directional and Exploratory Trajectory Stitching

이후 기존 dataset에 있는 짧은 trajectory segment들을 반복적으로 연결해 더 길고 다양한 trajectory를 만든다. 먼저 offline dataset $\mathcal{D}$로부터 initial segment $\tau_{\mathrm{init}}$를 선택하고, 이를 현재 composed trajectory $\tau_{\mathrm{comp}}$로 둔다.

Diverse state coverage를 만들기 위해 fixed latent-space direction인 unit vector $\mathbf{z}$를 sample한다.

$$
\mathbf{z} \sim \mathcal{N}(0,I),
\qquad
\mathbf{z}
\leftarrow
\frac{\mathbf{z}}{\|\mathbf{z}\|}
$$

여기서 $\tau_{\mathrm{comp}}$는 현재까지 composed된 trajectory를 의미하고, $\operatorname{end}(\tau)$는 trajectory $\tau$의 final state를 반환하는 함수이다. Candidate segment 집합 $\{\tau_j\}_{j=1}^{k}$는 latent space에서 $\operatorname{end}(\tau_{\mathrm{comp}})$와 initial state가 가장 가까운 $k$개의 segment로 정의된다.

$$
\{\tau_j\}_{j=1}^{k}
=
\operatorname{TopKNeighbors}
\!\left(
\phi(\operatorname{end}(\tau_{\mathrm{comp}})),
\,
\phi(\mathcal{D}),
\,
k
\right)
$$

여기서 $\phi(\mathcal{D})$는 dataset 안의 모든 trajectory segment의 initial state를 latent embedding한 집합을 간단히 표현한 것이다. 즉 candidate $\tau_j$의 initial state를 $s_{1,j}$라고 하면, neighbor retrieval에서 사용하는 distance metric은 다음과 같다.

$$
\left\|
\phi(\operatorname{end}(\tau_{\mathrm{comp}}))
-
\phi(s_{1,j})
\right\|_2
$$

Stitching에 사용할 가장 좋은 candidate를 선택하기 위해, 각 candidate segment를 다시 평가한다. Candidate segment $\tau_j$는 다음과 같이 길이 $H$의 state sequence로 둔다.

$$
\tau_j
=
(s_{1,j}, \ldots, s_{H,j})
$$

이때 SCoTS는 directional progress와 novelty를 함께 고려하는 composite score를 사용한다. 즉 latent direction $\mathbf{z}$를 따라 trajectory가 얼마나 잘 진행되는지와, 기존에 충분히 방문하지 않은 state region을 얼마나 잘 cover하는지를 동시에 평가한다.

Progress score는 candidate segment의 진행 방향이 latent space 안에서 exploration direction $\mathbf{z}$와 얼마나 잘 align되어 있는지를 측정한다. 즉 선택된 segment가 현재 composed trajectory를 미리 정한 latent direction으로 얼마나 잘 확장하는지를 평가한다.

$$
P_j
=
\left\langle
\phi(\operatorname{end}(\tau_j))
-
\phi(s_{1,j}),
\,
\mathbf{z}
\right\rangle
$$

여기서 $\mathcal{V}_{\mathrm{rollout}}$은 이전에 stitched된 segment들을 따라 등장한 모든 state의 latent representation을 모아둔 집합을 의미한다.

Novelty score는 exploration을 유도하고 새로운 latent state의 coverage를 증가시키기 위한 점수이다. 이는 이전에 latent space에서 방문한 state들과 비교했을 때, 각 candidate segment의 endpoint가 얼마나 새로운 영역에 위치하는지를 entropy 관점에서 추정하는 방식으로 계산된다.

$$
N_j
=
\frac{1}{k_{\mathrm{density}}}
\sum_{\phi_v \in
\operatorname{k\text{-}NN}
\left(
\phi(\operatorname{end}(\tau_j)),
\mathcal{V}_{\mathrm{rollout}},
k_{\mathrm{density}}
\right)}
\left\|
\phi(\operatorname{end}(\tau_j))
-
\phi_v
\right\|_2
$$

높은 $N_j$는 novelty가 높다는 의미이다. 즉 해당 candidate segment가 latent space 안에서 아직 덜 탐색된 영역으로 이동하며 state coverage를 확장하는 신호로 볼 수 있다. SCoTS는 progress score $P_j$와 novelty score $N_j$를 결합해 전체 selection criterion을 만든다.

$$
S_j
=
P_j
+
\beta N_j
$$

여기서 $\beta$는 progress와 novelty의 balance를 조절하는 parameter이다. 이후 가장 높은 score를 갖는 candidate $\tau_{\mathrm{best}}$를 선택해 현재 trajectory $\tau_{\mathrm{comp}}$에 이어 붙인다.

Stitching 과정에서는 state space의 새로운 영역을 exploration하는 것과, 이미 유망한 trajectory를 확장하는 것 사이의 균형이 중요하다. 이를 위해 SCoTS는 latent directional exploration과 novelty-based selection을 함께 사용한다. 그 결과 이전에 exploration된 region들이 새로운 방식으로 연결되고, 특정 reward signal이나 기존 behavior pattern에만 치우치지 않는 trajectory coverage를 만들 수 있다.

### Diffusion-Based Refinement

앞의 과정에서 좋은 stitching candidate segment를 찾았더라도, 이를 현재 trajectory에 어떻게 자연스럽게 연결할지는 별도의 문제이다. 단순히 $\tau_{\mathrm{comp}}$ 뒤에 $\tau_{\mathrm{best}}$를 붙이면 segment 사이의 transition이 부자연스럽거나 dynamics consistency가 약할 수 있다.

이를 다루기 위해 SCoTS는 diffusion-based refinement step을 추가한다. 구체적으로 stitcher model $p_{\theta}^{\mathrm{stitcher}}$를 사용해 selected segment $\tau_{\mathrm{best}}$를 고려한 refined trajectory $\tau'$를 생성한다.

$$
\tau'
\sim
p_{\theta}^{\mathrm{stitcher}}
\!\left(
\,\cdot\,
\mid
s_1=\operatorname{end}(\tau_{\mathrm{comp}}),
\,
s_H=\operatorname{end}(\tau_{\mathrm{best}})
\right)
$$

즉 stitcher는 현재 composed trajectory의 endpoint와 selected segment의 endpoint를 조건으로 받아, 두 segment를 dynamics feasibility를 유지하는 trajectory로 연결하도록 정제한다.

### Diffusion Planner Training

최종적으로 refinement된 state-action trajectory들은 augmented dataset $\mathcal{D}_{\mathrm{aug}}$에 aggregate된다. 이러한 체계적이고 반복적인 augmentation 방식은 state space를 더 넓게 포함하는 augmented dataset을 생성한다.

Diffusion planner는 이 augmented dataset을 통해 더 넓은 state-space coverage와 더 긴 horizon의 trajectory pattern을 학습할 수 있다.

## Experiments

실험에서는 SCoTS가 단순히 trajectory를 더 많이 만드는 것을 넘어, 실제 planning과 offline GCRL 성능 향상에 도움이 되는지를 확인한다.

| 질문 | 확인하고 싶은 점 |
| --- | --- |
| SCoTS가 기존 dataset을 넘어 다양한 trajectory를 생성해 dataset을 확장하는가 | augmented dataset이 더 넓은 state-space coverage를 갖는지 확인한다. |
| Augmented trajectory가 unseen scenario의 long-horizon 문제 해결에 도움이 되는가 | diffusion planner가 training distribution 밖의 task에서도 coherent trajectory를 만들 수 있는지 확인한다. |
| Augmented dataset이 GCRL algorithm의 성능 향상에 기여하는가 | SCoTS가 특정 diffusion planner에만 유효한 것이 아니라, goal-conditioned RL에도 도움이 되는지 확인한다. |

### Datasets and Environments

실험은 OGBench benchmark의 locomotion task를 사용한다. 주요 환경은 PointMaze와 AntMaze이며, 각 환경에서 Stitch dataset과 Explore dataset을 사용해 서로 다른 일반화 문제를 평가한다.

| Dataset | 구성 | 평가하는 능력 |
| --- | --- | --- |
| Stitch dataset | 최대 4 cell unit 길이의 짧은 goal-reaching trajectory들로 구성된다. | 성공적인 inference를 위해 여러 segment를 이어 붙이는 능력을 평가한다. 일부 task에서는 최대 8개의 segment를 stitching해야 한다. |
| Explore dataset | random direction을 자주 resampling하고 큰 action noise를 주입해 수집한 길지만 품질이 낮은 exploratory trajectory들로 구성된다. | noisy하고 suboptimal한 trajectory로부터 navigation behavior를 학습할 수 있는지 평가한다. |

### Diversity and State Coverage

SCoTS가 trajectory stitching을 통해 다양한 state-space coverage를 만드는지 확인하기 위해 PointMaze-Giant-Stitch 환경에서 평가한다. 논문에서는 novelty weighting parameter $\beta \in \{0,2,20\}$에 따라 stitching 과정이 어떻게 달라지는지 시각화한다.

<img src="/assets/img/blog/paper-review-state-covering-trajectory-stitching-diffusion-planners/novelty-weight-coverage.png" alt="Novelty Weight Coverage" style="width: 50%; display: block; margin: 0 auto;">

$\beta=0$일 때는 latent directional guidance를 주로 따라가기 때문에 trajectory 방향은 뚜렷하지만 coverage가 제한된다. $\beta=2$에서는 directional progress와 novelty 사이의 균형이 가장 잘 맞아, 충분한 state-space coverage와 trajectory diversity를 함께 얻는다. 반대로 $\beta=20$처럼 novelty weight가 너무 크면 state space는 넓게 cover하지만, 서로 다른 latent exploration direction의 trajectory들이 겹치면서 구분성이 약해진다.

따라서 논문에서는 모든 환경에서 $\beta=2$를 사용한다.

### Long-Horizon Planning

SCoTS-augmented data로 학습한 diffusion planner가 long-horizon planning을 더 잘 수행하는지도 확인한다. 아래 그림은 SCoTS-augmented data로 학습한 diffusion planner가 생성한 trajectory를 AntMaze의 두 가지 어려운 dataset에서 시각화한 것이다.

![OGBench Long-Horizon Results](/assets/img/blog/paper-review-state-covering-trajectory-stitching-diffusion-planners/ogbench-long-horizon-results.png)

위쪽의 Explore dataset은 random direction resampling과 큰 action noise로 수집된 low-quality trajectory로 구성된다. 따라서 원본 data는 길게 이어진 navigation behavior를 안정적으로 보여주기 어렵다. 아래쪽의 Stitch dataset은 trajectory segment 하나가 최대 4 maze cell로 제한되어 있기 때문에, long-horizon task를 풀려면 여러 short segment를 이어 붙이는 능력이 필요하다.

즉 Explore는 data quality가 낮다는 점이 어렵고, Stitch는 segment horizon이 짧아 extensive stitching이 필요하다는 점이 어렵다. 그럼에도 SCoTS augmentation을 사용하면 planner가 원본 data의 horizon과 quality를 넘어, 지정된 start와 goal을 연결하는 trajectory를 생성할 수 있다.

### Offline GCRL with SCoTS-Augmented Dataset

SCoTS로 만든 augmented dataset이 diffusion planner에만 유효한 것이 아니라, offline goal-conditioned RL algorithm에도 도움이 되는지 확인한다.

<img src="/assets/img/blog/paper-review-state-covering-trajectory-stitching-diffusion-planners/gcrl-performance-enhancement.png" alt="GCRL Performance Enhancement" style="width: 50%; display: block; margin: 0 auto;">

위 표는 GCIQL, CRL, HIQL에 original dataset, SynthER-augmented dataset, SCoTS-augmented dataset을 적용했을 때의 성능을 비교한다. 평균 성능을 보면 SCoTS-augmented dataset을 사용한 경우가 가장 높으며, 특히 CRL과 HIQL에서 성능 향상이 크게 나타난다. 이는 SCoTS가 diffusion planner 전용 기법이 아니라, goal-conditioned learning에서도 더 나은 training distribution을 제공할 수 있음을 보여준다.

### Effectiveness of Diffusion-Based Stitching Refinement

마지막으로 diffusion-based refinement가 stitched trajectory의 dynamics consistency를 실제로 개선하는지 확인한다. 이를 위해 논문은 Dynamic Mean Squared Error(Dynamic MSE)를 사용한다. 여기서 $f^*$는 실제 환경의 ground-truth dynamics를 의미한다.

<img src="/assets/img/blog/paper-review-state-covering-trajectory-stitching-diffusion-planners/diffusion-refinement-dynamic-mse.png" alt="Diffusion Refinement Dynamic MSE" style="width: 50%; display: block; margin: 0 auto;">

그림에서 refinement를 사용하지 않은 경우에는 Dynamic MSE가 큰 영역에 많이 분포한다. 반면 refinement를 적용하면 Dynamic MSE가 훨씬 낮은 영역으로 이동한다. 이는 diffusion-based stitcher가 단순히 segment를 이어 붙이는 것이 아니라, transition이 실제 dynamics와 더 잘 맞도록 trajectory를 정제한다는 것을 보여준다.

## Discussion

## 한계 및 아쉬운 점

1. Computational overhead가 존재한다. Diffusion-based stitcher model을 추가로 학습해야 하고, trajectory augmentation process 자체도 반복적으로 수행되기 때문에 refinement를 많이 사용할수록 계산 비용이 커질 수 있다.
2. Temporal distance-preserving embedding은 asymmetric temporal distance를 명확히 구별하지 못할 수 있다. 따라서 irreversible action이 포함된 object manipulation task나, sparse connectivity를 가진 isolated region이 존재하는 환경처럼 highly asymmetric하거나 disconnected된 MDP에서는 효과가 제한될 수 있다.

## 내가 이해한 핵심

## Reference
