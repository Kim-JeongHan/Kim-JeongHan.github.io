---
layout: post
title: 'Collision Detection 기초: Broad Phase와 Narrow Phase'
date: 2025-03-16 00:43:33 +0900
slug: collision-detection-narrow-broad-phase
render_with_liquid: false
use_math: true
categories:
- 알고리즘
tags:
- collision-detection
- broad-phase
- narrow-phase
- separating-axis-theorem
- gjk
- gjk-epa
last_modified_at: 2026-06-15 17:00:00 +0900
imported_images:
- assets/img/blog/collision-detection-narrow-broad-phase/image-001.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-002.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-003.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-004.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-005.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-006.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-007.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-008.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-009.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-010.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-011.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-012.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-013.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-014.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-015.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-016.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-017.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-018.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-019.png
- assets/img/blog/collision-detection-narrow-broad-phase/image-020.png
source:
  provider: confluence
  id: '961118352'
  url: https://roboe.atlassian.net/wiki/spaces/ROBOENET/pages/961118352/Collision+Detection
---

Collision detection은 일반적으로 broad phase와 narrow phase 두 단계로 나누어 수행한다.

Broad phase에서는 전체 객체 중 정밀하게 검사할 필요가 있는 후보 쌍만 빠르게 걸러낸다. Narrow phase에서는 broad phase를 통과한 후보 쌍에 대해 실제 충돌 여부, 최소 거리, 침투 깊이 등을 더 정밀하게 계산한다.

## Broad Phase

Broad phase의 목적은 충돌 가능성이 없는 객체 쌍을 빠르게 제거하는 것이다.

모든 객체 쌍을 brute-force로 검사하면 객체 수가 $n$일 때 복잡도는 다음과 같다.

$$
O(n^2)
$$

객체 수가 많아지면 이 방식은 바로 부담이 커진다. 그래서 broad phase에서는 단순한 bounding volume이나 공간 분할 구조를 이용해 후보를 줄인다.

### Axis-Aligned Bounding Box

Axis-aligned bounding box(AABB)는 객체를 축에 정렬된 직사각형 또는 직육면체로 감싸는 방식이다.

계산이 빠르지만, 객체가 회전하면 실제 객체에 비해 빈 공간이 많이 포함될 수 있다.

![axis-aligned bounding box](/assets/img/blog/collision-detection-narrow-broad-phase/image-001.png)

### Oriented Bounding Box

Oriented bounding box(OBB)는 객체의 실제 방향에 맞춰 bounding box를 설정한다.

AABB보다 더 정확하게 객체를 감쌀 수 있지만, 축이 고정되어 있지 않기 때문에 연산은 더 복잡해진다.

![oriented bounding box](/assets/img/blog/collision-detection-narrow-broad-phase/image-002.png)

### Bounding Volume Hierarchy

Bounding volume hierarchy(BVH)는 객체의 세부 기하 정보를 트리 형태로 구성하는 방식이다. 상위 레벨에서는 단순한 bounding volume으로 후보를 걸러내고, 하위 레벨로 내려가면서 점점 정밀하게 검사한다.

FCL(Flexible Collision Library) 같은 충돌 검사 라이브러리에서도 BVH 구조가 널리 사용된다.

![bounding volume hierarchy](/assets/img/blog/collision-detection-narrow-broad-phase/image-003.png)

상위 레벨부터 하위 레벨까지 내려가며 충돌 검사를 진행한다.

![hierarchical collision check](/assets/img/blog/collision-detection-narrow-broad-phase/image-004.png)

잘못 묶인 예시는 bounding volume이 실제 충돌 후보를 효율적으로 줄이지 못한다.

![poor bounding volume grouping](/assets/img/blog/collision-detection-narrow-broad-phase/image-005.png)

반대로 잘 묶인 BVH는 상위 레벨에서 불필요한 후보를 빠르게 제거한다.

![good bounding volume grouping](/assets/img/blog/collision-detection-narrow-broad-phase/image-006.png)

### Sort and Sweep

Sort and sweep은 각 객체의 bounding volume을 $x$, $y$, $z$축 중 하나의 축에 투영해서 1차원 구간으로 만든다.

