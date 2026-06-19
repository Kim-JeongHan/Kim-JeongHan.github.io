---
layout: post
title: "[Git 스터디 3-2] GitHub 사용"
slug: git-study-03-github
subtitle: "Personal access token, repository 생성, remote push"
date: 2023-07-19 20:00:00 +0900
last_modified_at: 2023-07-16 15:16:00 +0900
categories:
  - 프로그래밍
  - Git
tags:
  - Git
  - GitHub
  - git-study
series: git-study
series_order: 6
render_with_liquid: false
---

이 글은 Git 스터디의 GitHub 사용 실습을 정리한 것이다. GitHub UI는 바뀔 수 있으므로, 큰 흐름을 중심으로 본다.

## Personal access token 만들기

GitHub에서 HTTPS로 push할 때 비밀번호 대신 Personal access token을 사용할 수 있다.

기본 흐름은 다음과 같다.

1. GitHub에 로그인한다.
2. 우측 상단 프로필 메뉴에서 `Settings`로 들어간다.
3. 왼쪽 메뉴 하단의 `Developer settings`로 들어간다.
4. `Personal access tokens` 메뉴를 선택한다.
5. 새 토큰 생성을 누른다.
6. 토큰 이름을 알아보기 쉽게 지정한다.
7. 만료 기간을 설정한다.
8. 필요한 권한만 선택한다. 실습에서는 보통 저장소 접근 권한이 필요하다.
9. 토큰을 생성한다.
10. 생성된 토큰을 복사해 로그인 또는 push 인증에 사용한다.

토큰은 생성 직후 한 번만 제대로 볼 수 있으므로 안전한 곳에 보관해야 한다. 재발급하면 기존 토큰으로 로그인해 둔 환경은 다시 인증해야 한다.

## Repository 만들기

GitHub에서 새 저장소를 만드는 절차는 다음과 같다.

1. 우측 상단의 `+` 버튼을 누르고 `New repository`를 선택한다.
2. repository 이름을 정한다. 예시에서는 `start_git`을 사용한다.
3. 필요한 공개 범위와 옵션을 선택한다.
4. `Create repository`를 눌러 저장소를 만든다.

저장소를 만든 뒤 HTTPS URL을 복사해둔다.

## 로컬 저장소를 GitHub에 push하기

로컬에서 실습용 디렉토리를 만든다.

```bash
$ cd
$ rm -rf start_git
$ mkdir start_git
$ cd start_git
$ echo "hi git" > README.md
```

이제 지난 실습처럼 Git 저장소를 만들고 첫 커밋을 만든다.

```bash
$ git init
$ git add README.md
$ git commit -m "first commit"
```

GitHub에서 만든 repository의 HTTPS URL을 remote로 추가한다.

```bash
$ git remote add origin https://github.com/<user>/<repository>.git
```

그리고 push한다.

```bash
$ git push -u origin master
```

기본 브랜치 이름이 `main`이라면 다음처럼 push한다.

```bash
$ git branch -M main
$ git push -u origin main
```

push가 끝나면 GitHub repository 페이지에서 파일이 올라갔는지 확인한다.

## 다른 사람과 협업하기

GitHub 협업은 단순히 코드를 올리는 것에서 끝나지 않는다. 일반적으로는 다음 흐름을 가진다.

- remote 저장소를 기준으로 코드를 공유한다.
- 작업자는 각자 branch를 만들어 작업한다.
- 작업이 끝나면 push한다.
- 팀은 pull request 또는 merge request로 변경 내용을 검토한다.
- 검토와 테스트가 끝난 변경만 기준 브랜치에 merge한다.

초기 실습에서는 remote를 등록하고 push하는 것만 익혀도 충분하다. 이후에는 branch 전략과 pull request 흐름을 함께 익히면 된다.

## References

- [GitHub Docs: Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub 토큰 사용 참고 자료](https://wiznxt.tistory.com/873)
