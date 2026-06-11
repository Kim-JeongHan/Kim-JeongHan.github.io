---
layout: post
title: Ros 공부 1일차 - namespace, remappinig이란
date: 2022-02-25 01:59:41 +0900
slug: ros-day-01-namespace-remapping
render_with_liquid: false
categories:
- Tool
- ROS
tags:
- namespace
- remapping
- ROS
- Turtlesim
last_modified_at: 2022-02-25 03:45:42 +0900
imported_images:
- assets/img/blog/ros-day-01-namespace-remapping/image-001.png
- assets/img/blog/ros-day-01-namespace-remapping/image-002.png
- assets/img/blog/ros-day-01-namespace-remapping/image-003.png
- assets/img/blog/ros-day-01-namespace-remapping/image-004.png
- assets/img/blog/ros-day-01-namespace-remapping/image-005.png
- assets/img/blog/ros-day-01-namespace-remapping/image-006.png
- assets/img/blog/ros-day-01-namespace-remapping/image-007.png
- assets/img/blog/ros-day-01-namespace-remapping/image-008.png
series: ros-basics
series_order: 2
source:
  provider: tistory
  id: 3
---

## namspace

ros는 이름 충돌을 피하고자 별도로 구분된 이름공간으로 같은 노드들을 시작시킬 수 있다.  예를들어 로봇의 오른쪽 눈에 카메라 한대, 왼쪽 눈에 카메라 한대가 있다고 생각해보자. 우리는 이때 이 두 카메라를 left/camera, right/camera라고 구분에서 명칭하고 토픽이름 충돌, 노드 이름 충돌을 피하게 만든다.

## remapping

우리는 namespace라는 것을 알아봤다. 그러면 이제 remapping이라는 것을 이해할 차례이다. remapping은 프로그램내에서 이름을 정의하는 문자열을 실행시 remapping 할수 있다. 우리는 이를 터틀심 예시를 통해 알아볼 예정이다.

```html
$ rosrun turtlesim turtlesim_node 
$ rosrun turtlesim turtlesim_node __name:=turtlesim2
$ rqt_graph
```

![](/assets/img/blog/ros-day-01-namespace-remapping/image-001.png)

roscore는 turtlsim_node라는 고유의 노드 name을 확인하여 같은 노드가 켜지는 것을 막는다. 우리는 이를 remapping을 통해 재생성 해주었다. 이는 노드의 충돌을 피할수 있게 되어, 코드의 수정없이 roscore가 새로운 노드를 받아 드릴수 있게 만들어 준다.

여기서 우리는 하나의 노드를 더 실행시켜서 이 세 노드의 관계를 더 직관적으로 알아보겠다.

```html
$ rosrun turtlesim draw_square
```

![](/assets/img/blog/ros-day-01-namespace-remapping/image-002.png)

여기서 우리는 remapping으로 선언된 노드가 topic을 공유하고 있음을 알수 있다. 그렇다면 topic을 공유하지 않는 노드를 생성하기 위해서는 어떻게 해야할까?

일단 이것을 알기 위해 우리는 remapping 명령어 세가지를 알아야 한다.

1. topic remapping

2. __ns namespace remapping(노드를 이름공간 안으로 넣는 것을 의미한다.)

3. __name remapping (노드의 이름을 변경하는 개념)

#### 1. topic remapping 부터 해보자.(이해가 안되는 부분 발생!!!!)

topic remapping은 쉽게 말해 topic을 remapping해주는 것이다. 그렇게 생각하고 쉽게 접근했다.

그런데 여기서 이해가 안되는 부분이 있다.

```html
$ rosrun turtlesim turtlesim_node turtle1:=turtle2
$ rosrun turtlesim draw_square turtle1:=turtle2
```

![](/assets/img/blog/ros-day-01-namespace-remapping/image-003.png)

turtlesim_node의 topic은 /turtle1에서 /turtle2로 변경했지만, draw_square의 노드의 /turtle1은 /turtle2로 바꾸지 못했다.

