---
layout: post
title: Ros 공부 2일차 - Topic의 기초
date: 2022-02-27 04:19:43 +0900
slug: ros-day-02-topic-basics
render_with_liquid: false
categories:
- Tool
- ROS
tags:
- Publish
- ROS
- subsribe
- Topic
last_modified_at: 2022-02-27 04:22:28 +0900
imported_images:
- assets/img/blog/ros-day-02-topic-basics/image-001.png
series: ros-basics
series_order: 4
source:
  provider: tistory
  id: 5
---

## Topic의 발행

Ros는 독립적인 노드로 구성되어있다. 그렇다면 이 노드사이의 데이터와 정보를 교환하려면 어떻게 해야될까? 가장 보편적인 방법은 토픽(topic)을 사용한 통신이다. 우리는 이번에 그러한 Topic을 사용하여 data를 교환해볼려고 한다.

일단 우리는 목적을 정해야한다.

목적 1 : 숫자1, 문자a, 특수문자#를 전달하자.

목적 2 :  숫자를 받으면 'hello ' 문자를 받으면 'good ', 특수문자 'day ' 출력할 예정이다.

하나는 subscribe 노드로 사용할 예정이고, 하나는 publisher 노드로 사용할 예정이다.

먼저 우리는 과거에  turtle 이라는 패키지를 만든것과 같이 package를 하나 만들어줄려고 한다.

```html
$ cd ~/RC_ws/src
$ catkin_create_pkg beginner rospy roscpp std_msgs
$ cd ..
$ $ catkin_make
```

이제 패키지 안에 src 안에 python 형식으로 노드를 두개 만들 것이다.

우리는 이들을 std_msgs 형태로 공유할 예정이다.

먼저 std_msg를 알아보자. 우리는 ros document를 이 과정에서 사용할 예정이다.

[http://docs.ros.org/en/lunar/api/std_msgs/html/index-msg.html](http://docs.ros.org/en/lunar/api/std_msgs/html/index-msg.html)

[std_msgs Msg/Srv Documentation

docs.ros.org](http://docs.ros.org/en/lunar/api/std_msgs/html/index-msg.html)

그 중 커다란 저장공간이 필요하지 않으므로, int16와 string을 사용할 예정이다.

먼저 new_publisher.py파일을 beginner 디렉토리안에 만들어주자.

우리는 노드이름을 new_publisher을 선언해줄것이고, topic은 두개의 topic은 사용할 예정이다.

topic 하나의 이름을 integer로 선언하고 int16의 메세지를 주고받으려고 하고 나머지 topic의 이름은  language로 선언하고 String의 메세지를 주고 받겠다.

2hz에 한번씩 정보를 주겠다.

```python
#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int16, String
import time

rospy.init_node('new_publisher')
pub1 = rospy.Publisher('language', String, queue_size=1)
pub2 = rospy.Publisher('integer', Int16, queue_size=1)
pub3 = rospy.Publisher('special_language', String, queue_size=1)
rate = rospy.Rate(1)

language = "a"
number = 1
special_language ="@"
while not rospy.is_shutdown():
    pub2.publish(number)
    time.sleep(0.3)
    pub1.publish(language)
    time.sleep(0.3)
    pub3.publish(special_language)
    rate.sleep()
```

첫번째로 publisher 파일을 만들었다.

이제 두번째로 subscriber 파일을 만들어보자.

```python
#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int16, String

def callback1(msg):
    rospy.loginfo('hello ')

def callback2(msg):
    rospy.loginfo('good ')
    
def callback3(msg):
    rospy.loginfo('day ')
    rospy.loginfo('')

rospy.init_node('new_subscriber')
sub1 = rospy.Subscriber('integer', Int16, callback1)
sub2 = rospy.Subscriber('language', String, callback2)
sub3 = rospy.Subscriber('special_language', String, callback3)
rospy.spin()
```

만들었다!!! 코드 관련 내용은 ROS  wiki를 참고해보기 바란다.

마지막으로 rqt_graph를 보자

![](/assets/img/blog/ros-day-02-topic-basics/image-001.png)
