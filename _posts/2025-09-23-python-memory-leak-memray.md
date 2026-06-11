---
layout: post
title: 파이썬 moemory leak 디버그(memray)
date: 2025-09-23 15:59:20 +0900
slug: python-memory-leak-memray
render_with_liquid: false
categories:
- 프로그래밍
- python
tags:
- python
- memray
- memory-leak
last_modified_at: 2025-09-23 16:30:27 +0900
imported_images:
- assets/img/tistory/77/image-001.png
source:
  provider: tistory
  id: 77
---

최근 사내 모든 시스템을 최적화 TFT를 진행하는 과정에서 ROS 기반 Python 노드를 실행하면서 메모리가 비정상적으로 증가하는 현상을 발견했다. 프로그램을 오랫동안 실행할수록 RSS 값이 계속 늘어나 결국 시스템이 느려지는 문제가 발생했다. 이번 글에서는 문제를 추적하고 해결한 과정을 기록한다.

## 1. 증상 발견

- htop와 nvidia-smi로 확인했을 때, Python 노드의 메모리 사용량이 실행 시간에 따라 지속적으로 증가했다.
- GPU 메모리 역시 점점 늘어나 reset 되지 않았다.

이는 전형적인 **메모리 누수(memory leak)** 패턴이었다.

## 2. 추적 도구 선택

Python 메모리 누수를 잡기 위해 Bloomberg에서 공개한 [Memray](https://bloomberg.github.io/memray/)를 사용했다.
Memray는 Python 코드뿐만 아니라 C 확장 모듈(PyTorch, Open3D 등) 내부에서 발생하는 메모리 할당까지 추적할 수 있다.

```cmake
pip install memray
```

## 3. 실행 및 데이터 수집

ROS 노드를 Memray로 실행했다:

```bash
memray run <검사할 pythoin>.py
```

프로그램 실행이 끝나면 결과가 .bin 파일로 저장된다.

## 4. 분석

### Summary 리포트 생성

```bash
memray summary memray-p.py.1184031.bin
```

리포트를 보면, 대부분의 메모리가 mv3_infer_from_ros_image → torch.Tensor.to() 경로에서 반복적으로 할당되고 있었다.
특히 to() 호출로 인해 **4.9GB 이상**이 GPU 메모리에 누적된 것이 확인되었다.

![](/assets/img/tistory/77/image-001.png)

## 5. 원인

코드를 다시 살펴본 결과, **ROS 콜백 함수 안에서 모델을 반복적으로 생성**하고 있었다.

즉, 카메라 이미지가 들어올 때마다 새로운 PyTorch 모델이 로드되고 GPU로 복사되면서 메모리가 점점 쌓인 것이다. 사내에서는 lru_cache방식으로 객체 생성함수가 wrapping되어있어서 추가로 모델이 반복적으로 로드되지않을것이라고 예상했으나, 파라미터가 변화하는 상황에서 객체가 재생성되었다.

## 6. 해결

해당 구조를 singleton으로 바꾸어 해결했다. 모델자체의 생성을 한번만 생성할수 있게 재개발하였다.
