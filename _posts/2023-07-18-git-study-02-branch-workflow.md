---
layout: post
title: "[Git 스터디 2-2] 브랜치 활용과 병합"
slug: git-study-02-branch-workflow
subtitle: "작업 브랜치, hotfix, fast-forward merge, conflict 처리"
date: 2023-07-18 21:00:00 +0900
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
series_order: 4
source:
  provider: notion
  page_id: 4bb89340-1893-49d3-9981-5b4501f53201
  project_id: 2fa9e30d-1d04-489c-a612-db1add10d0c0
render_with_liquid: false
---

브랜치와 merge는 실제 개발 중 아래 흐름으로 자주 사용된다.

1. 웹사이트나 소프트웨어가 있고, 기존 작업을 진행하고 있다.
2. 새로운 이슈를 처리할 브랜치를 만든다.
3. 그 브랜치에서 작업을 진행한다.
4. 중간에 긴급 문제가 생기면 hotfix 브랜치를 만들어 먼저 처리한다.
5. hotfix를 운영 브랜치에 merge한다.
6. 다시 원래 작업 브랜치로 돌아와 하던 일을 계속한다.

## 작업 브랜치 만들기

예제 저장소를 clone하고 이슈 처리를 위한 브랜치를 만든다.

```bash
$ git clone https://github.com/jeong-han-kim/start_git
$ git checkout -b iss53
```

`git checkout -b iss53`은 브랜치를 만들고 바로 그 브랜치로 이동한다.

```bash
$ echo 'hello' > iss53_project
$ git add .
$ git commit -m "edit issue 1"
```

## Hotfix 브랜치

작업 중 급한 문제가 생기면 다시 운영 브랜치로 돌아가 hotfix 브랜치를 만든다.

```bash
$ git checkout master
$ git checkout -b hotfix
$ echo 'problem' > speed_problem
$ git add .
$ git commit -m "fixed problem"
```

hotfix를 master에 merge한다.

```bash
$ git checkout master
$ git merge hotfix
```

현재 master가 hotfix의 조상 커밋이면 Git은 fast-forward merge를 수행한다. 이 경우 별도의 merge commit 없이 master 포인터만 앞으로 이동한다.

처리가 끝난 hotfix 브랜치는 삭제할 수 있다.

```bash
$ git branch -d hotfix
```

## Conflict 처리

서로 다른 브랜치에서 같은 파일의 같은 부분을 수정하면 merge conflict가 날 수 있다.

```bash
$ git clone https://github.com/Kim-JeongHan/merge_start
$ git checkout issue1
$ git log --graph
```

master에서 `issue1`을 merge해본다.

```bash
$ git checkout master
$ git merge issue1
자동 병합: motorB
충돌! (내용): motorB에 병합 충돌
자동 병합이 실패했습니다. 충돌을 바로잡고 결과물을 커밋하십시오.
```

충돌이 나면 `git status`로 어떤 파일을 고쳐야 하는지 확인한다.

```bash
$ git status
```

충돌 파일 안에는 다음과 같은 표시가 생긴다.

```text
 <<<<<<< HEAD
editing

## 고생많아요 다들
 =======
editing 2
 >>>>>>> issue1
```

`<<<<<<<`, `=======`, `>>>>>>>` 사이의 내용을 보고 최종으로 남길 내용을 직접 정리한다. 수정이 끝나면 다시 add와 commit으로 merge를 마무리한다.

```bash
$ git add .
$ git commit -m "finish issue1"
```

작업 브랜치가 더 필요 없으면 삭제한다.

```bash
$ git branch -d issue1
```

## 브랜치 상태 확인

이미 현재 브랜치에 merge된 브랜치는 다음으로 확인할 수 있다.

```bash
$ git branch --merged
  iss53
* master
```

아직 merge되지 않은 브랜치는 다음으로 확인한다.

```bash
$ git branch --no-merged
```

merge된 브랜치는 보통 삭제해도 된다. 반대로 merge되지 않은 브랜치를 `-d`로 삭제하려 하면 Git이 막는다.

```bash
$ git branch -d issue1
```

정말 버려도 되는 브랜치라면 강제 삭제 옵션을 쓴다.

```bash
$ git branch -D issue1
```

강제 삭제는 커밋을 잃을 수 있으므로, 실습용이 아닌 실제 프로젝트에서는 삭제 전에 로그와 merge 여부를 확인해야 한다.

## References

- [Pro Git: 리모트 브랜치](https://git-scm.com/book/ko/v2/Git-%EB%B8%8C%EB%9E%9C%EC%B9%98-%EB%A6%AC%EB%AA%A8%ED%8A%B8-%EB%B8%8C%EB%9E%9C%EC%B9%98)
- [Pro Git: Rebase 하기](https://git-scm.com/book/ko/v2/Git-%EB%B8%8C%EB%9E%9C%EC%B9%98-Rebase-%ED%95%98%EA%B8%B0)
- [Pro Git: Reset 명확히 알고 가기](https://git-scm.com/book/ko/v2/Git-%EB%8F%84%EA%B5%AC-Reset-%EB%AA%85%ED%99%95%ED%9E%88-%EC%95%8C%EA%B3%A0-%EA%B0%80%EA%B8%B0)