두 객체의 투영 구간이 겹치지 않으면, 해당 축에서 두 객체는 충돌할 수 없다.

![sort and sweep](/assets/img/blog/collision-detection-narrow-broad-phase/image-007.png)

### Spatial Subdivision

Spatial subdivision은 공간을 균일한 grid로 분할하는 방식이다. Grid cell의 크기는 보통 가장 큰 객체의 bounding volume보다 크거나 같게 잡는다.

이렇게 공간을 나누면 같은 cell에 있거나 인접한 cell에 있는 객체끼리만 충돌 검사를 수행하고, 나머지 조합은 무시할 수 있다.

![spatial subdivision grid](/assets/img/blog/collision-detection-narrow-broad-phase/image-008.png)

객체 하나는 여러 cell과 겹칠 수 있다.

![object overlapping grid cells](/assets/img/blog/collision-detection-narrow-broad-phase/image-009.png)

예를 들어 다음과 같이 후보를 줄일 수 있다.

- $o_1$, $o_2$: 충돌 검사
- $o_2$, $o_3$: 충돌 검사
- $o_1$, $o_3$: 같은 기준 cell 후보가 아니므로 충돌 검사 제외

## Narrow Phase

Broad phase를 거친 뒤 남은 객체들은 충돌 가능성이 있는 후보들이다. Narrow phase에서는 이 후보들이 실제로 충돌하는지 정밀하게 판단한다.

## Separating Axis Theorem

Separating axis theorem(SAT)은 두 convex 객체의 충돌 여부를 판단하는 방법이다.

두 convex 객체가 서로 충돌하지 않는다면, 두 객체의 projection이 겹치지 않는 축이 적어도 하나 존재한다. 반대로 모든 후보 축에 대해 projection이 겹친다면 두 객체는 충돌한다.

![separating axis theorem](/assets/img/blog/collision-detection-narrow-broad-phase/image-010.png)

두 볼록 집합 $A$, $B$에 대해 임의의 방향 벡터 $\mathbf{d}$로 projection을 잡으면 다음과 같다.

$$
\begin{aligned}
\operatorname{Projection}_A(\mathbf{d})
&=
\left[
\min_{\mathbf{a}\in A}(\mathbf{a}\cdot\mathbf{d}),
\max_{\mathbf{a}\in A}(\mathbf{a}\cdot\mathbf{d})
\right] \\
\operatorname{Projection}_B(\mathbf{d})
&=
\left[
\min_{\mathbf{b}\in B}(\mathbf{b}\cdot\mathbf{d}),
\max_{\mathbf{b}\in B}(\mathbf{b}\cdot\mathbf{d})
\right]
\end{aligned}
$$

두 interval이 겹치지 않는다면 $\mathbf{d}$는 separating axis다.

$$
\max_A < \min_B
\qquad \text{or} \qquad
\max_B < \min_A
$$

이런 축이 하나라도 발견되면 두 객체는 충돌하지 않는다.

## GJK

GJK(Gilbert-Johnson-Keerthi)는 convex 객체 간의 충돌 여부를 판단하거나, 두 객체 사이의 최소 거리를 계산하기 위해 사용되는 알고리즘이다.

![gjk collision detection](/assets/img/blog/collision-detection-narrow-broad-phase/image-011.png)

GJK는 convex 객체를 대상으로 하므로, convex하지 않은 객체는 그대로 사용할 수 없다. 일반적으로 convex decomposition을 하거나, convex hull 또는 bounding volume을 이용해 근사한다.

## Minkowski Sum and Difference

Minkowski sum 또는 difference는 두 객체의 모든 점 조합을 더하거나 빼서 새로운 집합을 만드는 연산이다.

![minkowski operation 1](/assets/img/blog/collision-detection-narrow-broad-phase/image-012.png)

![minkowski operation 2](/assets/img/blog/collision-detection-narrow-broad-phase/image-013.png)

Collision detection에서는 주로 Minkowski difference를 이용한다.

- 충돌한 경우: Minkowski difference로 만들어진 객체가 원점을 포함한다.
- 충돌하지 않은 경우: Minkowski difference의 simplex와 원점 사이의 최단거리를 근사해서 두 객체 사이의 최소 거리를 계산할 수 있다.

