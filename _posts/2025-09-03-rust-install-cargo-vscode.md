---
layout: post
title: Rust설치, Cargo활용 및 유용한 확장(Vscode, IDE)
date: 2025-09-03 00:48:26 +0900
slug: rust-install-cargo-vscode
render_with_liquid: false
categories:
- 프로그래밍
- Rust
tags:
- Cargo
- rust
- vscode
last_modified_at: 2025-09-03 00:48:26 +0900
imported_images:
- assets/img/blog/rust-install-cargo-vscode/image-001.png
- assets/img/blog/rust-install-cargo-vscode/image-002.png
- assets/img/blog/rust-install-cargo-vscode/image-003.png
- assets/img/blog/rust-install-cargo-vscode/image-004.png
- assets/img/blog/rust-install-cargo-vscode/image-005.png
- assets/img/blog/rust-install-cargo-vscode/image-006.png
- assets/img/blog/rust-install-cargo-vscode/image-007.png
- assets/img/blog/rust-install-cargo-vscode/image-008.png
source:
  provider: tistory
  id: 69
---

## rust 설치하기

```vim
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

rust는 rustup이라는 패키지에 의해서 설치 된다. rust는 6주의 빠른 release process를 가지며, rustup은 이러한 rust를 모든 platform에서 cross compile을 지원한다.

기본적으로 rust는 ~/.cargo/bin 경로에 설치가 되며, Rust toolchain은 물론, rust, cargo, rustup은 모두 이안에 포함되어 있다.
따라서, Rust 개발자들은 PATH에 rustup path를 추가해야한다.

### path추가

```routeros
export PATH=$PATH:<경로>
# 만약 귀찮다면 해당 내용을 ~/.bashrc에 추가하면 편하게 사용이 가능하다.
```

### rust 업데이트 하기

```ebnf
rustup update
```

### rust 삭제하기

```armasm
rustup self uninstall
```

## rust 패키지 사용하기

rust의 패키지 매니저인 cargo는 굉장히 유용한 툴로써 사용가능하다.
cargo의 명령어를 간단히 소개한다.

### build(release/debug)

```mipsasm
cargo build --debug
cargo build --release
```

### main.rs 실행하기

```dockerfile
cargo run
```

### 테스트 코드 검증하기

```bash
cargo test
```

## vscode extension 사용하기

1. rust-analyzer

![](/assets/img/blog/rust-install-cargo-vscode/image-001.png)

정적 분석기이다. run을 vscode에서 쉽게 지원한다.

![](/assets/img/blog/rust-install-cargo-vscode/image-002.png)

에러 구문을 정적으로 분석하여 알려준다.

![](/assets/img/blog/rust-install-cargo-vscode/image-003.png)

run과 debug 버튼이 생겼다.
![](/assets/img/blog/rust-install-cargo-vscode/image-004.png)

에러 메세지

debug를 클릭하면 codeLLDB를 설치하라고 하는 에러가 발생하는데 codeLLDB를 설치하면 정상적으로 실행된다.

1. CodeLLDB

![](/assets/img/blog/rust-install-cargo-vscode/image-005.png)

설치 후 정상실행 모습을 확인 할 수 있다.

![](/assets/img/blog/rust-install-cargo-vscode/image-006.png)

1. Dependi

![](/assets/img/blog/rust-install-cargo-vscode/image-007.png)

Cargo.toml에서 패키지 버전 및 의존성을 효율적으로 관리할수 있게 도와준다.

![](/assets/img/blog/rust-install-cargo-vscode/image-008.png)
