---
layout: post
title: Ros 공부 3일차 - topic, 서비스 발행
date: 2022-02-27 18:49:38 +0900
slug: ros-day-03-topic-service-publishing
render_with_liquid: false
categories:
- Tool
- ROS
tags:
- ROS
- Service
- Topic
last_modified_at: 2022-02-27 18:49:38 +0900
imported_images:
- assets/img/blog/ros-day-03-topic-service-publishing/image-001.png
- assets/img/blog/ros-day-03-topic-service-publishing/image-002.png
- assets/img/blog/ros-day-03-topic-service-publishing/image-003.png
- assets/img/blog/ros-day-03-topic-service-publishing/image-004.png
series: ros-basics
series_order: 5
source:
  provider: tistory
  id: 6
---

## 1. 터틀심 노드 생성

```elixir
$ roscore
$ rosrun turtlesim turtlesim_node
```

![](/assets/img/blog/ros-day-03-topic-service-publishing/image-001.png)

## 2. 새로운 노드를 생성하고 거북이 방향조정

```elixir
$ rosrun turtlesim turtle_teleop_key
```

## 3. 노드 정보 확인

```routeros
$ rosnode info /teleop_turtle
```

## 4. 그 중 turtlesim 노드와 tturtle_teleop_key의 노드 사이에서 연결되어있는 topic의 메시지를 스크린에 출력

```shell
$ rostopic echo turtle1/cmd_vel
```

turtle_teleop_key에서 거북이에 명령을 줄때마다 토픽이 보내는 메시지 타입을 볼수 있다.

![](/assets/img/blog/ros-day-03-topic-service-publishing/image-002.png)

## 5. 토픽의 메세지 타입 확인하기

```routeros
$ rostopic type /turtle1/cmd_vel
```

## 6. 메세지 필드 확인하기

```bash
$ rosmsg show geometry_msgs/Twist
geometry_msgs/Vector3 linear
  float64 x
  float64 y
  float64 z
geometry_msgs/Vector3 angular
  float64 x
  float64 y
  float64 z
```

## 7. rostopic pub [topic] [msg_type] [args] 명령을 사용해서 토픽을 발행 (pub을 사용하면 임시 노드가 생성된다.)

```lsl
$ rostopic pub /turtle1/cmd_vel geometry_msgs/Twist -r 1 -- '[2.0, 0.0, 0.0]' '[0.0, 0.0, -1.8]'
```

-r의 1 : HZ의 단위 -r 2를 입력하면 2초에 한번씩 실행이 된다.

![](/assets/img/blog/ros-day-03-topic-service-publishing/image-003.png)

```lsl
$ rostopic pub -1 /turtle1/cmd_vel geometry_msgs/Twist -- '[2.0, 0.0, 0.0]' '[0.0, 0.0, 1.8]'
```

-1 : 노드를 한번 실행하고 난 후에 노드가 사라진다.

## 8. 가능한 서비스 보이기

```bash
$ rosservice list
/clear
/kill
/reset
/rosout/get_loggers
/rosout/set_logger_level
/rqt_gui_py_node_11760/get_loggers
/rqt_gui_py_node_11760/set_logger_level
/spawn
/teleop_turtle/get_loggers
/teleop_turtle/set_logger_level
/turtle1/set_pen
/turtle1/teleport_absolute
/turtle1/teleport_relative
/turtlesim/get_loggers
/turtlesim/set_logger_level
```

## 9. 서비스를 실행시키기(/clear)

a. 서비스 타입 보이기

```
$ rosservice type /clear
```

b. 서비스의 메세지 형태를 알아보자

```bash
$ rossrv show std_srvs/Empty
```

c. 서비스를 시작하기 위해 rosservice call [service] [args]

```bash
$ rosservice call /clear
```

## 10. 서비스를 실행시키기(/spawn)

a. 서비스 타입 보이기

```shell
$ rosservice type /spawn
turtlesim/Spawn
```

b. 서비스의 메세지 형태를 알아보자.

```shell
$ rossrv show turtlesim/Spawn
float32 x
float32 y
float32 theta(방향)
string name
---
string name
```

c. 서비스를 시작하기 위해 rosservice call [service] [args]

```shell
$ rosservice call /spawn 3 3 0.2 "turtle2"
name: "new_turtle”
```

💡 이때, 다른 roscore, turtlesim_node를 제외한 다른 터미널창은 꺼주길 바란다.

![](/assets/img/blog/ros-day-03-topic-service-publishing/image-004.png)

우리는 여기서 turtle1, turtle2의 서비스 밑으로 각각 3개의 topic이 묶여 있는 것을 알수 있다.