흐음...그후 다양한 이름으로 /turtle1을 변경하려고 했으나, 변경하지 못했다. ㅠㅠ

이 부분에 대해서 해결한 방법!!!!

turtle1자체가 topic이라는 생각을 버리고 이름공간이라는 개념으로 접근했다.

turtle1/cmd_vel의 topic namespace를 remapping 했더니 성공했다!!!

```html
$ rosrun turtlesim turtlesim_node turtle1/cmd_vel:=turtle/cmd_vel2
$ rosrun turtlesim draw_square turtle1/cmd_vel:=ture/cmd_vel2
```

![](/assets/img/blog/ros-day-01-namespace-remapping/image-004.png)

rqt_graph를 사용해보니 내부의 topic이 아애 turtle1이라는 namespace에서 빠져나온것을 알수 있다.

**ps)그렇다면.... 왜 turtlesim_node의 turtle1은 수정이 된거지....???? 이 부분은 잘모르겠다...**

#### 2.  __ns namespace remapping

여기서부터는 매우 간단하다. 그냥 하나의 이름공간을 크게 생성한다고 보면된다.

```html
$ rosrun turtlesim turtlesim_node __ns:=right
$ rosrun turtlesim draw_square turtle1:=turtle/righe __ns:=right
```

![](/assets/img/blog/ros-day-01-namespace-remapping/image-005.png)

right라는 상위의 이름공간을 만드는 개념이다.

#### 3. __name remapping

마지막으로, node의 이름을 바꾸는 remapping을 해보겠다. 이도 간단하다.

```html
$ rosrun turtlesim turtlesim_node __name:=turtlesim_node1
$ rosrun turtlesim draw_square __name:=draw_quare1
```

![](/assets/img/blog/ros-day-01-namespace-remapping/image-006.png)

여기서는 turtle1을 remapping하지 않고 있기 때문에, turtlesim노드를 하나더 키더라도 topic이 공유된다.

마지막 최종응용!!!!!!

배운것들을 응용해서 터틀봇 topic을 바꾸고 node를 바꾸고 상위 namespace를 추가해서 거북이를 세마리 만들어 보았다.

```html
$ rosrun turtlesim turtlesim_node turtle1/cmd_vel:=turtle/cmd_vel2
& rosrun turtlesim draw_square turtle1/cmd_vel:=turtle/cmd_vel2
//위 두가지는 cmd_vel의 토픽 이름을 remapping 해주었다.

$ rosrun turtlesim turtlesim_node __name:=turtlesim_node1
$ rosrun turtlesim draw_square __name:=draw_quare1
//위 두가지는 node의 이름을 remapping해주었다.

$ rosrun turtlesim turtlesim_node __ns:=right
$ rosrun turtlesim draw_square turtle1:=turtle/righ__ns:=right
//위 두가지는 상위namespace를 remapping해주었다.
```

그리고 rqt_graph를 확인하고 거북이들을 확인한 결과

![](/assets/img/blog/ros-day-01-namespace-remapping/image-007.png)

하나가 벽으로 돌진하는 결과가 나왔다...

turtle/cmd_vel2를 remapping해준 노드가 문제였던것같아서 추가로 pose도 remapping해주었다.(기본의 turtle/cmd_vel2리맵핑 해주는 터미널을 종료 후 실행시켜야한다.)

```html
$ rosrun turtlesim turtlesim_node turtle1/cmd_vel:=turtle/cmd_vel2 turtle1/pose:=turtle/pose2
$ rosrun turtlesim draw_square turtle1/cmd_vel:=ture/cmd_vel2 turtle1/pose:=turtle/pose2
```

![](/assets/img/blog/ros-day-01-namespace-remapping/image-008.png)

거북이 세개를 각각 다른 방식으로 돌려봤다.

remapping에 대한 개념 어느정도 개념이 얼추 잡힌것 같다.

다음번에는 이것들을 똑같이 roslaunch로 구현해보고자 한다.

PS) turtlesim으로 생각보다 많은것들을 배울수있다
