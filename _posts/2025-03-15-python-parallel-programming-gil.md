---
layout: post
title: '[Parallel Programming] 파이썬의 병렬프로그래밍- GIL'
date: 2025-03-15 16:41:14 +0900
slug: python-parallel-programming-gil
render_with_liquid: false
categories:
- 프로그래밍
- python
tags:
- python
- parallel-programming
- gil
last_modified_at: 2025-03-16 00:06:28 +0900
imported_images:
- assets/img/tistory/26/image-001.png
- assets/img/tistory/26/image-002.png
- assets/img/tistory/26/image-003.png
- assets/img/tistory/26/image-004.png
source:
  provider: tistory
  id: 26
---

## 개요

### 병렬프로그램이란 무엇일까?

소위 말하는 정의는 여러 ‘프로세스’와 ‘스레드’를 동시에 실행되도록 프로그래밍을 작성하는 프로그맹 기술을 말한다.

우리는 이러한 병렬프로그램으로 계산 및 작업 수행능력을 빠르게 완료시키는데 주 목적이 있다.

언어마다 이러한 병렬프로그래밍은 큰 차이가 있고, 그 중 python의 병렬프로그래밍에 대해서 좀더 깊이 있게 다루어 보겠다.

본격적인 python의 병렬프로그래밍을 다루기전에 중요하게 알아야할 것이 파이썬의 설계원칙이다.

### Python의 설계원칙

![](/assets/img/tistory/26/image-001.png)

파이썬은 유저입장에서 매우 직관적이고 접근성있게 만들어진 언어이다.

이말은 반대로 말하면, c나 기타 다른언어보다 훨씬 직관적으로 만들면서 유저입장을 생각하면서 설계되었다는 말을 의미한다.

그래서 파이썬은 소프트웨어적인 지식이 다른 언어보다 덜 필요하게 설계되었는데, 여기서 나오는게 GIL이다.

병렬프로그래밍은 일반 파이썬을 쉽게 사용하려는 유저의 입장에서는 어렵게 다가오는 프로그래밍이다. 이 안에 자세하게 담겨있는 Data Racing, Semaphore, deadlock, thread, process등의 개념은 이러한 병렬프로그램을 더욱 어렵게 만들었다. 그래서 파이썬의 CPython 구현에서는 **GIL(Global Interpreter Lock)**이란 매커니즘을 써서 일반유저입장에서는 하나의 잠금장치를 만들었다. 이를 통해, 유저가 저 위에 복잡한 SW의 지식없이 병렬프로그래밍을 쉽게 처리 할 수 있게 만들었다.

얻는게 있으면 잃는게 있는법, 이러한 파이썬의 GIL은 결국 일반 유저 입장에서의 파이썬을 쉽게 만들었지만, 개발자의 입장에서는 병렬프로그래밍을 힘들게 만들었다. 즉, 파이썬의 인터프레이터에서 여러가지 스레드가 동시에 실행되는 것을 막는 것이다.

## GIL(Global Interpreter Lock)

앞에서 말했듯이 GIL은 GIL은 파이썬 인터프리터의 여러 스레드가 동시에 실행되는 것을 방지하여, 한 번에 하나의 스레드만 파이썬 코드를 실행할 수 있게 하는 것을 의미한다.

이말을 다시한번 설명해보자면 우리가 10초 짜리 Task를 4개 가지고 있을때, single Thread에서는 40초가 걸린다.

![](/assets/img/tistory/26/image-002.png)

이 Task를 두개의 쓰레드를 사용하면 두개의 쓰레드에서 작업을 나누어 관리함으로, 시간의 소요가 20초로 단축된다.

![](/assets/img/tistory/26/image-003.png)

이러한 것이 병렬프로그래밍의 장점인데 파이썬의 Thread는 GIL에 의해서 다르게 작동된다.

![](/assets/img/tistory/26/image-004.png)

바로 병렬인것처럼 작동되는 것이다. 똑같이 40초가 걸리는 것을 알수 있다. 이렇게 Thread를 동시에 실행되는 것을 막고 하나씩 번갈아가면서 수행하는 것을 GIL이라고 하며, 이를 컨텍스트 스위칭이라고한다.

