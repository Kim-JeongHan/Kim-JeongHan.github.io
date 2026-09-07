# Python 인터랙티브 예제

이 디렉터리는 블로그 글에 넣을 Python 시뮬레이션을 보관합니다.
독자는 코드 편집기나 터미널 없이 슬라이더를 움직여 입력을 바꿀 수 있습니다.

## 동작 방식

각 예제는 `assets/interactive/<slug>/` 아래에 둡니다.
`index.html`의 `<main>`이 Python 파일과 필요한 패키지를 선언합니다.

```html
<main data-python-demo data-source="./main.py" data-packages='["numpy"]'></main>
<link rel="stylesheet" href="../shared/python-demo.css">
<script type="module" src="../shared/python-demo.js"></script>
```

새 예제는 기존 `kl-divergence/index.html`을 복사한 뒤 `<title>`만 고칩니다.
공통 JavaScript가 슬라이더, 초기화, 계산 상태, Plotly 그림을 생성합니다.
예제 페이지에는 코드 편집 기능이나 터미널을 넣지 않습니다.

## Python 파일 계약

`main.py`는 조절할 입력을 `CONTROLS`에 선언하며 각 항목에는 `name`, `label`, `min`, `max`, `step`, `value`를 넣습니다.

```python
CONTROLS = [{
    "name": "scale", "label": "scale", "min": 0.5, "max": 3.0,
    "step": 0.1, "value": 1.0,
}]
```

`compute(parameters: dict)`는 입력 딕셔너리 하나를 받고 결과 딕셔너리를 반환합니다.
결과에는 화면에 표시할 `status`와 Python dict로 만든 Plotly `data`, `layout`을 둡니다.
Plotly Python 패키지는 필요하지 않습니다.

```python
def compute(parameters: dict):
    scale = float(parameters["scale"])
    x = [0, 1, 2]
    y = [scale * v for v in x]
    return {"status": f"scale = {scale:.1f}", "figure": {
        "data": [{"type": "scatter", "mode": "lines+markers", "x": x, "y": y}],
        "layout": {"title": {"text": "간단한 선 그래프"}},
    }}
```

NumPy 배열은 반환하기 전에 `.tolist()`로 바꿉니다.
NumPy scalar와 수치 scalar도 `float(...)`로 바꾸어 JSON으로 직렬화합니다.
`main.py`에는 브라우저 전용 import를 넣지 않고 Python 숫자 계산을 작성합니다.
`data-packages`에 선언한 Pyodide 배포 패키지는 계산에 사용할 수 있습니다.

## 실행과 패키지

공통 worker가 `data-source`의 `.py`를 읽고 CDN의 Pyodide 314.0.6에서 실행합니다.
기존 KL 예제는 이 배포판의 NumPy 2.4.6을 사용합니다.
Python 함수에는 입력값 딕셔너리 하나만 전달합니다.
처음 열 때 런타임을 CDN에서 내려받으므로 초기 계산이 느릴 수 있으며 상태를 UI에 표시합니다.

`data-packages`에는 Pyodide 배포판에 포함된 패키지만 적습니다.
임의의 PyPI 패키지 설치나 실행 중 `pip install`은 지원하지 않습니다.

## 글에 삽입하기

블로그 글에서는 예제 URL을 다음 iframe으로 삽입합니다.

```html
<iframe
  src="/assets/interactive/<slug>/"
  width="100%" height="650px" style="border: 0;"
  loading="lazy" title="예제의 주제를 설명하는 제목"
></iframe>
```

정적 GitHub Pages 배포에서 동작하므로 별도 서버나 Node 빌드 과정이 필요하지 않습니다.

## 디렉터리 구조

```text
assets/interactive/
├── README.md
├── shared/
│   ├── python-demo.css
│   ├── python-demo.js
│   └── python-worker.js
├── kl-divergence/
│   ├── index.html
│   └── main.py
└── <slug>/
    ├── index.html
    └── main.py
```

`shared/`에는 모든 예제가 함께 쓰는 UI와 스타일을 둡니다.
각 예제의 `index.html`은 선언과 공통 파일 연결만 담당하고 계산은 `main.py`에 둡니다.
기존 `scripts/visualizations/generate_kl_divergence.py`는 표준 라이브러리만 사용하는
얇은 `index.html` 생성 호환 명령으로 유지합니다.
`main.py`만 수정할 때는 HTML을 다시 생성할 필요가 없습니다.

## 로컬에서 빠르게 확인하기

예제 디렉터리에서 네이티브 Python으로 함수의 입력과 반환 구조를 확인합니다.
기존 KL 예제는 이 점검에도 NumPy 2 이상이 필요합니다.

```bash
python - <<'PY'
from main import CONTROLS, compute
parameters = {c["name"]: c["value"] for c in CONTROLS}
result = compute(parameters)
assert isinstance(result["status"], str)
assert set(result["figure"]) == {"data", "layout"}
print(result["status"])
PY
```

이 점검은 Python 함수 계약을 확인하는 용도이며 정적 페이지의 CDN 로딩을 대신하지 않습니다.
