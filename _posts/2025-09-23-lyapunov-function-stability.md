---
layout: post
title: 'Lyapunov Function: Stability을 증명하는 에너지 함수'
date: 2025-09-23 17:21:54 +0900
slug: lyapunov-function-stability
render_with_liquid: false
categories:
- 공부
- mpc
tags:
- mpc
- lyapunov
- stability
last_modified_at: 2025-09-23 20:24:53 +0900
imported_images:
- assets/img/tistory/78/image-001.png
source:
  provider: tistory
  id: 78
---

제어 이론이나 로보틱스 분야에서 시스템의 **안정성(Stability)** 은 가장 중요한 주제 중 하나다. 단순히 시뮬레이션 결과가 잘 나왔다고 해서 실제 시스템이 항상 안정적으로 동작한다고 보장할 수는 없다. 이때 수학적으로 안정성을 증명하는 강력한 도구가 바로 **Lyapunov Function**이다.

## Lyapunov Function이란?

Lyapunov function은 시스템 상태 $x$에 대해 정의되는 스칼라 함수 $J(x)$다. 이를 통해 시스템이 시간이 지남에 따라 평형점(예: 원점)으로 수렴하는지를 확인할 수 있다. 핵심 조건은 다음과 같다.

- $J(x) > 0$ for $x \neq 0$, 그리고 $V(0) = 0$
  → 평형점이 아닌 곳에서는 항상 양수, 평형점에서는 0
- $\dot{J}(x) < 0$
  → 시간이 흐르면서 값이 줄어듦

즉, $V(x)$는 일종의 “에너지”처럼 정의되고, 그 에너지가 시간이 갈수록 줄어든다면 시스템은 자연스럽게 평형점으로 수렴한다.

## 직관적인 이해

![](/assets/img/tistory/78/image-001.png)

Lyapunov function을 물리적 에너지 함수로 비유하면 쉽다.

- **공이 그릇 안에 있는 상황**을 떠올려 보자.
- 그릇의 바닥은 평형점, 그릇 모양은 $J(x)$다.
- 공이 바닥에서 벗어나면 위치 에너지가 커진다.
- 시간이 지나면서 마찰 때문에 공은 결국 바닥으로 굴러간다.
- 이것이 바로 Lyapunov 안정성의 직관적인 모습이다.

## 왜 중요한가?

- **시뮬레이션이 아닌 수학적 보장**을 제공한다.
- 비선형 시스템에서도 적용 가능하다.
- LQR, MPC 같은 현대 제어 기법에서도 안정성 보장의 근거로 사용된다.
