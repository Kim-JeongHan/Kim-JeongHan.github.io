---
layout: post
title: ROS 공부 9일차 - C++로 노드를 생성해보다.
date: 2022-05-31 17:52:21 +0900
slug: ros-day-09-cpp-node
render_with_liquid: false
categories:
- Tool
- ROS
tags:
- C++
- ROS
last_modified_at: 2022-06-07 17:57:47 +0900
imported_images:
- assets/img/tistory/14/image-001.png
series: ros-basics
series_order: 12
source:
  provider: tistory
  id: 14
---

위 코드는 ROS로 효과적인 로봇 프로그래밍하기 3판에 있는 코드와 설명을 사용하겠다.

```cpp
#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>

int main(int argc, char **argv)
{
  ros::init(argc, argv, "example1_a");
  ros::NodeHandle n;
  ros::Publisher pub = n.advertise<std_msgs::String>("message", 1000);
  ros::Rate loop_rate(10);
  while (ros::ok())
  {
    std_msgs::String msg;
    std::stringstream ss;
    ss << " I am the example1_a node ";
    msg.data = ss.str();
    //ROS_INFO("%s", msg.data.c_str());
    pub.publish(msg);
    ros::spinOnce();
    loop_rate.sleep();
  }
  return 0;
}
```

- ros::init(argc, argv, "example1_a") -> 노드를 초기화하고 이름을 정한다.
- ros::NodeHandle n -> 프로세스의 핸들러, 우리 코드가 환경과 상호작용할 수 있게 해준다.
- ros::Publisher pub = n.advertise<std_msgs::String>("message", 1000) 
  아래 코드는 발행자의 인스턴스를 만들고 마스터에 그 토픽의 이름과 타입을 알려준다.
  토픽의 이름은 message이고, 두번째 파라미터는 버퍼의 크기이다. 만약 토픽이 데이터를 빨리 발행하면, 버퍼는 적어도 1000개의 메시지를 유지할 것이다.

버퍼란? 데이터를 한 곳에서 다른 한 곳으로 전송하는 동안 일시적으로 그 데이터를 보관하는 [메모리](https://ko.wikipedia.org/wiki/%EB%A9%94%EB%AA%A8%EB%A6%AC)의 영역이다. **버퍼링**(buffering)이란 버퍼를 활용하는 방식 또는 버퍼를 채우는 동작을 말한다.

![](/assets/img/tistory/14/image-001.png)

- ros::Rate loop_rate(10) -> 데이터를 보내는 주파수를 정하는 것이다. 단위는 HZ이다.
- while(ros::ok()) -> Ctrl+C키가 눌러지거나 ROS가 모든 노드를 중지하면 노드를 정지시킨다.
- std_msgs::String msg;                        -> std_msg 의 string타입의 메세지를 msg로 선언
  std::stringstream ss;                            -> std에서 string타입의 변수 ss 선언
  ss << " I am the example1_a node "; -> ss안에 문자열을 집어넣는다.
  msg.data = ss.str();                             -> msg.data(string)에 ss의 문자열을 집어 넣는다.
- pub.publish(msg); -> 변수msg에 담긴 정보를 pub 해준다.
- ros::spinOnce();

<div class="table-responsive tistory-table">
<table>
<tbody>
<tr>
<td> </td>
<td><span>ros::spin</span></td>
<td>ros::spinOnce()</td>
</tr>
<tr>
<td>공통점</td>
<td colspan="2"><span>버퍼(큐)에<span> 쌓여있는 콜백함수를 처리한다. </span></span></td>
</tr>
<tr>
<td>차이점</td>
<td>자체로 무한루프의 의미를 지니고 있다. 계속적으로 함수를 콜백한다.<br/>spin 다음에 있는 코드는 실행되지 않는다.</td>
<td>호출 시점까지 버퍼에 쌓여있는 콜백함수를 처리한다. 그 후 다음 코드가 실행된다.</td>
</tr>
</tbody>
</table>
</div>

```cpp
while (ros::ok())
{
  ros::getGlobalCallbackQueue()->callAvailable(ros::WallDuration(0.1));
}
```

```cpp
ros::getGlobalCallbackQueue()->callAvailable(ros::WallDuration(0));
```

호출되는 순간 버퍼(큐)안에 쌓여있는 모든 콜백함수를 처리한 후 빠져나가고 다음 코드를 실행시킨다.

보통 spinonce는 위 코드와 같이 while문안에서 loop_rate.sleep()과 같이 사용된다.

```cpp
  while (ros::ok())
  {
    std_msgs::String msg;
    std::stringstream ss;
    ss << " I am the example1_a node ";
    msg.data = ss.str();
    //ROS_INFO("%s", msg.data.c_str());
    pub.publish(msg);
    ros::spinOnce();
    loop_rate.sleep();
  }
```

- loop_rate.sleep();  -> 코드를 설정한 주기적으로 돌리기 위해 사용되는 코드이다. 
  예시를 하나 들어보자. 주기가 4초로 설정된 코드에서 while문 안에서 코드가 실행되는 상황이다. ros::spinonce();까지 2초의 시간이 소요되었다. 그리고 loop_rate.sleep이 실행되면 2초동안 코드는 기다린 뒤에 다시 while문이 돌기 시작한다.

참고한 사이트

[https://gnaseel.tistory.com/31](https://gnaseel.tistory.com/31)
