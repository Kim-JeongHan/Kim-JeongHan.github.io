# Repository instructions

이 저장소는 Jekyll/al-folio 기반 GitHub Pages 블로그다. 사용자 지시가 항상 이 규칙보다 우선한다.

## Scope and preservation

- 작업은 요청한 파일과 범위에 한정하고, 기존 문체, 구조, 사용자 변경을 보존한다.
- 포스트는 `_posts/YYYY-MM-DD-title.md` 형식을 따르며, 관련 없는 문단을 임의로 크게 고치지 않는다.
- `date:`가 있으면 그 값을 발행일로 사용하고, 없으면 Git 최초 commit 시각, Git 기록이 없으면 파일 수정 시각을 사용한다.

## Content conventions

- 수식 포스트에는 `use_math: true`를 둔다. 인라인은 `$...$`, 독립 수식은 `$$...$$`를 사용한다.
- 포스트 본문에는 `\(...\)`, `\[...\]`, `\coloneqq`를 쓰지 않는다. 정의에는 `=` 또는 `\mathrel{:=}`를 사용한다. (이 지침 문서에서는 금지 예시로 표기할 수 있다.)
- Liquid는 `render_with_liquid: false`를 기본으로 하고, include가 필요한 글만 `true`로 둔다.
- 알고리즘은 `algorithm.html`의 `math=` 입력을 사용하고, 한 컬럼 `array`, `\quad\quad` 들여쓰기, 빈 행 없는 흐름, 모바일을 고려한 짧은 줄을 지킨다.
- 알고리즘 설명 문장은 `\text{...}` 안에 두고, `&` 정렬은 Input/Output처럼 꼭 필요한 경우에만 사용한다.
- callout은 `callout.html`의 `note`, `idea`, `warning`, `quote`, `danger` 중 하나를 사용하며, Markdown/수식 본문은 `capture` 후 `content=`로 전달한다.

## Images and structure

- 이미지는 `_posts`에 두지 않고 `assets/img/blog/<post-slug>/`에 둔다. 본문 경로는 `/assets/img/blog/...` 절대 경로를 쓴다.
- 이미지 파일명은 의미를 알 수 있는 영문으로 하고, 뜻이 분명한 한국어 `alt`를 쓴다. 본문이나 캡션에서 색상, 기호, 화살표, 영역의 의미를 설명한다.
- 강화학습 글 제목은 `Reinforcement Learning N - 큰 주제`, 큰 목차는 `## 00_`, `## 01_` 형식을 따른다.
- 기존 제목과 목차 번호는 임의로 재정렬하지 않고, 내부 링크는 실제 URL을 확인한다.
- 강화학습 Markdown 표에는 `{: .policy-comparison-table}`를 붙이고, 독립 글에 임의의 강의 번호나 series metadata를 만들지 않는다.
- 작성 문서에는 Unicode 중간점을 쓰지 않고 나열에는 쉼표를 사용한다.
- 과학적 주장은 조건과 예외를 함께 쓰며, 논문, 공식 문서, 공식 구현 등 1차 자료를 우선 확인한다.
- source 검사에는 `git diff --check`, 금지 수식/중간점 검색, 이미지 경로 확인, 삭제, 이동 asset 참조 확인을 포함한다.
- 추적되지 않은 파일은 일반 `git diff`에서 빠질 수 있으므로 내용과 `git status`를 직접 확인한다.
- 전체 Jekyll 빌드, `start.sh`, Playwright 검증은 사용자가 명시적으로 요청한 경우에만 실행한다.
- 삭제 전 정확한 경로와 참조를 확인하고, 가능하면 영구 삭제 대신 휴지통으로 이동한 뒤 삭제 내용과 복구 가능 여부를 보고한다.

블로그 작업 전에는 [blog-writing-workflow.md](.agents/blog-writing-workflow.md)를 읽는다. 수식, include, 이미지 예시가 필요할 때만 [AGENT.md](AGENT.md)를 참고한다.
