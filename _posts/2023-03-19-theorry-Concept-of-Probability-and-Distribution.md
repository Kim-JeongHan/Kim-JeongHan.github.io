---
layout: post  
title: "1 Concept of Probability and Distribution"  
subtitle: "🌙 확률의 개념과 확률 분포"  
categories: theory  
tags: 확률과통계 확률의정의 확률의목표 확률변수 확률분포
comments: true
---

- 요약
	> 🌙 확률의 개념과 확률 분포


- [확률](#확률)
  * [확률이 필요한 이유?](#확률이-필요한-이유)
    + [☾ 일반 적인 확률](#-폭넓은-확률의-정의)
    + [☾ 폭넓은 확률의 정의](#-무작위적이고-예측-불가능한-일상)
    + [☾ 무작위적이고 예측 불가능한 일상](#-무작위성에-숨어-있는-규칙-확률--확률분포sample-space)
    + [☾ 무작위성에 숨어 있는 규칙→ 확률 → 확률분포(sample space)](#-무작위성에-숨어-있는-규칙-확률--확률분포sample-space)
    + [☾ 무작위적 현상의 확률(분포)를 이용](#-무작위적-현상의-확률분포를-이용)
    + [<span style="color:fuchsia">☾ 확률 이론의 주요 목표(sample space)</span](#-확률-이론의-주요-목표sample-space)
  * [How do we handle probability?](#how-do-we-handle-probability)
    + [☾ 확률 변수(random variable)](#-확률-변수random-variable)
    + [☾ 확률 분포(probability distribution function)](#-확률-분포probability-distribution-function)
    + [☾ 확률 분석의 대상 설정](#-확률-분석의-대상-설정)
    + [☾ 확률 이론의 주요 매개변수](#-확률-이론의-주요-매개변수)


# 확률

## 확률이 필요한 이유?

### ☾ 일반 적인 확률
<img src="https://Kim-JeongHan.github.io/assets/img/theory/probability&statistics/Concept-of-Probability-and-Distribution-1.png" width="80%">

### ☾ 폭넓은 확률의 정의

- 무작의(random)로 나타나는 어떤 현상이 발생하거나 존재할 가능성(possibility)의 크기
    - 무작위 : 예측 불가능한 불규칙적인 발생
    - 현상 : 숫자, 집합(사건), 벡터 (두개 이상의 값이 동시에 발생)
- 확률 대상의 무작위성(radomness)
    - 예측 불가능(unpredictable)
- 확률 대상 범위 제한: 시행(Trial, experiment), <span style="color:fuchsia">표본 공간(sample space)</span> 
    - **표본 공간** :  시행으로부터 무작위로 발생하는 현상의 **전체 집합**
    - 예 : 주사위 1개 던지기 - {1,2,3,4,5,6}
    - 예 : 주사위 2개던지기 - {(1,1),(1,2) ….. (6,6)} 36가지 2차원 벡터
- 제한된 범위에서 총확률의 계산
    - 발생 가능한 모든 현상들의 확률의 합 = 1

### ☾ 무작위적이고 예측 불가능한 일상

- 일기예보 - 불확실한 현상에 대한 예측문제
- 처리 대상인 정보 신호의 무작위성 - 통신, 영상, 음성, 센서

###  <span style="color:red">☾ 무작위성에 숨어 있는 규칙→ 확률 → 확률분포(sample space)</span>

- 예 : 주사위{1,2,3,4,5,6,} 예측 VS 주사위{1,1,1,2,3,4,} 예측
- 위 두가지 주사위중에서 앞으로를 예측하기 쉬운 것은 1이 좀더 많이 나온 주사위 이다.

### ☾ 무작위적 현상의 확률(분포)를 이용

- <span style="color:red">예측/추정 가능성(sample space)</span>은 높이고, 오류/실패 가능성은 낮춤
- 잡음이나 불확실한 신호 성분 제거

### <span style="color:fuchsia">☾ 확률 이론의 주요 목표(sample space)</span>

- 무작위 현상의 확률 특성과 분포 파악(수학적 모델, 통계적 모델)
- 추정, 예측, 판별 학습 등에 대한 확률적 해석

## How do we handle probability?

### ☾ 확률 변수(random variable)

- 확률을 갖는 무작위 현상을 숫자(정수, 실수)에 대응
- 무작위 현상을 수학적 변수로 취급

### ☾ 확률 분포(probability distribution function)

- 무작위 현상 각각에 대한 확률값을 정의
- 무작위 현상은 변수로 하고 함수값은 확률(또는 확률밀도)값을 갖는 함수를 설계하여 표현(확률분포함수)

### ☾ 확률 분석의 대상 설정

- 대상 현상의 분석 - 단일 확률 변수
    - 예: 키, 체중
- 여러 현상의 연합 분석 - 다중 확률 변수
    - 변수간의 상관성을 고려
    - 예 : (키, 체중) → 연관성이 어느정도 있음

### ☾ 확률 이론의 주요 매개변수

- 평균, 분산, 상관계수
- 무작위 현상에 따른 독특한 확률 분포함수 모델
    - 예: 정규분포, 포아송 분포

---

> 이 글은 이상화 교수님의 확률과 통계를 기반으로 작성되어있습니다.
* [이상화 교수님의 선형대수](https://www.youtube.com/@user-xx1mm6mk5y)
<!--stackedit_data:
eyJoaXN0b3J5IjpbODg5NTc0MzAwLDE3NjM2NTM3MDksMTQ4MT
Q2NjkyMiw1ODUyNzUwODRdfQ==
-->
