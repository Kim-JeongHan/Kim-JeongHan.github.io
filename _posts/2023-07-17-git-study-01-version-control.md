---
layout: post
title: "[Git 스터디 1-1] 버전관리와 Git 기본 설정"
slug: git-study-01-version-control
subtitle: "분산 버전관리, Git의 세 가지 상태, 설치와 사용자 설정"
date: 2023-07-17 20:00:00 +0900
categories:
  - 프로그래밍
  - Git
tags:
  - Git
  - GitHub
  - version-control
  - git-study
series: git-study
series_order: 1
render_with_liquid: false
---

이 글은 Git 스터디 1일차 첫 번째 자료를 블로그용으로 정리한 것이다. 전체 흐름은 [Pro Git 한국어판](https://git-scm.com/book/ko/v2)을 기준으로 잡았다.

## 분산 버전관리 시스템

현재 우리가 사용하는 Git은 분산 버전관리 시스템(DVCS, Distributed Version Control System)이다. 분산 버전관리에서는 서버뿐 아니라 각 클라이언트에도 저장소의 버전 기록이 남는다.

이 구조의 장점은 단순 백업 이상의 의미가 있다. 서버에 문제가 생겨도 클라이언트의 복제본에서 복구할 수 있고, 여러 리모트 저장소를 두면서 팀, 그룹, 외부 협업자와 다양한 방식으로 작업할 수 있다. 중앙집중식 버전관리만으로는 만들기 어려운 워크플로가 가능해진다.

## Git의 파일 관리

Git은 파일을 크게 세 가지 상태로 본다.

- `Modified`: 파일을 수정했지만 아직 다음 커밋 대상으로 올리지 않은 상태
- `Staged`: 다음 커밋에 들어갈 스냅샷으로 표시한 상태
- `Committed`: 데이터가 로컬 저장소에 안전하게 기록된 상태

이 세 상태는 Git 프로젝트의 세 영역과 연결된다.

- `Git directory`: Git이 메타데이터와 객체 데이터베이스를 저장하는 곳이다. 저장소의 핵심이며, clone을 하면 이 영역이 함께 만들어진다.
- `Working tree`: 특정 버전을 checkout 해서 실제 파일로 펼쳐 놓은 작업 공간이다.
- `Staging area`: 다음 커밋에 들어갈 파일 정보를 저장하는 영역이다. Git에서는 `index`라고도 부른다.

기본 흐름은 단순하다.

1. 워킹 트리에서 파일을 수정한다.
2. `git add`로 수정 내용을 staging area에 올린다.
3. `git commit`으로 staging area의 내용을 Git directory에 영구 스냅샷으로 저장한다.

## Linux에서 Git 설치

Ubuntu 계열에서는 다음처럼 설치할 수 있다.

```bash
$ sudo apt install git-all
```

설치 후에는 버전을 확인한다.

```bash
$ git --version
```

## Git 설정 파일의 우선순위

Git 설정은 여러 위치에 저장될 수 있다.

- `/etc/gitconfig`: 시스템 전체에 적용되는 설정
- `~/.gitconfig` 또는 `~/.config/git/config`: 현재 사용자에게 적용되는 설정
- `.git/config`: 현재 저장소에만 적용되는 설정

설정은 더 좁은 범위가 더 높은 우선순위를 갖는다. 예를 들어 현재 저장소의 `.git/config`는 사용자 전역 설정인 `~/.gitconfig`보다 우선한다.

## 사용자 정보 입력

Git을 설치한 뒤 가장 먼저 해야 할 일은 사용자 이름과 이메일 주소를 설정하는 것이다. Git은 커밋할 때 이 정보를 사용한다.

```bash
$ git config --global user.name "John Doe"
$ git config --global user.email johndoe@example.com
```

`--global` 옵션은 현재 사용자 전체에 적용한다는 뜻이다. 프로젝트마다 다른 이름이나 이메일을 쓰고 싶다면 해당 저장소 안에서 `--global`을 빼고 실행하면 된다.

설정은 다음 명령으로 확인한다.

```bash
$ git config --list
user.name=John Doe
user.email=johndoe@example.com
color.status=auto
color.branch=auto
color.interactive=auto
color.diff=auto
...
```

## 도움말 보기

Git 명령어가 헷갈릴 때는 내장 도움말을 먼저 확인한다.

```bash
$ git help <verb>
```

예를 들어 `config` 명령이 궁금하면 다음처럼 볼 수 있다.

```bash
$ git help config
```

명령 옵션만 빠르게 확인하고 싶을 때는 `-h`를 붙인다.

```bash
$ git add -h
usage: git add [<options>] [--] <pathspec>...

    -n, --dry-run         dry run
    -v, --verbose         be verbose
    -i, --interactive     interactive picking
    -p, --patch           select hunks interactively
    -A, --all             add changes from all tracked and untracked files
```

Git은 명령이 많지만, 처음에는 `config`, `init`, `clone`, `status`, `add`, `commit`, `log` 정도만 익혀도 실습을 시작할 수 있다.

## References

- [Pro Git 한국어판](https://git-scm.com/book/ko/v2)
