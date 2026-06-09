---
layout: post  
title: "2 Concept of Random variable and probability distribution"  
subtitle: "🌙 확률 변수와 확률분포에 대해 알아보자."  
categories: theory  
tags: 확률과통계  확률변수 확률분포
disqus_comments: true
---

- 요약
	> 🌙 Random variable와 probability distribution의 차이를 알아보자.


- [01) Concept of Random variable and probability distribution](#01-concept-of-random-variable-and-probability-distribution)
  * [01_Random Variable (확률 변수)의 필요성](#01_random-variable-확률-변수의-필요성)
    + [☾ Probability(확률)](#-probability확률)
    + [☾ Random 현상](#-random-현상)
    + [☾ 어떻게 random현상과 확률을 수학적으로 다룰 것인가?](#-어떻게-random현상과-확률을-수학적으로-다룰-것인가)
  * [02_Random Variable (확률 변수) - 정의역](#02_random-variable-확률-변수---정의역)
    + [☾ 확률 변수(random variable)](#-확률-변수random-variable)
    + [☾ 이산 확률 변수 (discrete random variable)](#-이산-확률-변수-discrete-random-variable)
    + [☾ 연속 확률 변수 (continuos random variable)](#-연속-확률-변수-continuos-random-variable)
  * [03_Probability Distribution (확률 분포) - 치역](#03_probability-distribution-확률-분포---치역)
    + [☾ 확률 분포 함수(Probability distribution function)](#-확률-분포-함수probability-distribution-function-)
    + [☾ 확률 분포 함수(Probability distribution function)의 모델](#-확률-분포-함수probability-distribution-function의-모델)


# 01) Concept of Random variable and probability distribution

## 01_Random Variable (확률 변수)의 필요성


### ☾ Probability(확률)

-   무작위(random) 현상의 발생 / 존재 가능성의 크기
-   0 < 확률 < 1

### ☾ Random 현상

-   예측 불가능, 불규칙적인 발생
-   확률 크기에 비례적으로 발생하는 경향 → random 현상의 핷미 단서

### ☾ 어떻게 random현상과 확률을 수학적으로 다룰 것인가?

-   확률 변수(domain)와 확률 분포 함수(range)의 정의

## 02_Random Variable (확률 변수) - 정의역


### ☾ 확률 변수(random variable)

-   확률을 갖는 무작위 현상을 숫자(정수, 실수)에 대응
    
    -   예 : 동전 H/T(표본 공간) → 1/0(확률변수)
    -   영상 신호 : 각 화소의 빛의 세기(표본 공간) → 0~255 정수값으로 대응(확률변수)
-   무작위 현상을 수학 함수의 변수(정의역, domain)로 취급
    
-   표기법 : 대문자 (X,Y) - 확률 변수 이름, 소문자(x,y)- 확률변수의 값(X=1)
    
    <img src="/assets/img/theory/probability&statistics/Concept-of-Random-variable-and-probability-distribution-1.png" width="80%">

### ☾ 이산 확률 변수 (discrete random variable)

-   일반적으로 정수값에 대응하는 확률 변수
    -   0,1,2,3,4,…
-   개수, 횟수 등과 관련
    -   예 : 이항 분포(n번 반복 시행하여 특정한 경우가 x번 발생할 확률)
    -   예 : 포아송 분포(어떤 시간 동안에 특정한 사건이 발생하는 횟수에 대한 확률)
-   디지털 양자화된 값과 관련
    -   예: 영상 신호: 각 화소에 들어오는 빛의 세기를 0~255정수로 대응

### ☾ 연속 확률 변수 (continuos random variable)

-   특정한 구간의 모든 실수값에 대응하는 확률 변수
    -   예: (0,1), 모든 실수 구간
-   특정한 구간에서 어떠한 실수값이든 무한하게 나올 수 있는 경우
    -   예 : 정규분포
    -   참고 : 셀 수 없는 정도의 무한함(uncountable infinite)
-   실제 변수를 다룰 때는 유한한 개수의 이산 변수로 다루는 경우가 많음
    -   일정한 간격으로 확률변수를 quantization → 특정 구간을 quantization
    -   연속 확률밀도 함수를 확률분포함수로 적용

## 03_Probability Distribution (확률 분포) - 치역

----------

### ☾ 확률 분포 함수(Probability distribution function)

-   표본 공간에 대응하는 모든 확률변수의 값에 대하여 그 확률을 함수의 값으로 취급
-   확률분포 함수의 정의역(domain) - 확률변수
-   확률분포함수의 치역(range) - 확률(이산), 확률밀도(연속)

    <img src="/assets/img/theory/probability&statistics/Concept-of-Random-variable-and-probability-distribution-2.png" width="80%">

<aside> 💡 논문에서 대문자와 소문자를 잘 구분해서 보아야한다.

</aside>

### ☾ 확률 분포 함수(Probability distribution function)의 모델

 <img src="/assets/img/theory/probability&statistics/Concept-of-Random-variable-and-probability-distribution-3.png" width="80%">

---

> 이 글은 이상화 교수님의 확률과 통계를 기반으로 작성되어있습니다.
* [이상화 교수님의 선형대수](https://www.youtube.com/@user-xx1mm6mk5y)
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE0MTE4NDk0NjQsLTE3ODk4Nzg5OSwxNj
YxMzk1MjUzLDEzMzMxMTU5MiwxNTgwMTg4NTcyLDM1NzIxMDQ2
NCwtMjEyNjcyMDgwNSwtMTQ1ODkzMzM0MywtMzcyNzc4OTk4XX
0=
-->
