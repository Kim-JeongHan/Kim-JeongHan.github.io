---
layout: post
title: c++ 구조체 memory layout 이란?
date: 2025-09-01 22:33:15 +0900
slug: cpp-struct-memory-layout
render_with_liquid: false
categories:
- 프로그래밍
- c++
tags:
- c++
- memory-layout
last_modified_at: 2025-09-01 22:34:25 +0900
source:
  provider: tistory
  id: 66
---

## 일반적인 구조체

```cpp
typdef struct{
  char first;
  char second;
  char third;
  short fourth;
}smaple_t;
sample_t var;
```

해당 구조체는 총 char 1바이트 3개, short 2바이트 총 5바이트로 예상된다. 그러나 실제로 구조체는 6바이트를 가지고 있다. 이유는 cpu의 메모리 정렬(memory alignment)와 관련이 있다.

## memory alignment

CPU는 각 메모리에 접근할 때 특정 바이트의 숫자를 주로 읽는다. 이 바이트의 수는 주로 워드(word)라고 한다. 메모리는 워드로 나뉘며, 메모리로부터 읽고 쓰기 위해 CPU가 사용하는 작은 기본 단위를 워드라 한다. 워드에 있는 바이트의 실제 숫자는 아키텍처에 따라 다르다. 예를 들어 대부분의 64bit머신에서 워드 크기는 32비트 또는 4바이트이다. 메모리 정렬을 고려하면, 바이트가 워드의 시작점에 있을때, 이 변수는 메모리에 정되어 있다고 한다. 이러한 방식으로 CPU는 메모리 접그에 최적화된 숫자에서 그 값을 로드한다.

앞의 char 3바이트는 첫번째 워드에 탑재한다. 만약에 뒤의 short 2바이트중 한바이트를 첫번째 워드에 탑재하고, 두번째 워드에 나머지 바이트를 넣는다면, CPU는 값을 얻기 위해 2개의 메모리에 접근해야하는 불상사가 생긴다. 이를 해결하기 위해 첫번째 워드에 char의 세 바이트를 넣고 패딩(padding)을 사용해 메모리의 값을 정렬한다.

즉, 요약하자면 memory alignment를 패딩을 사용하여 구현되며, 아키텍쳐의 성능향상을 위해 자동으로 구현된다.

## 비정렬 구조체, 패킹된 구조체(Pakced structure)

```cpp
struct __attribute__((__packed__)) sample_t {
  char first;
  char second;
  char third;
  short fourth;
};
```

해당 구조체는 padding을 없앤 구조체이다. 이러한 구조체의 선언은 메모리 최적화를 요구하는 환경에서 사용될수 있으나, 대부분의 아키텍쳐에서 성능에 악영향을 미친다.

구조체를 만들때, 패딩이 덜 생기는 방식으로 구조체를 만든다면 메모리 최적화, 속도 최적화에 도움이 될수 있다.
