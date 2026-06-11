---
layout: post
title: Ros 공부 4일차 - msg 관련 명령어
date: 2022-03-03 03:53:02 +0900
slug: ros-day-04-msg-commands
render_with_liquid: false
categories:
- Tool
- ROS
tags:
- ROS
- msg
- command
last_modified_at: 2022-03-03 03:53:02 +0900
series: ros-basics
series_order: 6
source:
  provider: tistory
  id: 7
---

```shell
rosmsg show <msg이름>
rosmsg show Bool
rosmsg show std_msgs/bool
```

rosmsg 명령은 메시지 자료형의 내용을 볼 수 있게 한다.

```shell
rosmsg package <package이름>
rosmsg package std_msg
```

package에 포함되어있는 msg를 전부 보여준다.

주의!

메세지 자료형은 반드시 만들어야 할때만 사용하는 것이 좋다. 유사한 데이터에 대하여 서로 다른 메시지를 사용한다면, 시스템이 동작 할 수 있도록 이들 메시지 간에 번역하는 무의미한 작업을 많이 해야만 할 것이다.
