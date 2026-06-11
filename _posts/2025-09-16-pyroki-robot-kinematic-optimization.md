---
layout: post
title: 'Tool 분석 - PyRoki: A Modular Toolkit for Robot Kinematic Optimization'
date: 2025-09-16 00:49:20 +0900
slug: pyroki-robot-kinematic-optimization
render_with_liquid: false
categories:
- Tool
tags: []
last_modified_at: 2025-09-16 00:49:33 +0900
imported_images:
- assets/img/tistory/72/image-001.png
source:
  provider: tistory
  id: 72
---

# 도입

robot kinematics에 최적화를 위한 범용적인 tool을 만들겠다.

기존 라이브러리들을 특정작업에만 최적화되어 있어서, 다른 문제로 확장하기 어려운것 같다. variable과 cost function을 모듈화하여, IK, trajectory optimization, motion retargeting을 pyroki라는 틀안에서 다룰 수 있도록 하겠다.

## 핵심 설계

1. modular : cost function을 모듈러하게 설계
2. Extensible : cost weights 튜닝을 위한 real-time interface제공, 자동화된 differctionation을 통한 빠른 prototyping이 가능하게 해줌 analytical Jacobian지원
3. Cross-platform : CPU, NPU, TPU 모두 지원

![](/assets/img/tistory/72/image-001.png)

## 비용함수(composable cost function로 modular 방식으로 디자인)

custom cost function을 지원하지만 이미 지원하는 cost function들이 있다. 이건 LM optimizer를 사용했다.

1. Joint pose cost
2. Joint Limit Cost
3. Velocity Limit cost
4. Joint Regularization Cost
5. Smoothness Cost
6. Manipulability Cost
7. Collision Avoidance Cost

## Interactive Robot Web viewer

viser라는 tool을 사용해서, cost function의 weight을 즉각적으로 보면서 튜닝 할수 있다.

# 적용 application

1. IK
2. trajectory optimization
3. motion retargeting