![gjk simplex search](/assets/img/blog/collision-detection-narrow-broad-phase/image-014.png)

GJK의 simplex 탐색 흐름은 다음과 같이 볼 수 있다.

1. 임의의 vertex $A$를 초기 simplex로 선택한다. $Q=\{A\}$.
2. $-A$ 방향의 support point를 찾아 $B$를 simplex에 추가한다. $Q=\{A,B\}$.
3. Convex hull $Q$에서 원점에 가장 가까운 점 $C$를 찾는다. $C$를 표현하는 데 $A$, $B$가 모두 필요하므로 둘 다 유지한다.
4. $-C$ 방향의 support point $D$를 찾아 $Q=\{A,B,D\}$로 만든다.
5. Convex hull $Q$에서 원점에 가장 가까운 점 $E$를 찾는다.
6. $E$를 표현하는 데 $B$, $D$만 필요하면 $Q=\{B,D\}$로 갱신한다. 이후 $-E$ 방향의 support point $F$를 추가한다.
7. Convex hull $Q$에서 원점에 가장 가까운 점 $G$를 찾는다.
8. $G$를 표현하는 데 필요한 최소 vertex가 $D$, $F$라면 $Q=\{D,F\}$로 갱신한다.
9. $-G$ 방향에서 $G$보다 원점에 더 가까운 vertex를 찾을 수 없다면 $G$가 원점에 가장 가까운 점이고, 충돌은 발생하지 않은 것으로 판단한다.

## GJK-EPA

GJK는 충돌 여부를 판정할 수 있지만, 얼마나 깊게 충돌했는지는 직접 알려주지 않는다. 이때 EPA(expanding polytope algorithm)를 함께 사용한다.

EPA는 GJK가 만든 simplex를 확장해서 penetration depth와 contact normal을 추정한다.

### EPA 동작 원리

1. GJK에서 사용한 simplex를 polytope로 지정한다.
2. 원점과 polytope edge 사이의 거리가 가장 가까운 edge를 고른다.
3. 원점에서 가장 가까운 edge 방향을 이용해 support point를 구한다.
4. Support point를 edge의 두 점 사이에 삽입해 polytope를 확장한다.
5. Support point가 더 이상 polytope를 의미 있게 확장하지 못하면 중단한다.
6. 최종 polytope에서 원점과 가장 가까운 edge까지의 거리가 penetration depth가 되고, 원점에서 edge 쪽 방향이 contact normal이 된다.

<div class="table-responsive tistory-table">
<table>
<tbody>
<tr>
<th>Step</th>
<th>Polytope</th>
<th>Closest edge</th>
</tr>
<tr>
<td>1</td>
<td><img src="/assets/img/blog/collision-detection-narrow-broad-phase/image-015.png" alt="epa polytope step 1"></td>
<td><img src="/assets/img/blog/collision-detection-narrow-broad-phase/image-016.png" alt="epa closest edge step 1"></td>
</tr>
<tr>
<td>2</td>
<td><img src="/assets/img/blog/collision-detection-narrow-broad-phase/image-017.png" alt="epa polytope step 2"></td>
<td><img src="/assets/img/blog/collision-detection-narrow-broad-phase/image-018.png" alt="epa closest edge step 2"></td>
</tr>
<tr>
<td>3</td>
<td><img src="/assets/img/blog/collision-detection-narrow-broad-phase/image-019.png" alt="epa polytope step 3"></td>
<td><img src="/assets/img/blog/collision-detection-narrow-broad-phase/image-020.png" alt="epa closest edge step 3"></td>
</tr>
</tbody>
</table>
</div>

## Reference

- <https://m.blog.naver.com/jerrypoiu/221172549241>
- <https://mathmakeworld.tistory.com/109#google_vignette>
- <https://developer.nvidia.com/gpugems/gpugems3/part-v-physics-simulation/chapter-32-broad-phase-collision-detection-cuda>
- <https://blog.smilecat.dev/posts/graphics-separating-axis-theorem>
- <https://www.slideshare.net/slideshow/collision-detection-algorithms/251207941>
- <https://www.haroldserrano.com/blog/visualizing-the-gjk-collision-algorithm>
