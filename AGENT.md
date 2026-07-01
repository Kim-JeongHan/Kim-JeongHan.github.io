# Agent Notes

이 저장소는 Jekyll/al-folio 기반 GitHub Pages 블로그이다. 블로그 글을 수정할 때는 기존 포스트의 문체와 구조를 우선 따른다.

## Post Editing

- 논문 리뷰나 개념 글은 `_posts/YYYY-MM-DD-title.md` 형식으로 작성한다.
- 포스트의 `date:` front matter가 있으면 그 값을 발행일로 사용한다. `date:`가 없는 포스트는 빌드 시 Git 최초 commit 시각을 자동 발행일로 사용하며, Git 기록이 없는 새 파일은 파일 수정 시각을 fallback으로 사용한다.
- 수식이 필요한 글은 front matter에 `use_math: true`를 둔다.
- Liquid include가 필요한 글만 `render_with_liquid: true`로 둔다. 일반 논문 리뷰처럼 수식이 많은 글은 기본적으로 `render_with_liquid: false`가 안전하다.
- 사용자가 작성 중인 문장은 요청받은 부분만 다듬고, 관련 없는 문단은 임의로 크게 고치지 않는다.
- 이미지 원본을 `_posts`에 두지 않는다. 블로그 이미지로 사용할 파일은 `assets/img/blog/<post-slug>/` 아래로 옮기고, 본문에서는 절대 경로 `/assets/img/blog/...`를 사용한다.

## Math And Algorithm Blocks

- 일반 수식은 display math로 작성한다.

```latex
$$
Q(s, a)
=
\frac{W(s, a)}{N(s, a)}
$$
```

- 알고리즘을 LaTeX로 표현할 때는 `algorithm.html` include의 `math=` 입력을 사용한다.

```liquid
{% capture algorithm_name %}
$$
\begin{array}{l}
\textbf{Input : } \text{state } s \in \mathcal{S} \\
\textbf{Output : } \text{expanded state } s' \\[1mm]
\textbf{if } s\ \text{is not fully expanded}\ \textbf{then} \\
\quad\quad \text{Randomly select an untried action } a\ \text{to apply in } s \\
\quad\quad \text{Expand one outcome } s'\ \text{according to } P_a(s' \mid s) \\
\quad\quad \text{Observe reward } r \\[1mm]
\textbf{return } s'
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Function -- Expand(s)" label="algorithm:mcts:expand" math=algorithm_name %}
```

- 알고리즘 `array`는 보통 `\begin{array}{l}`처럼 한 컬럼으로 쓰고, block depth는 들여쓰기로 표현한다. 기본 한 단계 들여쓰기는 `\quad\quad`이고, 더 깊은 단계는 `\quad\quad`를 추가한다. `&` 정렬은 Input/Output 표처럼 꼭 필요한 경우에만 쓴다.
- 알고리즘 `array` 내부에서는 줄 사이에 빈 줄을 넣지 않는다. Markdown 원문에서 빈 줄이 중간중간 들어가면 알고리즘 흐름을 읽기 어렵고, MathJax 렌더링도 예측하기 어려워진다.
- 알고리즘에서 설명 문장은 `\text{...}` 안에 넣고, 변수와 수식은 LaTeX 기호로 둔다.
- 긴 알고리즘은 모바일에서 가로 스크롤이 생길 수 있으므로 한 줄을 너무 길게 만들지 않는다.

## Callout Blocks

- Notion callout처럼 강조 박스가 필요하면 `callout.html` include를 사용한다.
- callout을 쓰는 글은 front matter에 `render_with_liquid: true`를 둔다.
- `type`은 `note`, `idea`, `warning`, `quote`, `danger` 중에서 고른다.
- callout 본문에 Markdown이나 수식이 들어가면 `capture`로 먼저 잡고 `content=`에 넘긴다.

```liquid
{% capture callout_body %}
MCTS는 모든 미래를 완전 탐색하지 않고, 여러 rollout 결과를 통해 action의 가치를 추정한다.
{% endcapture %}

{% include callout.html type="idea" title="핵심 아이디어" content=callout_body %}
```
