# Agent Notes

이 저장소는 Jekyll/al-folio 기반 GitHub Pages 블로그이다. 블로그 글을 수정할 때는 기존 포스트의 문체와 구조를 우선 따른다.

## Post Editing

- 논문 리뷰나 개념 글은 `_posts/YYYY-MM-DD-title.md` 형식으로 작성한다.
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
\begin{array}{ll}
\textbf{Input:} & \text{state } s \in \mathcal{S} \\
\textbf{Output:} & \text{expanded state } s' \\[1mm]
\textbf{if} & s\ \text{is not fully expanded}\ \textbf{then} \\
& \text{Randomly select an untried action } a\ \text{to apply in } s \\
& \text{Expand one outcome } s'\ \text{according to } P_a(s' \mid s) \\
& \text{Observe reward } r \\[1mm]
\textbf{return} & s'
\end{array}
$$
{% endcapture %}

{% include algorithm.html title="Function -- Expand(s)" label="algorithm:mcts:expand" math=algorithm_name %}
```

- 알고리즘 `array` 내부에서는 줄 사이에 빈 줄을 넣지 않는다. Markdown 원문에서 빈 줄이 중간중간 들어가면 알고리즘 흐름을 읽기 어렵고, MathJax 렌더링도 예측하기 어려워진다.
- 알고리즘에서 설명 문장은 `\text{...}` 안에 넣고, 변수와 수식은 LaTeX 기호로 둔다.
- 긴 알고리즘은 모바일에서 가로 스크롤이 생길 수 있으므로 한 줄을 너무 길게 만들지 않는다.
