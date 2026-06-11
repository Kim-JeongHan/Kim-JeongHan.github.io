---
layout: post
title: 데이터 분석 Tool - PlotJuggler
date: 2025-08-20 22:08:29 +0900
slug: plotjuggler-data-analysis
render_with_liquid: false
categories:
- 프로그래밍
tags:
- plotjuggler
- 데이터분석
last_modified_at: 2025-08-20 22:09:30 +0900
imported_images:
- assets/img/blog/plotjuggler-data-analysis/image-001.png
- assets/img/blog/plotjuggler-data-analysis/image-002.png
source:
  provider: tistory
  id: 54
---

## PlotJuggler

**PlotJuggler**는 ROS 환경에서 **시간 기반 데이터(Time Series)**를 실시간으로 시각화하고 분석하는 데 특화된 오픈소스 툴이다. 특히 로봇 제어 및 센서 데이터를 다루는 환경에서 매우 유용하게 활용된다.

#### **핵심 기능**

- 실시간 시각화: ROS 토픽에서 실시간 데이터를 sub하여 그래프에 반영
- 드래그 앤 드롭 방식의 직관적인 UI: 토픽, 메시지 필드를 GUI 상에서 시각적으로 매핑 가능
- CSV / .bag 파일 지원: 기록된 ROS bag 파일이나 CSV 파일을 불러와 분석 가능
- 수학 표현식 지원: Plot 내에서 필드 간 연산 및 파생 변수 계산 가능 (예: error=desired−actualerror = desired - actualerror=desired−actual)

![](/assets/img/blog/plotjuggler-data-analysis/image-001.png)

### **설치**

```bash
sudo apt install ros-${ROS_DISTRO}-plotjuggler \
                 ros-${ROS_DISTRO}-plotjuggler-ros
```

### **고급기능**

![](/assets/img/blog/plotjuggler-data-analysis/image-002.png)

간단한 함수 및, plugin 지원

- quaternion → rpy
- integral등등

---

이걸로 분석해서 가져가면 팀장님한테 칭찬을 들을 수 있다. 진짜 개인적으로 많이쓰는 기능이다.
