---
layout: post
title: Ros 공부 4일차 - rospy.spin()
date: 2022-03-03 04:18:09 +0900
slug: ros-day-04-rospy-spin
render_with_liquid: false
categories:
- Tool
- ROS
tags:
- ROS
- rospy.spin
last_modified_at: 2022-03-03 04:18:22 +0900
imported_images:
- assets/img/blog/ros-day-04-rospy-spin/image-001.png
- assets/img/blog/ros-day-04-rospy-spin/image-002.png
- assets/img/blog/ros-day-04-rospy-spin/image-003.png
series: ros-basics
series_order: 7
source:
  provider: tistory
  id: 8
---

## rospy.spin()

rospy.spin()

roswiki에서는 사용자의 노드가 셧다운되기전까지 종료로 부터 지킨다고 나와있다. 이에 대한 개념이 잘이해가 안되어서 추가적으로 몇가지 실험을 해보았다.

subscribe 노드이다.  임의의 랜덤한 숫자 두개를 pub하고 있다. subsrcibe노드에서는 따로 수정을 하지 않고 세번의 실험에 동일하게 썼다.

```shell
#!/usr/bin/env python
from gohome import msg
import rospy
from gohome.msg import Complex
from random import random

rospy.init_node('message_publisher')
pub = rospy.Publisher('complex', Complex, queue_size=1)
rate = rospy.Rate(2)
while not rospy.is_shutdown():
    msg = Complex()
    msg.real = random()
    msg.imaginary = random() 
    pub.publish(msg)
    rate.sleep()
```

#### 1. 기존의 publish

publish 노드

```python
#!/usr/bin/env python
import rospy
from gohome.msg import Complex

# print('Real')
def callback(msg):
    print( 'Real :' , msg.real)
    print('Imaginary:' , msg.imaginary)
    print

rospy.init_node('message_subscriber')
sub = rospy.Subscriber('complex', Complex, callback)
# while not rospy.is_shutdown():
#     print('Real')
rospy.spin()
```

![](/assets/img/blog/ros-day-04-rospy-spin/image-001.png)

2. callback 함수 외부에서 print가 추가 된 노드

```python
#!/usr/bin/env python
import rospy
from gohome.msg import Complex

# print('Real')
def callback(msg):
    print( 'Real :' , msg.real)
    print('Imaginary:' , msg.imaginary)
    print

rospy.init_node('message_subscriber')
sub = rospy.Subscriber('complex', Complex, callback)
# while not rospy.is_shutdown():
#     print('Real')
rospy.spin()
```

print는 한번 실행되었다.

![](/assets/img/blog/ros-day-04-rospy-spin/image-002.png)

#### 3. while not ropsy..is_shutdown에 들어가 있는 pirnt

```python
#!/usr/bin/env python
import rospy
from gohome.msg import Complex

#print('Real')
def callback(msg):
    print( 'Real :' , msg.real)
    print('Imaginary:' , msg.imaginary)
    print

rospy.init_node('message_subscriber')
sub = rospy.Subscriber('complex', Complex, callback)
while not rospy.is_shutdown():
    print('Real')
rospy.spin()
```

![](/assets/img/blog/ros-day-04-rospy-spin/image-003.png)

while not ropsy..is_shutdown에 갇쳐있다. 여기서 우리는 rospy.spin은 topic이 subsrcibe노드가 도착하더라도 작동하지 않았다는 것을 알수 있다.
