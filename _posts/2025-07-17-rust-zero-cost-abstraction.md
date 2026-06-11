---
layout: post
title: Rust에서의 Zero-cost Abstraction
date: 2025-07-17 11:08:24 +0900
slug: rust-zero-cost-abstraction
render_with_liquid: false
categories:
- 프로그래밍
- Rust
tags:
- rust
- zero-cost-abstraction
last_modified_at: 2025-07-17 11:08:24 +0900
source:
  provider: tistory
  id: 51
---

## 개요

**Zero-cost abstraction**은 Rust의 철학 중 하나로, “고수준의 추상화를 제공하지만, 런타임 성능 손실은 없다”는 개념이다. 즉, 컴파일 타임에 모든 추상화를 제거하여, 추상화를 사용하지 않은 코드와 동일한 성능을 갖도록 한다.

C++에서도 등장한 개념이지만, Rust는 이를 더 발전시켰다.

##

## 왜 중요한가?

일반적으로 프로그래밍 언어에서 추상화(예: trait, 제네릭, iterator 등)를 사용하면 가독성과 재사용성이 좋아지지만, 성능 저하라는 대가가 따른다.

하지만 Rust에서는 **Zero-cost abstraction**을 통해 다음을 동시에 얻을 수 있다:

- C만큼 빠른 실행 성능
- 추상화에 기반한 깔끔한 코드 구조
- 메모리 안전성 보장 (no GC)

## 예시 1: Iterator vs for-loop

### 일반적인 for-loop

```angelscript
let nums = vec![1, 2, 3, 4, 5];
let mut sum = 0;
for i in 0..nums.len() {
    sum += nums[i];
}
```

### Iterator 기반 추상화

```angelscript
let nums = vec![1, 2, 3, 4, 5];
let sum: i32 = nums.iter().sum();
```

Rust에서는 iter() 와 sum() 같은 메서드는 trait 기반 고수준 추상화이다. 하지만 컴파일러는 이 코드를 분석하여 for-loop와 **동일한 기계어 코드**로 최적화한다. 추상화의 비용이 없기 때문에 이것이 바로 "zero-cost abstraction"이다.

## 예시 2: generic 함수

```groovy
fn add<T: std::ops::Add<Output = T>>(a: T, b: T) -> T {
    a + b
}
```

이런 함수는 런타임에 T가 결정되지 않는다. 대신 **모노모피제이션(monomorphization)** 과정을 통해 컴파일 타임에 각 타입별 함수가 생성된다:

```rust
// 내부적으로 컴파일러가 아래처럼 만든다 (예시)
fn add_i32(a: i32, b: i32) -> i32 { a + b }
fn add_f64(a: f64, b: f64) -> f64 { a + b }
```

결과적으로 generic 함수는 런타임 오버헤드 없이 컴파일 타임에 구체화된다.

---

## 예시 3: Trait 객체 vs 제네릭

Trait을 사용할 때 두 방식이 있다.

### Trait 객체 (dynamic dispatch)

```rust
trait Animal {
    fn speak(&self);
}

fn make_speak(a: &dyn Animal) {
    a.speak(); // vtable을 통한 동적 호출
}
```

이 경우에는 런타임에 vtable을 통해 호출되므로 **zero-cost는 아니다.**

### 제네릭 (static dispatch)

```dts
fn make_speak<T: Animal>(a: &T) {
    a.speak(); // 컴파일 타임에 결정
}
```

이 경우는 정적으로 호출될 함수가 결정되므로 **zero-cost abstraction**이다.

##

## 핵심 요약

기능 추상화 방식 비용

<div class="table-responsive tistory-table">
<table>
<tbody>
<tr>
<td>Iterators</td>
<td>Zero-cost</td>
</tr>
<tr>
<td>Generics</td>
<td>Zero-cost</td>
</tr>
<tr>
<td>Trait Object - dynamic dispatch</td>
<td>비용 있음</td>
</tr>
</tbody>
</table>
</div>

##

## 마무리

Rust의 zero-cost abstraction은 **성능을 포기하지 않고도 추상화된 코드를 작성할 수 있게 해준다.** 이는 성능이 중요한 시스템 프로그래밍에서도 안전성과 유지보수성을 모두 만족시키는 데 핵심 역할을 한다.

Rust로 코딩할 때 우리는 추상화와 성능 사이에서 **양자택일이 아닌, 둘 다를 취할 수 있다.**
