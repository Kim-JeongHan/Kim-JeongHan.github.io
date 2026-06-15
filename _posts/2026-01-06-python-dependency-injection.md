---
layout: post
title: 의존성 주입(Dependency Injection) 기법을 활용한 파이썬 코드 개선 방법
date: 2026-01-06 12:25:39 +0900
slug: python-dependency-injection
render_with_liquid: false
published: false
categories:
- 프로그래밍
tags:
- python
- dependency-injection
- design-pattern
last_modified_at: 2026-06-15 00:00:00 +0900
source:
  provider: tistory
  id: 80
---

원본 영상: [https://www.youtube.com/watch?v=Xhzn1eAxoXk](https://www.youtube.com/watch?v=Xhzn1eAxoXk)

개인적으로는 원본 영상을 같이 보는 것을 추천한다.

## 서론

코드를 작성하다 보면 특정 구현에 너무 강하게 묶이는 경우가 자주 생긴다.

예를 들어 함수나 클래스 내부에서 직접 파일 경로를 정하고, DB 연결을 만들고, 외부 API 클라이언트를 생성한다고 해보자. 처음에는 편해 보이지만, 나중에 테스트하거나 구현을 바꾸려고 하면 코드 전체가 같이 흔들린다.

이때 사용할 수 있는 설계 방식이 **의존성 주입(Dependency Injection, DI)** 이다.

의존성 주입의 핵심은 간단하다.

- 필요한 객체를 내부에서 직접 만들지 않는다.
- 외부에서 필요한 것을 넘겨받는다.
- 구체 구현보다 역할에 의존한다.

즉, "무엇을 사용할지"를 코드 안에 고정하지 않고, 바깥에서 조립하게 만드는 방식이다.

이 글에서는 파이썬에서 DI를 적용하는 방법을 세 단계로 본다.

1. 함수를 주입하는 가장 단순한 방식
2. `Protocol`을 이용해 역할을 정의하는 방식
3. 필요할 때만 사용하는 간단한 DI 컨테이너

---

## 1. 가장 간단한 DI: 클래스 대신 ‘함수’를 주입

의존성 주입이라고 하면 보통 복잡한 클래스 구조를 먼저 떠올린다.

하지만 파이썬에서는 그렇게 시작할 필요가 없다. 함수도 객체처럼 다룰 수 있기 때문에, 함수 자체를 의존성으로 넘기면 된다.

예를 들어 데이터 로딩 로직을 생각해보자.

```python
from typing import Callable, List, Dict

def load_data_from_csv() -> List[Dict]:
    print("Loading data from data.csv")
    return [{"name": "Arjan", "age": 35}, {"name": "Bob", "age": 42}]

def run_pipeline(loader_function: Callable[[], List[Dict]]):
    data = loader_function()
    print("Pipeline running...")
    print(data)

if __name__ == "__main__":
    run_pipeline(load_data_from_csv)
```

여기서 `run_pipeline`은 CSV 파일을 직접 알지 않는다. 단지 "데이터를 반환하는 함수" 하나만 받는다.

즉, `run_pipeline` 입장에서는 데이터가 어디서 오는지가 중요하지 않다.

- CSV에서 올 수도 있다.
- JSON에서 올 수도 있다.
- DB에서 올 수도 있다.
- 테스트에서는 가짜 데이터를 반환하는 함수일 수도 있다.

여기서 중요한 점은 `run_pipeline`이 구체적인 데이터 소스에서 분리되었다는 것이다.

의존성이 하나의 동작으로 충분히 표현된다면, 굳이 클래스를 만들 필요가 없다. 함수를 넘기는 것만으로도 충분히 좋은 DI가 된다.

---

## 2. 상속 대신 구조: Protocol로 의존성을 정의

그런데 의존성이 항상 함수 하나로 끝나지는 않는다.

상태를 가져야 할 수도 있고, 여러 메서드를 가진 객체가 필요할 수도 있다. 이때는 클래스 기반 설계가 자연스럽다.

여기서 질문은 다음과 같다.

> “이 클래스가 무엇을 상속했는가가 중요한가,
>
> 아니면 **어떤 동작을 제공하는가**가 중요한가?”

파이썬에서는 후자가 더 자연스럽다.

즉, 어떤 클래스를 상속했는지보다, 필요한 메서드를 실제로 제공하는지가 더 중요하다. 이 생각을 타입 시스템에서 표현할 수 있게 해주는 것이 `typing.Protocol`이다.

`Protocol`은 명시적인 상속을 요구하지 않는다. 필요한 메서드만 가지고 있으면 해당 역할을 만족한다고 본다.

이를 구조적 서브타이핑(structural subtyping)이라고 한다. 쉽게 말하면, 파이썬의 덕 타이핑을 타입 힌트 수준에서 정리한 방식이다.

먼저 파이프라인의 역할을 정의해보자.

```python
from typing import Protocol, Any
import json

type Data = list[dict[str, Any]]

class DataLoader(Protocol):
    def load(self) -> Data: ...

class Transformer(Protocol):
    def transform(self, data: Data) -> Data: ...

class Exporter(Protocol):
    def export(self, data: Data) -> None: ...
```

여기서 정의한 것은 구현이 아니다.

각 객체가 어떤 메서드를 제공해야 하는지만 적었다.

- `DataLoader`는 `load()`를 제공해야 한다.
- `Transformer`는 `transform()`을 제공해야 한다.
- `Exporter`는 `export()`를 제공해야 한다.

이제 실제 구현은 자유롭게 만들 수 있다.

```python
class InMemoryLoader:
    def load(self) -> Data:
        return [
            {"name": "Arjan", "age": 37},
            {"name": "Jane", "age": None},
            {"name": "Bob", "age": 45},
        ]

class CleanMissingFields:
    def transform(self, data: Data) -> Data:
        return [row for row in data if row["age"] is not None]

class JSONExporter:
    def __init__(self, filename: str):
        self.filename = filename

    def export(self, data: Data) -> None:
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)
```

여기서 `InMemoryLoader`, `CleanMissingFields`, `JSONExporter`는 각각의 `Protocol`을 상속하지 않았다.

그런데 필요한 메서드를 가지고 있으므로 타입 체커 입장에서는 호환된다고 볼 수 있다.

이제 파이프라인은 구체 구현이 아니라 역할에 의존한다.

```python
class DataPipeline:
    def __init__(
        self,
        loader: DataLoader,
        transformer: Transformer,
        exporter: Exporter,
    ):
        self.loader = loader
        self.transformer = transformer
        self.exporter = exporter

    def run(self) -> None:
        data = self.loader.load()
        clean = self.transformer.transform(data)
        self.exporter.export(clean)
```

`DataPipeline`이 아는 것은 다음뿐이다.

- `loader`는 `load()`를 제공한다.
- `transformer`는 `transform()`을 제공한다.
- `exporter`는 `export()`를 제공한다.

그 이상은 파이프라인의 관심사가 아니다.

- 데이터가 메모리에서 오는지, CSV에서 오는지
- 변환 규칙이 무엇인지
- 결과가 JSON으로 저장되는지, 다른 곳으로 전송되는지

이런 것들은 모두 외부에서 결정된다.

마지막으로 애플리케이션의 진입점에서 실제 객체들을 조립한다.

```python
def main() -> None:
    loader = InMemoryLoader()
    transformer = CleanMissingFields()
    exporter = JSONExporter("output.json")

    pipeline = DataPipeline(loader, transformer, exporter)
    pipeline.run()

    print("Pipeline completed. Output written to output.json")
```

이 구조의 장점은 다음과 같다.

- 새로운 loader, transformer, exporter를 추가해도 `DataPipeline`을 수정하지 않아도 된다.
- 테스트에서는 각 역할에 맞는 가짜 구현을 넣으면 된다.
- 각 구현 클래스는 자신에게 필요한 생성자만 가지면 된다.

즉, `Protocol` 기반 DI는 상속 구조를 크게 만들지 않고도 객체지향 DI의 장점을 가져오는 방식이다.

---

## 3. 그래도 필요하다면: 아주 단순한 DI 컨테이너

여기까지 보면 이런 생각이 들 수 있다.

> “의존성이 많아지면, 이걸 매번 main에서 직접 조립해야 하나?”

대부분의 경우에는 직접 조립해도 된다.

실제로 작은 프로젝트에서는 `main()`이나 별도의 조립 함수에서 객체를 생성하고 연결하는 정도면 충분하다.

다만 객체가 많아지고 의존성 그래프가 복잡해지면, 간단한 DI 컨테이너를 둘 수 있다.

여기서 말하는 컨테이너는 거창한 프레임워크가 아니다.

역할은 단순하다.

- 객체를 어떻게 만들지 등록한다.
- 필요할 때 객체를 꺼낸다.
- 필요하면 싱글톤으로 관리한다.

```python
from typing import Callable, Any

class Container:
    def __init__(self) -> None:
        self._providers: dict[str, tuple[Callable[[], Any], bool]] = {}
        self._singletons: dict[str, Any] = {}

    def register(
        self,
        name: str,
        provider: Callable[[], Any],
        singleton: bool = False
    ) -> None:
        self._providers[name] = (provider, singleton)

    def resolve(self, name: str) -> Any:
        if name in self._singletons:
            return self._singletons[name]

        if name not in self._providers:
            raise ValueError(f"No provider registered for '{name}'")

        provider, singleton = self._providers[name]
        instance = provider()

        if singleton:
            self._singletons[name] = instance

        return instance
```

이 컨테이너는 이름을 기준으로 provider를 등록하고, `resolve()`를 통해 객체를 만든다.

이를 이용해 전체 파이프라인을 조립하면 다음과 같다.

```python
def main() -> None:
    container = Container()

    container.register("loader", lambda: InMemoryLoader(), singleton=True)
    container.register("transformer", lambda: CleanMissingFields())
    container.register("exporter", lambda: JSONExporter("output.json"))

    container.register(
        "pipeline",
        lambda: DataPipeline(
            loader=container.resolve("loader"),
            transformer=container.resolve("transformer"),
            exporter=container.resolve("exporter"),
        )
    )

    pipeline = container.resolve("pipeline")
    pipeline.run()
```

이 방식의 장점은 객체 생성 로직이 한 곳에 모인다는 것이다.

테스트할 때는 특정 provider만 바꾸면 된다. 예를 들어 `"loader"`에 실제 로더 대신 테스트용 로더를 등록하면, 나머지 파이프라인 코드는 그대로 사용할 수 있다.

단, 컨테이너는 선택지이다.

의존성이 단순한데 컨테이너부터 만들면 오히려 코드가 멀어진다. 먼저 직접 주입으로 충분한지 보고, 조립 코드가 반복되거나 복잡해질 때만 컨테이너를 두는 편이 낫다.

---

## 결론

의존성 주입은 특별한 프레임워크를 써야만 가능한 기술이 아니다.

파이썬에서는 다음 정도만으로도 충분히 시작할 수 있다.

- 함수 하나면 충분할 때는 함수를 주입한다.
- 객체의 역할을 명확히 하고 싶으면 `Protocol`을 사용한다.
- 의존성 조립이 복잡해질 때만 작은 컨테이너를 둔다.

여기서 중요한 것은 도구가 아니다.

핵심은 구체 구현이 아니라 역할에 의존하는 것이다. 객체가 필요한 것을 스스로 만들지 않고, 외부에서 넘겨받게 만드는 것이다.

즉, DI는 코드를 더 유연하게 만들기 위한 조립 방식이라고 볼 수 있다.
