---
layout: post
title: "[Git 스터디 3-1] 브랜치 전략"
slug: git-study-03-branch-strategy
subtitle: "Long-running branch, topic branch, ROS 프로젝트 브랜치 운영"
date: 2023-07-18 22:00:00 +0900
last_modified_at: 2023-07-16 15:16:00 +0900
categories:
  - 프로그래밍
  - Git
tags:
  - Git
  - branch
  - robotics
  - git-study
series: git-study
series_order: 5
source:
  provider: notion
  page_id: 1b287ffc-c013-421d-b05d-6d75d3bc5284
  project_id: 2fa9e30d-1d04-489c-a612-db1add10d0c0
render_with_liquid: false
---

Git은 브랜치 생성과 merge 비용이 작기 때문에 브랜치를 적극적으로 활용하는 워크플로가 잘 맞는다. 이 글에서는 장기간 유지하는 브랜치와 짧은 작업 단위 브랜치를 나누어 본다.

## Long-running 브랜치

Git은 3-way merge를 꼼꼼하게 처리하므로 한 브랜치를 다른 브랜치와 여러 번 merge하는 일이 비교적 자연스럽다. 그래서 개발 과정에서 필요한 용도별 브랜치를 만들어 두고 계속 사용할 수 있다.

대표적인 흐름은 다음과 같다.

- `master` 또는 `main`: 배포했거나 배포할 수 있는 안정 코드만 둔다.
- `develop`, `next`: 개발을 진행하고 안정화하는 브랜치로 둔다.
- `proposed`, `pu`: 아직 `develop`이나 `main`으로 올리기 전의 실험적 변경을 모아둔다.

테스트를 거쳐 안정적이라고 판단되면 개발 브랜치의 내용을 안정 브랜치로 merge한다.

![안정적인 브랜치일수록 커밋 히스토리가 뒤쳐짐](/assets/img/blog/git-study-03-branch-strategy/lr-branches-1.png)

개발 브랜치는 공격적으로 히스토리를 만들고, 안정 브랜치는 충분히 검증된 히스토리만 따라간다고 생각하면 된다.

![각 브랜치를 하나의 실험실로 생각](/assets/img/blog/git-study-03-branch-strategy/lr-branches-2.png)

실험실에서 충분히 테스트하고 실전에 배치하는 과정으로 보면 이해하기 쉽다.

## Topic 브랜치

토픽 브랜치는 한 가지 주제나 작업을 위해 만든 짧은 브랜치다. 앞에서 사용한 `iss53`, `hotfix` 같은 브랜치가 토픽 브랜치다.

Git에서는 브랜치를 만드는 비용이 작기 때문에 기능, 버그, 실험 단위로 브랜치를 나누기 좋다. 각 작업은 독립적으로 유지하다가, master 또는 develop에 merge할 시점이 되면 순서에 맞게 병합하면 된다.

![토픽 브랜치 여러 개가 있는 모습](/assets/img/blog/git-study-03-branch-strategy/topic-branches-1.png)

![토픽 브랜치를 merge한 뒤의 모습](/assets/img/blog/git-study-03-branch-strategy/topic-branches-2.png)

지금까지 다룬 브랜치 생성과 merge는 모두 로컬 저장소 안에서 일어난다. 로컬에서 브랜치를 만들고 merge한다고 해서 자동으로 서버와 통신하는 것은 아니다.

## ROS 프로젝트에 적용해보기

간단한 모바일 로봇 프로젝트를 진행한다고 생각해보자. 먼저 `master` 또는 `main`에서 `develop` 브랜치를 만들고, 실제 개발은 대부분 `develop`에서 진행한다.

기능 단위는 feature 브랜치로 나눈다.

| Feature | Package | 실제 브랜치 이름 |
| --- | --- | --- |
| 모터 제어 및 odometry | `로봇이름_bringup` | `feature/bringup` |
| 로봇의 visual, physical, structure 등 기구 정보 | `로봇이름_description` | `feature/description` |
| SLAM | `로봇이름_slam` | `feature/slam` |
| Navigation | `로봇이름_navigation` | `feature/navigation` |
| 원격조종(teleop) | `로봇이름_teleop` | `feature/teleop` |
| 가상환경(optional) | `로봇이름_gazebo` | `feature/gazebo` |
| 다양한 센서 | `로봇이름_sensor` | `feature/sensor` |

각 기능 브랜치에서 개발이 끝나면 테스트를 통과한 뒤 `develop`으로 merge한다. 대부분의 feature 개발이 끝나고 `develop`이 안정되면 그때 `master` 또는 `main`으로 merge한다.

주의할 점은 테스트가 성공적으로 완료된 변경만 `develop`에 merge하는 것이다. 팀 프로젝트에서는 브랜치를 나누는 것만큼 merge 기준을 정하는 것도 중요하다.

## References

- [Pro Git: 분산 환경에서의 Git](https://git-scm.com/book/ko/v2/ch00/ch05-distributed-git)
