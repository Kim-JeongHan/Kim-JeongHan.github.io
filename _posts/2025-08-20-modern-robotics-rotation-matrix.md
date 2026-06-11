---
layout: post
title: '[Modern Robotics] Rigid body의 표현 - 회전 행렬(Roataion Matrix)'
date: 2025-08-20 23:57:26 +0900
slug: modern-robotics-rotation-matrix
render_with_liquid: false
categories:
- 공부
- 로봇공학
tags:
- modern-robotics
- rotation-matrix
last_modified_at: 2025-08-20 23:58:23 +0900
imported_images:
- assets/img/blog/modern-robotics-rotation-matrix/image-001.png
- assets/img/blog/modern-robotics-rotation-matrix/image-002.png
- assets/img/blog/modern-robotics-rotation-matrix/image-003.png
series: modern-robotics
series_order: 2
source:
  provider: tistory
  id: 58
---

## **Rigid body의 표현 - 회전 행렬**

앞서서 회전 행렬 R의 9개 항목중 실제로는 3개만 독립적으로 선택이 가능하다

### 제약조건

1. **단위 벡터 조건 (unit norm condition) - 3개**
2. **직교성 조건 (orthogonality condition) - 3개**

이 6개의 제약조건은 하나의 행렬조건으로 표현 가능하다.

### 추가조건

추가적으로 해당좌표계가 오른손 좌표계기준인지 왼손좌표계 기준인지 구별하기 위해 determinant 조건을 추가한다.

수학적 의미설명

<div class="table-responsive tistory-table">
<table>
<tbody>
<tr>
<td>항목</td>
<td>수학적 의미</td>
<td>설명</td>
</tr>
<tr>
<td>단위 벡터 조건</td>
<td>​$\|r_i\| = 1$</td>
<td>각 열 벡터가 단위 벡터</td>
</tr>
<tr>
<td>직교성 조건</td>
<td>$ r_i^T r_j = 0 (i ≠ j) $</td>
<td>서로 직교</td>
</tr>
<tr>
<td>직교 행렬 조건</td>
<td>$ R^T R = I $</td>
<td>위 두 조건을 포함</td>
</tr>
<tr>
<td>오른손 조건</td>
<td>$ \det R = 1 $</td>
<td>$ \hat{x}_b \times \hat{y}_b = \hat{z}_b $</td>
</tr>
</tbody>
</table>
</div>

### 회전행렬 Lie group 표현

회전 행렬의 집합인 SO(2)와 SO(3)는 수학적으로 group이라고 불린다.

### Group조건

- **폐쇄성(Closure)**: A,B가 그룹에 속할 때, AB 또한 그룹에 속한다.
- **결합법칙(Associativity)**: (AB)C=A(BC) 가 항상 성립한다.
- **항등원 존재(Identity)**: AI=IA=A를 만족하는 항등원 $I$가 존재한다. (SO(n)에서는 단위 행렬)
- **역원 존재(Inverse): $AA^{-1}=A^{-1}A=I$** 를 만족하는 역원 $A^{-1}$이 존재한다.

## 회전행렬의 용도

1. 어떤 방향을 표현하기 위해
2. 기준좌표계를 바꾸기 위해
3. 벡터나 프레임을 회전하기 위해

### 방향 표현

- $R_c$를 쓸 때, **프레임 $\{c\}$의 방향이 고정 프레임 $\{s\}$에 대해 어떤지를 나타내고 있는 것**

→ $R_{sc}$로 쓸수도 있다.

### 기준 좌표계 변경

$R_{ac} = R_{ab} R_{bc}$

회전행렬 $R_{ab}$에 $R_{bc}$를 곱해서 $R_{ac}$라는 새로운 기준 좌표계를 만들 수 있다.

항목 의미

<div class="table-responsive tistory-table">
<table>
<tbody>
<tr>
<td>$R_{ac} = R_{ca}^{-1} = R_{ca}^T$</td>
<td>서로의 전치 행렬</td>
</tr>
<tr>
<td>$R_{ac} = R_{ab} R_{bc}$</td>
<td>좌표계 기준 변경</td>
</tr>
<tr>
<td><b>소거 규칙</b></td>
<td>$R_{ab} R_{bc} = R_{ac}$, $R_{ab} p_b = p_a$</td>
</tr>
</tbody>
</table>
</div>

### 벡터나 프레임 회전

$R=Rot( \hat\omega ,\theta)$

단위 행렬(기준 방향)에서 시작하여 **$\hat{\omega}$축을 중심으로 $\theta$만큼 회전**한 결과가 $R$이라는 뜻이다.

이를 사용하여 벡터나 프레임을 회전시킬 수 있다.

![](/assets/img/blog/modern-robotics-rotation-matrix/image-001.png)
![](/assets/img/blog/modern-robotics-rotation-matrix/image-002.png)

### 기준 프레임에 따른 회전의 차이

고정프레임에서 바라본 바디프레임 : $R_{sb}$

- 고정 프레임 기준 회전 : $R_{sb′}​=R⋅R_{sb}$
- 바디 프레임 기준 회전 : $R_{sb^{′′}}​=R_{sb}⋅R$

회전 행렬을 왼쪽에다 곱하면 고정프레임 기준으로 회전 한것이다.

회전 행렬을 오른쪽에다가 곱하면 바디프레임 기준으로 회전한것이다.

이는 전혀 다른 두 결과를 보인다.

![](/assets/img/blog/modern-robotics-rotation-matrix/image-003.png)

따라서 벡터를 회전시키기 위해서는 이미 벡터가 표현되어 있는 좌표계안에서 연산이 이루어진다는 것을 의미하여, v'=Rv로 표현된다.
