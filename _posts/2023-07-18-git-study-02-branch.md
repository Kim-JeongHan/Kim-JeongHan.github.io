---
layout: post
title: "[Git 스터디 2-1] 브랜치의 원리"
slug: git-study-02-branch
subtitle: "Git의 스냅샷 저장 방식과 브랜치 포인터 이해"
date: 2023-07-18 20:00:00 +0900
last_modified_at: 2023-07-16 15:16:00 +0900
categories:
  - 프로그래밍
  - Git
tags:
  - Git
  - branch
  - merge
  - git-study
series: git-study
series_order: 3
render_with_liquid: false
---

브랜치를 이해하려면 먼저 Git이 데이터를 어떻게 기록하는지 알아야 한다.

## Git의 데이터 기록

Git은 파일의 변경 사항만 줄 단위로 저장하는 방식이 아니라, 특정 순간의 스냅샷을 저장하는 방식에 가깝다. 커밋을 만들면 Git은 staging area에 있는 데이터의 스냅샷을 만들고, 그 스냅샷을 가리키는 커밋 객체를 저장한다.

커밋 객체에는 다음 정보가 들어간다.

- 루트 트리 객체를 가리키는 포인터
- 작성자와 커밋 메시지 같은 메타데이터
- 이전 커밋을 가리키는 포인터

예를 들어 세 개의 파일을 만들고 커밋해보자.

```bash
$ mkdir new
$ cd new
$ echo 'A' > A
$ echo 'B' > B
$ echo 'C' > C
$ git init
$ git add A B C
$ git commit -m 'The initial commit of my project'
```

이 커밋은 단순히 "A, B, C가 바뀌었다"만 저장하는 것이 아니라, 현재 디렉토리 구조를 트리 객체로 기록하고 그 루트 트리를 커밋 객체가 가리키게 만든다. 이후 커밋은 이전 커밋을 가리키는 포인터를 갖기 때문에 히스토리가 연결된다.

정리하면 `git commit`은 스냅샷을 기록하고, 그 스냅샷은 트리 구조로 관리된다. 커밋 객체는 그 트리 구조의 루트와 이전 커밋을 가리키는 포인터를 가진다.

## Git branch

Git의 브랜치는 커밋을 가리키는 가벼운 포인터다. `master` 또는 `main` 브랜치도 결국 특정 커밋을 가리키는 이름일 뿐이다.

새 브랜치를 만들면 새로운 포인터가 생긴다.

```bash
$ git branch testing
```

이 시점에서 `master`와 `testing`은 같은 커밋을 가리킬 수 있다. 현재 내가 어느 브랜치 위에서 작업 중인지는 `HEAD`가 가리킨다.

## 브랜치 이동

다른 브랜치로 이동하려면 `checkout`을 사용할 수 있다.

```bash
$ git checkout testing
```

이제 `HEAD`는 `testing` 브랜치를 가리킨다. 여기서 파일을 수정하고 커밋하면 `testing` 브랜치만 앞으로 이동한다.

```bash
$ echo 'AAA' > A
$ git commit -a -m 'made a change'
$ git log --oneline --decorate
ee8d035 (HEAD -> testing) made a change
fb8a72a (master) first commit
```

다시 `master` 브랜치로 돌아가면 working tree도 `master`가 가리키는 커밋 기준으로 바뀐다.

```bash
$ git checkout master
```

이 상태에서 다시 파일을 수정하고 커밋하면 `master`도 다른 방향으로 앞으로 이동할 수 있다.

```bash
$ echo 'BB' > B
$ git commit -a -m 'made other change'
$ git log --oneline --decorate --all
ee8d035 (testing) made a change
fb8a72a (HEAD -> master) made other change
```

현재 브랜치의 로그만 보면 다른 브랜치의 커밋이 보이지 않을 수 있다. 전체 브랜치를 보고 싶으면 `--all`을 붙인다.

```bash
$ git log --oneline --decorate --all
```

브랜치는 무거운 복사본이 아니라 커밋 포인터이므로 만들고 이동하는 비용이 작다. Git에서 브랜치를 자주 만들고 버리는 워크플로가 자연스러운 이유다.
