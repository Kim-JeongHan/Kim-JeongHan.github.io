---
layout: post
title: '[QT공부] QsizePolicy란?'
date: 2025-02-04 21:42:48 +0900
slug: qt-qsizepolicy
render_with_liquid: false
categories:
- Tool
- qt
tags:
- QT
last_modified_at: 2025-02-04 21:45:11 +0900
imported_images:
- assets/img/blog/qt-qsizepolicy/image-001.png
- assets/img/blog/qt-qsizepolicy/image-002.png
source:
  provider: tistory
  id: 15
---

**QSizePolicy**는 PySide6(또는 PyQt)에서 위젯의 크기 조정 동작을 정의하는 데 사용되는 클래스이다. 이 정책은 레이아웃 매니저가 위젯을 어떻게 크기 조절할지를 결정하게 도와준다. 위 이미지에 나와 있는 각 상수에 대해 설명하면 다음과 같다:

---

1. **QSizePolicy::Fixed (0)**
  - 위젯은 절대로 크기 조정이 되지 않는다. QWidget::sizeHint()에 의해 제공된 크기만 사용할 수 있다.
  - **예시**: 푸시 버튼의 수직 방향처럼 고정 크기가 필요한 경우.
2. **QSizePolicy::Minimum (GrowFlag)**
  - 위젯의 최소 크기가 sizeHint()로 정의되며, 필요에 따라 확장할 수 있지만, 더 크게 만드는 이점은 없다.
  - **예시**: 푸시 버튼의 수평 방향. 크기는 확장 가능하지만 최소 크기보다 작아질 수 없다.
3. **QSizePolicy::Maximum (ShrinkFlag)**
  - 위젯의 크기가 최대 sizeHint()로 제한된다. 필요에 따라 크기를 줄일 수 있지만, 더 크게 만들 수 없다.
  - **예시**: 구분선(separator line)처럼 공간이 필요할 때 최소한의 크기만 사용하도록 설정.
4. **QSizePolicy::Preferred (GrowFlag | ShrinkFlag)**
  - sizeHint()에 제안된 크기가 가장 적합하지만, 필요에 따라 줄이거나 확장할 수 있다. 크기를 키우는 것에는 특별한 이점이 없다.
  - **예시**: 기본 QWidget 정책으로, 위젯이 너무 작아지지 않는 선에서 자유롭게 크기를 조정할 수 있다.
5. **QSizePolicy::Expanding (GrowFlag | ShrinkFlag | ExpandFlag)**
  - 위젯은 공간이 허용하는 한 최대한 확장되도록 설정된다. 필요 시 축소도 가능하다.
  - **예시**: 수평 슬라이더처럼 가능한 한 많은 공간을 차지하도록 설정할 때.
6. **QSizePolicy::MinimumExpanding (GrowFlag | ExpandFlag)**
  - 최소 크기는 sizeHint()로 설정되지만, 가능한 한 많은 공간을 차지하려고 시도한다. 필요 시 축소는 제한적이다.
  - **예시**: 수평 슬라이더처럼 최소 크기 이상으로 공간을 많이 차지하려고 할 때.

```python
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QSize

app = QApplication([])

class CustomButton(QPushButton):
    def __init__(self, text, size_hint):
        super().__init__(text)
        self._size_hint = size_hint

    def sizeHint(self):
        return self._size_hint

window = QWidget()
layout = QVBoxLayout()

# QSizePolicy::Fixed
btn_fixed = CustomButton("Fixed", QSize(100, 30))
btn_fixed.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

# QSizePolicy::Minimum
btn_minimum = CustomButton("Minimum", QSize(100, 30))
btn_minimum.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

# QSizePolicy::Maximum
btn_maximum = CustomButton("Maximum", QSize(120, 30))
btn_maximum.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

# QSizePolicy::Preferred
btn_preferred = CustomButton("Preferred", QSize(100, 30))
btn_preferred.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

# QSizePolicy::Expanding
btn_expanding = CustomButton("Expanding", QSize(100, 30))
btn_expanding.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

# QSizePolicy::MinimumExpanding
btn_min_expanding = CustomButton("MinimumExpanding", QSize(100, 30))
btn_min_expanding.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

# Add all buttons to the layout
layout.addWidget(btn_fixed)
layout.addWidget(btn_minimum)
layout.addWidget(btn_maximum)
layout.addWidget(btn_preferred)
layout.addWidget(btn_expanding)
layout.addWidget(btn_min_expanding)

window.setLayout(layout)
window.setWindowTitle("QSizePolicy with sizeHint Examples")
window.show()

app.exec()
```

![](/assets/img/blog/qt-qsizepolicy/image-001.png)

최소 크기
![](/assets/img/blog/qt-qsizepolicy/image-002.png)

늘린 크기

1. Fixed와 maximum의 차이는 거의 없는 것 처럼 보인다.

2. minimum은 늘어나는것은 자유 그러나 줄어드는것은 제한이 있다.

3. Expanding 기본 크기는 있되, 가능한 공간차지.(축소가능이라고 하는데 잘모르겠다.)

4. 임계이하로 축소가 가능하다.
