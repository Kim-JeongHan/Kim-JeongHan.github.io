---
layout: post
title: 'Rust-C++ 통합 : cbindgen과 Collision을 활용한 workflow'
date: 2025-09-02 22:49:56 +0900
slug: rust-cpp-cbindgen-collision-workflow
render_with_liquid: false
categories:
- 프로그래밍
- Rust
tags:
- C++
- cbindgen
- CMAKE
- corrosion
- rust
last_modified_at: 2025-09-02 22:59:21 +0900
imported_images:
- assets/img/tistory/68/image-001.png
source:
  provider: tistory
  id: 68
---

이 글에서는 **cbindgen**과 **Corrosion**을 활용해 Rust와 C++를 매끄럽게 통합하는 워크플로우를 소개한다.

앞서 다루었던 cbindgen -> corrision -> 통합 과정으로 설명을 진행한다.

### cbindgen이란?

**cbindgen**은 Rust 라이브러리의 public C API를 분석해 자동으로 C 또는 C++11 헤더 파일을 생성하는 도구이다. Rust 팀과 협력해 개발된 만큼 Rust의 타입 레이아웃과 ABI를 정확히 보장한다.

### 설치 및 사용법

```sql
cargo install --force cbindgen
```

```brainfuck
cbindgen --config cbindgen.toml --crate my_rust_library --output my_header.h
```

참고자료 : [관련 글](/blog/2025/cbindgen-rust-cpp-header-generator/)


### Corrosion의 필요성

Rust 코드를 CMake 기반 C++ 프로젝트에 통합하려면 보통 다음과 같은 작업이 필요하다.

- cargo로 빌드한 라이브러리를 CMake에 수동 등록
- 빌드 설정(Debug/Release 등) 동기화
- 복잡한 링킹 스크립트 관리

**Corrosion**은 이 과정을 자동화해 Rust와 CMake를 원활히 연결해준다.

### 주요 기능

- **자동 타겟 생성**: Cargo.toml을 읽어 CMake 타겟으로 변환
- **빌드 설정 연동**: CMake의 Debug/Release 설정을 Rust 빌드에 자동 적용
- **크로스 컴파일 지원**: 아키텍처 지정 및 플랫폼 빌드 단순화
- **FetchContent 연동**: 외부 의존성처럼 쉽게 추가 가능

참고자료 : [관련 글](/blog/2025/corrosion-rust-cmake-integration/)


## 통합 워크플로우 템플릿

cbindgen과 Corrosion을 함께 사용하면 Rust-C++ 통합 환경을 좀더 쉽게 만들 수 있다.

### 프로젝트 구조

![](/assets/img/tistory/68/image-001.png)

### 주요 구성 요소

- **Rust 라이브러리(lib.rs)**: FFI 함수 정의
- **cbindgen.toml**: 헤더 생성 설정
- **CMakeLists.txt**: Corrosion으로 Rust crate 통합, cbindgen으로 헤더 자동 생성
- **build.sh**: 빌드 및 실행 자동화

### 빌드 및 실행

```dts
./scripts/build.sh Debug   # Debug 모드
./scripts/build.sh         # Release 모드
./build/bin/cpp_example    # 실행
```

**출력 예시**

```basic
15 + 27: 42
5!: 120
```

## CMakeLists.txt

```bash
cmake_minimum_required(VERSION 3.15)
project(rust_cmake_template)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set Rust environment variables
set(ENV{PATH} "$ENV{HOME}/.cargo/bin:$ENV{PATH}")

# Find Rust tools with absolute paths
find_program(CARGO_EXECUTABLE cargo
    PATHS $ENV{HOME}/.cargo/bin
    NO_DEFAULT_PATH
    REQUIRED)
find_program(RUSTC_EXECUTABLE rustc
    PATHS $ENV{HOME}/.cargo/bin
    NO_DEFAULT_PATH
    REQUIRED)

# Set Rust toolchain for Corrosion
set(Rust_TOOLCHAIN "stable-x86_64-unknown-linux-gnu")
set(Rust_COMPILER ${RUSTC_EXECUTABLE})
set(Rust_CARGO ${CARGO_EXECUTABLE})
set(Rust_CARGO_TARGET_DIR ${CMAKE_CURRENT_SOURCE_DIR}/rust_lib/target)

message(STATUS "Found Cargo: ${CARGO_EXECUTABLE}")
message(STATUS "Found Rustc: ${RUSTC_EXECUTABLE}")
message(STATUS "Rust Toolchain: ${Rust_TOOLCHAIN}")

include(FetchContent)
FetchContent_Declare(
    Corrosion
    GIT_REPOSITORY https://github.com/corrosion-rs/corrosion.git
    GIT_TAG v0.3.5
    GIT_SHALLOW ON
)
FetchContent_MakeAvailable(Corrosion)

corrosion_import_crate(
    MANIFEST_PATH rust_lib/Cargo.toml
    CRATES rust_math_lib
)

# Set up header generation with cbindgen
set(RUST_HEADER_DIR ${CMAKE_CURRENT_BINARY_DIR}/include)
set(RUST_HEADER_FILE ${RUST_HEADER_DIR}/rust_math_lib.h)
set(RUST_LIB_DIR ${CMAKE_CURRENT_SOURCE_DIR}/rust_lib)

# Find cbindgen executable
find_program(CBINDGEN_EXECUTABLE cbindgen
    PATHS $ENV{HOME}/.cargo/bin
    REQUIRED)

# Custom command to generate C header using cbindgen
add_custom_command(
    OUTPUT ${RUST_HEADER_FILE}
    COMMAND ${CBINDGEN_EXECUTABLE}
        --config ${RUST_LIB_DIR}/cbindgen.toml
        --crate rust_math_lib
        --output ${RUST_HEADER_FILE}
    WORKING_DIRECTORY ${RUST_LIB_DIR}
    DEPENDS ${RUST_LIB_DIR}/src/lib.rs ${RUST_LIB_DIR}/cbindgen.toml
    COMMENT "Generating C header with cbindgen"
    VERBATIM
)

# Custom target for header generation
add_custom_target(generate_rust_header
    DEPENDS ${RUST_HEADER_FILE}
)

include_directories(${RUST_HEADER_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
add_executable(cpp_example src/main.cpp)
target_link_libraries(cpp_example rust_math_lib)
add_dependencies(cpp_example generate_rust_header)

set_target_properties(cpp_example PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)
```

해당 CmakeLists.txt는 add_custom_target과 add_custom_command를 활용하여, cbindgen을 연결하였고, 기존 Corrision을 사용하여, Cmake에서 rust 빌드를 쉽게 사용할 수 있게 만들었다.

[https://github.com/Kim-JeongHan/rust_cmake_template](https://github.com/Kim-JeongHan/rust_cmake_template)

[GitHub - Kim-JeongHan/rust_cmake_template
Contribute to Kim-JeongHan/rust_cmake_template development by creating an account on GitHub.
github.com](https://github.com/Kim-JeongHan/rust_cmake_template)

위 github링크에서 사용할 수 있다.
