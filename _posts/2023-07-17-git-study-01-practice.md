---
layout: post
title: "[Git 스터디 1-2] 저장소 만들기와 기본 실습"
slug: git-study-01-practice
subtitle: "git init, clone, add, commit, rm, mv 실습"
date: 2023-07-17 21:00:00 +0900
last_modified_at: 2023-07-16 15:16:00 +0900
categories:
  - 프로그래밍
  - Git
tags:
  - Git
  - GitHub
  - version-control
  - git-study
series: git-study
series_order: 2
render_with_liquid: false
---

Git 저장소를 쓰는 방법은 보통 두 가지다.

1. 아직 버전관리를 하지 않는 로컬 디렉토리에 Git 저장소를 적용한다.
2. 다른 곳에 있는 Git 저장소를 `clone`한다.

둘 다 실습해보는 것이 좋다. 단, 같은 디렉토리에서 섞어 하지 말고 하나를 끝낸 뒤 새 디렉토리에서 다음 실습을 하는 편이 깔끔하다.

## 기존 디렉토리를 Git 저장소로 만들기

기존 프로젝트를 Git으로 관리하려면 프로젝트 디렉토리로 이동한 뒤 `git init`을 실행한다.

```bash
$ git init
```

`git add`를 하려면 디렉토리 안에 하나 이상의 파일이 있어야 한다. 예를 들어 파일을 하나 만든 뒤 staging area에 올리고 커밋한다.

```bash
$ echo "hello git" > README.md
$ git add README.md
$ git commit -m "initial project version"
```

모든 변경 파일을 한 번에 올리고 싶으면 `git add .`을 사용할 수 있다.

```bash
$ git add .
$ git commit -m "initial project version"
```

`git add <file>`은 특정 파일만 staging area에 올리고, `git add .`은 현재 디렉토리 아래의 변경을 한 번에 올린다.

## 기존 저장소 clone하기

다른 프로젝트에 참여하거나 저장소를 복사하고 싶을 때는 `git clone`을 쓴다. `clone`을 실행하면 파일뿐 아니라 프로젝트 히스토리도 함께 받아온다.

```bash
$ git clone https://github.com/Kim-JeongHan/start_git.git
```

clone 이후에는 새 디렉토리가 만들어지고, 그 안에 원격 저장소의 파일과 `.git` 디렉토리가 함께 들어온다.

## 상태 확인

작업 중에는 `git status`로 상태를 자주 확인한다.

```bash
$ git status
```

`git status`는 어떤 파일이 수정됐는지, 어떤 파일이 staged 상태인지, 아직 Git이 추적하지 않는 파일이 무엇인지 보여준다.

## 커밋 메시지 작성

커밋은 편집기를 열어서 메시지를 작성할 수도 있고, `-m` 옵션으로 바로 작성할 수도 있다.

```bash
$ git commit -m "first commit"
```

이미 Git이 추적 중인 파일만 수정했다면 `-a` 옵션으로 `git add`와 비슷한 처리를 함께 할 수 있다.

```bash
$ git commit -a -m "first commit"
```

주의할 점은 `git commit -a`가 한 번도 추적되지 않은 새 파일까지 자동으로 올려주지는 않는다는 것이다. 새 파일은 여전히 `git add`가 필요하다.

## 파일 삭제하기

Git이 추적 중인 파일을 삭제할 때는 `git rm`을 사용할 수 있다.

```bash
$ git rm CONTRIBUTING.md
$ git commit -m "remove contributing guide"
```

이 명령은 working tree의 실제 파일도 함께 삭제한다. 파일은 남기고 staging area에서만 빼고 싶다면 `--cached`를 쓴다.

```bash
$ git rm --cached CONTRIBUTING.md
```

## 파일 이름 변경하기

Git은 파일 이름 변경 자체를 별도 메타데이터로 저장하지 않는다. 그래도 `git mv`를 쓰면 이름 변경 의도를 명확하게 표현할 수 있다.

```bash
$ echo "file name change" > mv_file.md
$ git add .
$ git commit -m "add file before rename"
$ git mv mv_file.md mv_file_2.md
$ git commit -m "rename file"
```

`git mv`를 쓰지 않으면 일반 `mv`, `git rm`, `git add`를 조합해도 같은 결과를 만들 수 있다.

```bash
$ mv mv_file_2.md mv_file.md
$ git rm mv_file_2.md
$ git add mv_file.md
```

핵심은 working tree에서 파일을 바꾼 뒤 staging area에 올리고, 커밋으로 저장소에 확정한다는 흐름이다.
