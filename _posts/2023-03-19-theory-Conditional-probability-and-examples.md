---
layout: post  
title: "3 Conditional probability and examples"  
subtitle: "🌙 조건부 확률과 예시를 알아보자."  
categories: theory  
tags: 확률과통계  조건부확률
comments: true
use_math: true
---

- 요약
	> 🌙 Random variable와 probability distribution의 차이를 알아보자.

- [01) Conditional probability and examples](#01-conditional-probability-and-examples)
  * [01_Conditional probability의 정의](#01_conditional-probability의-정의)
    + [☾ P(A|B)](#-pab)
    + [☾ P(A and B)](#-pa-and-b)
  * [02_Conditional probability Example](#02_conditional-probability-example)
    + [☾ Ex: 안경 착용할 확률 - 100명의 학생에서 한 명 무작위 추출](#-ex-안경-착용할-확률---100명의-학생에서-한-명-무작위-추출)
    + [☾ Ex: 부품을 납품하는 3 suppliers, 부품 불량(defect) 확률](#-ex-부품을-납품하는-3-suppliers-부품-불량defect-확률)
    + [☾ Ex: Communtcation channel](#-ex-communtcation-channel)
  * [03_실생활에서의 Conditional probability](#03_실생활에서의-conditional-probability)


# 01) Conditional probability and examples

  

## 01_Conditional probability의 정의


  

### ☾ P(A|B)

  

- B 사건에 속하는 random 현상(확률변수)이 발생했을 때, 동시에 A사건에도 속하는 현산(확률변수)일 확률

- P(A): random현상(확률 변수)이 사건 A에 속할 확률

- B: 새로운 (축소된) 표본 공간

  

$$
P(A|B) = \frac{P(A\cap B)}{P(B)}

\\

-> \frac{n(A\cap B)/n(s)}{n(B)/n(s)}
$$

   <img src="https://Kim-JeongHan.github.io/assets/img/theory/probability&statistics/Conditional-probability-and-examples-1.png" width="80%">

  

### ☾ P(A and B)

  

- 두 사건 A와 B에 동시에 속하는 경우의 확률

- 조건부 확률을 이용

$ P(A\cap B) = P(A|B)P(B) $

$ P(A\cap B)=P(B|A)P(A) $

  

## 02_Conditional probability Example

### ☾ Ex: 안경 착용할 확률 - 100명의 학생에서 한 명 무작위 추출

   <img src="https://Kim-JeongHan.github.io/assets/img/theory/probability&statistics/Conditional-probability-and-examples-2.png" width="80%">
  

1. P(안경을 착용) → P(WG)=$ \frac{60}{100} $

2. P(안경을 착용한 여학생) → P(WG and G) = $ \frac{20}{100} $

3. P(여학생 중에서 안경을 착용) → $ \frac{P(WG)}{(P(WG\,and\,G)}=\frac{0.2}{0.5} =0.4 $

  

### ☾ Ex: 부품을 납품하는 3 suppliers, 부품 불량(defect) 확률

  
   <img src="https://Kim-JeongHan.github.io/assets/img/theory/probability&statistics/Conditional-probability-and-examples-3.png" width="80%">
  

1. 총 6000개에서 1개의 부품을 선택하였을 때, P(A and defect)?

→ n(A and defect)/총 부품수 = (1000*0.05)/6000

→ $ P(A \cap defect) = P(defect|A)P(A) $

  

### ☾ Ex: Communtcation channel

  
   <img src="https://Kim-JeongHan.github.io/assets/img/theory/probability&statistics/Conditional-probability-and-examples-4.png" width="80%">

  

- 0.7 = P(y1|x1)

- 0.3 = P(y2|x1)

- 0.2 = P(y2|x2)

- 0.8 = P(y1|x2)

  

---

  

## 03_실생활에서의 Conditional probability

  
   <img src="https://Kim-JeongHan.github.io/assets/img/theory/probability&statistics/Conditional-probability-and-examples-5.png" width="80%">


---

> 이 글은 이상화 교수님의 확률과 통계를 기반으로 작성되어있습니다.
* [이상화 교수님의 선형대수](https://www.youtube.com/@user-xx1mm6mk5y)
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTQ3MDU4NjE4OSwyMTIyNjAzMTI5LDEzNz
M3OTU0NDMsLTE5NDg1OTg5OTUsMjA3NDc3NDAwOSwtMTM1MzIy
MTAwMSwtMTM3MDY5NTc3LDEyMTgwMTY2NzYsLTk1MDY5ODY5Mi
wzMDA1MTM2MiwtMTg1Njc5MDQ0N119
-->
