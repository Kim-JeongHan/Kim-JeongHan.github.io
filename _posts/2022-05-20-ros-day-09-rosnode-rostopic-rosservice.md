---
layout: post
title: ROS 공부 9일차 - rosnode, rostopic, rosservice, rosmsg, rosparam
date: 2022-05-20 16:13:36 +0900
slug: ros-day-09-rosnode-rostopic-rosservice
render_with_liquid: false
categories:
- Tool
- ROS
tags:
- ROS
last_modified_at: 2022-05-20 16:13:50 +0900
series: ros-basics
series_order: 11
source:
  provider: tistory
  id: 13
---

오늘은 rosnode, rostopic, rosmsg, rosparam가 지원하는 명령들을 알아보려고 한다.

따로 많이사용하는 것들은 빨간색 처리와 굵음표시를 해놓았다.

## rosnode

- **rosnode info NODE : 노드의 정보를 출력한다**
- rosnode kill NODE : 실행중인 노드를 정지하거나 주어진 신호를 보낸다.
- **rosnode list : 활성화된 노드를 열거한다.**
- rosnode machine hostname : 특정 장치에서 실행중인 노드를 열거하거나 장치들을 나열한다.
- rosnode ping NODE : 노드의 연결성을 테스트한다.
- rosnode cleanup : 연겨할 수 없는 노드의 정보를 등록정보에서 깨끗이 지운다.

## rostopic

- rostopic bw /topic : 토픽에 의해 사용되는 밴드폭을 보여준다.
- **rostopic echo /topic : 스크린에 메시지를 출력한다.**
- **rostopic find messag_type : 이 message_type을 사용하고 있는 topic을 찾아준다.**
- **rostopic info /topic : 토픽의 메시지 타입, 발행차, 구독자와 같은 토픽의 정보를 출력한다.**
- **rostopic list : 활성화된 토픽에 관한 정보를 출력한다.**
- **rostopic pub /topic type_args : topic와 msg타입의 인수를 입력하면 publish하는 노드를 발행한다.**
- **rostopic type /topic : topic의 msg 타입을 알수 있다.**

## rosmsg

- **rosmsg show : 메시지의 필드를 보여준다.**
- **rosmsg list : 모든 메세지를 열거한다.**
- rosmsg package : 패키지 안에 있는 모든 메시지를 열거한다.
- rosmsg packages : 그 메시지를 가진 모든 패키지를 열거한다.

## rosservice

- **rosservice call /service args: 서비스와 srv타입의 인수를 입력하면 서비스를 호출한다.**
- rosservice find msg-type: 서비스가 사용하는 msg타입(srv)으로 서비스를 검색한다.
- **rosservice info /service: 서비스에 관한 정보를 출력한다.**
- **rosservice list: 활성화된 서비스를 나열한다.**
- **rosservice type /service: 서비스 타입을 출력한다.**

## rosparam

- **rosparam list: 서버의 모든 파라미터를 열거한다.**
- **rosparam get parameter : 파라미터 값을 얻는다.**
- **rosparam set parameter value : 파라미터값을 정한다.**
- rosparam delete parameter : 파라미터를 지운다.
- rosparam dump file : 파라미터 서버를 하나의 파일에 저장한다.
- rosparam load file : 파일을 파라미터와 함께 파라미터 서버에 로드한다.
