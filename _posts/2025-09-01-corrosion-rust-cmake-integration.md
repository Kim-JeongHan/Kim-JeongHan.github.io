---
layout: post
title: 'Corrosion : Rust와 CMake의 통합'
date: 2025-09-01 16:32:37 +0900
slug: corrosion-rust-cmake-integration
render_with_liquid: false
categories:
- 프로그래밍
- Rust
tags:
- Cargo
- CMAKE
- corrosion
- rust
last_modified_at: 2025-09-01 20:54:06 +0900
source:
  provider: tistory
  id: 63
---

## 소개

현대 로보틱스와 임베디드 커널 시스템에서는 C, C++, Python과 같은 언어가 주로 사용된다. 최근 각광받는 Rust는 메모리 안전성과 동시성에서 강점을 보이지만, 기존의 대규모 소프트웨어 스택(ROS, 시뮬레이터, 미들웨어 등)은 대부분 CMake 기반의 C/C++로 작성되어 있다. 이러한 상황에서 Rust를 기존 CMake 기반 프로젝트에 손쉽게 통합할 수 있도록 도와주는 도구가 바로 **Corrosion**이다. 이 도구는 원래 cmake-cargo라는 이름으로 시작되었다.

## 필요성

Rust 코드를 C++ 프로젝트에 통합하려면 다음과 같은 작업이 필요하다.

- cargo로 빌드한 .a 또는 .so 라이브러리를 CMake에 직접 등록
- 빌드 설정(cargo target, linker 옵션 등)을 CMake 설정과 일치
- 크로스 컴파일 및 멀티플랫폼 지원을 위한 복잡한 스크립트 관리

이 과정은 번거롭고 오류가 발생하기 쉽다. Corrosion은 이러한 과정을 자동화하여 Rust와 CMake 빌드를 통합해 주며, 개발자가 두 환경을 원활하게 함께 활용할 수 있도록 지원한다.

## 주요 기능

- **자동 라이브러리/실행 파일 가져오기**: Rust Crate의 Cargo.toml을 읽어 CMake 타겟으로 변환
- **실행 파일 설치 지원**: Rust 실행 파일을 CMake의 install 프로세스에 쉽게 통합
- **C++ ↔ Rust 링크 연동**: C++에서 Rust 라이브러리를 직접 링크 가능
- **멀티-Config 지원**: Debug/Release 등 CMake 빌드 설정을 그대로 Rust 빌드에 적용
- **크로스 컴파일 단순화**: 타겟 아키텍처 지정 및 플랫폼 빌드를 손쉽게 처리
- **FetchContent 연동**: 외부 프로젝트 의존성처럼 쉽게 가져와 사용 가능

## 방법

#### 파일 구조

```crystal
├── CMakeLists.txt
├── include
│   └── rust_math_interface.h
├── rust_math
│   ├── Cargo.lock
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
└── src
    └── main.cpp
```

CmakeLists.txt내용

```python
cmake_minimum_required(VERSION 3.15)
project(rust_cmake_integration)

# C++ standard configuration
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Fetch Corrosion using FetchContent
include(FetchContent)

FetchContent_Declare(
    Corrosion
    GIT_REPOSITORY https://github.com/corrosion-rs/corrosion.git
    GIT_TAG v0.4.7
)
FetchContent_MakeAvailable(Corrosion)

# Import Rust crate using Corrosion
corrosion_import_crate(MANIFEST_PATH rust_math/Cargo.toml)

# Include directory configuration
include_directories(include)

# Create C++ executable
add_executable(math_calculator
  src/main.cpp
)

# Link with Rust library (Corrosion automatically handles everything)
target_link_libraries(math_calculator
  rust_math_lib  # Target automatically created by Corrosion
)

# Installation configuration
install(TARGETS math_calculator
  RUNTIME DESTINATION bin
)
```

lib.rs

```bash
use std::os::raw::c_int;

/// Calculate the nth Fibonacci number
#[no_mangle]
pub extern "C" fn fibonacci(n: c_int) -> c_int {
    if n <= 1 {
        return n;
    }
    
    let mut a = 0;
    let mut b = 1;
    
    for _ in 2..=n {
        let temp = a + b;
        a = b;
        b = temp;
    }
    
    b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fibonacci() {
        assert_eq!(fibonacci(0), 0);
        assert_eq!(fibonacci(1), 1);
        assert_eq!(fibonacci(10), 55);
    }
}
```

cargo.toml

```bash
[package]
name = "rust_math_lib"
version = "0.1.0"
edition = "2021"

# Build as C-compatible library
[lib]
crate-type = ["cdylib", "staticlib"]

[dependencies]
# Example dependency for math operations
num-traits = "0.2"

# Dependency for C FFI
libc = "0.2"

[profile.release]
# Optimization settings
opt-level = 3
lto = true
codegen-units = 1
```

rust_math_interface.h

```bash
#ifndef RUST_MATH_INTERFACE_H
#define RUST_MATH_INTERFACE_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Calculate the nth value of Fibonacci sequence
 * @param n Index (starting from 0)
 * @return nth Fibonacci number
 */
int fibonacci(int n);

#ifdef __cplusplus
}
#endif

#endif // RUST_MATH_INTERFACE_H
```

main.cpp

```cpp
#include <iostream>
#include "rust_math_interface.h"

int main() {
    std::cout << "=== Rust-CMake Integration Example ===\n\n";

    // Fibonacci sequence test
    std::cout << "Fibonacci Sequence (first 15 numbers):\n";
    std::cout << "   ";
    for (int i = 0; i < 15; ++i) {
        int fib = fibonacci(i);
        std::cout << fib;
        if (i < 14) std::cout << ", ";
    }
    std::cout << "\n\n";

    // Individual Fibonacci calculations
    std::cout << "Individual Fibonacci calculations:\n";
    int test_values[] = {5, 10, 15, 20};
    for (int n : test_values) {
        int result = fibonacci(n);
        std::cout << "   fibonacci(" << n << ") = " << result << "\n";
    }

    std::cout << "\n=== Test Completed! ===\n";
    return 0;
}
```

### 결과

```bash
=== Rust-CMake Integration Example ===

Fibonacci Sequence (first 15 numbers):
   0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377

Individual Fibonacci calculations:
   fibonacci(5) = 5
   fibonacci(10) = 55
   fibonacci(15) = 610
   fibonacci(20) = 6765

=== Test Completed! ===
```

관련 github 링크 참조

[https://github.com/Kim-JeongHan/rust_make_integration](https://github.com/Kim-JeongHan/rust_make_integration)
