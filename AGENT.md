# Conditional examples

이 파일은 저장소 핵심 규칙이 아니라 수식, include, 이미지 작업에 필요한 예시 모음이다. 핵심 규칙은 [AGENTS.md](AGENTS.md), 작업 절차는 [.agents/blog-writing-workflow.md](.agents/blog-writing-workflow.md)를 먼저 따른다.

## Display math

```latex
$$
Q(s, a)
=
\frac{W(s, a)}{N(s, a)}
$$
```

## Algorithm include

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

## Callout include

```liquid
{% capture callout_body %}
MCTS는 모든 미래를 완전 탐색하지 않고, 여러 rollout 결과로 action의 가치를 추정한다.
{% endcapture %}

{% include callout.html type="idea" title="핵심 아이디어" content=callout_body %}
```

## Image include

```html
<div style="text-align: center;">
  <img src="/assets/img/blog/<post-slug>/<image-name>.png" alt="그림 설명" style="width: 100%;">
</div>
```