<div class="table-responsive tistory-table">
<table>
<tbody>
<tr>
<td> </td>
<td>single Thread</td>
<td>double thread - expected</td>
<td>double thread - excuted</td>
</tr>
<tr>
<td>Time</td>
<td>40</td>
<td>20</td>
<td>40</td>
</tr>
</tbody>
</table>
</div>

지금까지 말한 이야기만 따르면 GIL은 정말 안좋은 기능인것 처럼 보이며, python에서는 thread를 사용할 이유가 없어 보인다. 그렇다면 python의 쓰레드는 어떤 상황에서 쓸까? 여기서 등장하는 Cpu-boud작업과 I/O작업이다.

### I/O바운드란?

I/O 바운드 작업(I/O-bound tasks)은 컴퓨터의 성능이 주로 입출력(I/O) 작업에 의해 제한되는 작업을 의미한다.

- 파일 읽기/쓰기

- 네트워크 요청

- 데이터베이스 쿼리

### CPU 바운드란?

CPU 바운드 작업(CPU-bound tasks)은 컴퓨터의 성능이 주로 CPU의 처리 능력에 의해 제한되는 작업을 의미한다.

- 대규모 행렬 연산

- 이미지 렌더링

- cpu에서 처리하는 거의 대부분의 연산

특징CPU 바운드 작업I/O 바운드 작업주된 제한 요소CPU 사용률대기 시간최적화 방법예시

<div class="table-responsive tistory-table">
<table>
<tbody>
<tr>
<td><b>특징</b></td>
<td><b>CPU 바운드 작업</b></td>
<td><b>I/O 바운드 작업</b></td>
</tr>
<tr>
<td><b>주된 제한 요소</b></td>
<td>CPU의 처리 능력</td>
<td>입출력 장치의 속도</td>
</tr>
<tr>
<td><b>CPU 사용률</b></td>
<td>높음</td>
<td>낮음</td>
</tr>
<tr>
<td><b>대기 시간</b></td>
<td>거의 없음</td>
<td>I/O 작업 대기 시간 존재</td>
</tr>
<tr>
<td><b>최적화 방법</b></td>
<td>멀티프로세싱, 병렬 프로그래밍</td>
<td>비동기 프로그래밍, 멀티스레딩</td>
</tr>
<tr>
<td><b>예시</b></td>
<td>행렬 연산, 이미지 렌더링</td>
<td>파일 읽기/쓰게, 네트워 요청</td>
</tr>
</tbody>
</table>
</div>

<div class="table-responsive tistory-table">
<table>
<tbody>
<tr>
<td>Feature</td>
<td>CPU-bound Tasks</td>
<td>I/O-bound Tasks</td>
</tr>
<tr>
<td>Limiting Factor</td>
<td>CPU processing power</td>
<td>Speed of I/O devices</td>
</tr>
<tr>
<td>CPU Usage</td>
<td>High</td>
<td>Low</td>
</tr>
<tr>
<td>Waiting Time</td>
<td>Almost none</td>
<td>Exists due to I/O operations</td>
</tr>
<tr>
<td>Optimal Methods</td>
<td>Multiprocessing, Parallel Programming</td>
<td>Asynchronous Programming, Multithreading</td>
</tr>
<tr>
<td>Examples</td>
<td>Matrix operations, Image rendering</td>
<td>File read/write, Network requests</td>
</tr>
</tbody>
</table>
</div>

python의 쓰레드는 CPU바운드의 Task에서는 효용이 없지만 I/O바운드의 task에서는 특정 I/O작업 실행 후 기다리지않고 다른 I/O작업을 실행시킨다. 단일쓰레드에서 I/O작업은 하나가 끝나야 다음 I/O작업이 실행되는 구조이때문에, 이러한 I/O작업에서의 멀티쓰레드는 충분히 효율적이다.

### 요약

- GIL이란?
  - 쓰레드가 동시에 실행하는것을 막는것

- GIL의 단점
  - CPU영역의 Task를 실행시킬때, single thread와 다른게 없다….

- GIL의 장점
  - 멀티쓰레딩 구현에서 고려해야하는 race condition현상을 방지해주며, 파이썬을 쉽게 만들어준다.

- 파이썬의 Threading을 쓰는 이유?
  - I/O작업에서 효과적이다
