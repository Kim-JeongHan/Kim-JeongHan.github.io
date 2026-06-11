---
layout: post
title: ROS 공부 8일차 - python을 활용하여 센서 데이터 효율화
date: 2022-05-18 00:36:39 +0900
slug: ros-day-08-python-sensor-data
render_with_liquid: false
categories:
- Tool
- ROS
tags:
- Python
- ROS
- 비동기적
last_modified_at: 2022-05-20 15:05:35 +0900
series: ros-basics
series_order: 10
source:
  provider: tistory
  id: 12
---

roboticsbackend 홈페이지에서 ROS tutorial 내용을 바탕으로 정리한 내용이다.

[https://roboticsbackend.com/how-to-use-a-ros-timer-in-python-to-publish-data-at-a-fixed-rate/](https://roboticsbackend.com/how-to-use-a-ros-timer-in-python-to-publish-data-at-a-fixed-rate/)

크게 세가지 분류로 설명하겠습니다.

1. 타이머가 없는방식

2. ROS타이머를 사용하여 비동기식으로 publish

3. 필터를 사용한 oversampling, averaging방식입니다.

## 1-1타이머 없는 쉬운 방식

```python
#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64

def read_temperature_sensor_data():
    # Here you read the data from your sensor
    # And you return the real value
    return 30

if __name__ == '__main__':
    rospy.init_node("your_sensor_node")

    # Create a ROS publisher
    data_publisher = rospy.Publisher("/temperature", Float64, queue_size=1)

    # Create a rate
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        msg = Float64()
        msg.data = read_temperature_sensor_data()
        data_publisher.publish(msg)
        rate.sleep()
```

위 코드는 센서데이터의 읽는 것과 publish하는 것을 모두 10hz 기준으로 작동시킵니다.

사실 위의 방식은 추천하는 방식은 아닙니다. ROS wiki에서 기초 python코드로 제공하는 것과 큰 차이는 없겠지요. 흔히 말하는 ROS를 접한지 얼마안된 사람들이 시험삼아 코드를 짜보는 단계입니다.

## 1-2 Timer가 없는 class를 사용한 방식

```python
#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64

class TemperatureSensor:

    def read_temperature_sensor_data(self):
        # Here you read the data from your sensor
        # And you return the real value
        self.temperature = 30.0

    def __init__(self):
        # Create a ROS publisher
        self.temperature_publisher = rospy.Publisher("/temperature", Float64, queue_size=1)

        # Initialize temperature data
        self.temperature = 0

    def publish_temperature(self):
        msg = Float64()
        msg.data = self.temperature
        self.temperature_publisher.publish(msg)

if __name__ == '__main__':
    rospy.init_node("your_sensor_node")

    # Create an instance of Temperature sensor
    ts = TemperatureSensor()

    # Create a rate
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        ts.read_temperature_sensor_data()
        ts.publish_temperature()
        rate.sleep()
```

class를 활용한 객체 지향을 사용한 코드입니다. 대부분의 python을 활용한 코드는 위와같이 class를 사용한 방식으로 진행됩니다.

## ROS Timer을 활용한 데이터 읽기 및 비동기식 publish

비동기라는 개념이 어색할수 있다. 간략하게 비동기에 대한 개념을 설명하자면, 동기화되지않게 각각 따로 작용하는 방식을 의미한다.

```python
#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64

class TemperatureSensor:

    def read_temperature_sensor_data(self, event=None):
        # Here you read the data from your sensor
        # And you return the real value
        self.temperature = 30.0

    def __init__(self):
        # Create a ROS publisher
        self.temperature_publisher = rospy.Publisher("/temperature", Float64, queue_size=1)

        # Initialize temperature data
        self.temperature = 0

    def publish_temperature(self, event=None):
        msg = Float64()
        msg.data = self.temperature
        self.temperature_publisher.publish(msg)

if __name__ == '__main__':
    rospy.init_node("your_sensor_node")

    # Create an instance of Temperature sensor
    ts = TemperatureSensor()

    # Create a ROS Timer for reading data
    rospy.Timer(rospy.Duration(1.0/10.0), ts.read_temperature_sensor_data)

    # Create another ROS Timer for publishing data
    rospy.Timer(rospy.Duration(1.0/10.0), ts.publish_temperature)

    # Don't forget this or else the program will exit
    rospy.spin()
```

ropy.Timer함수를 사용하여 publish 하는 것과 read 하는 것을 독립적으로 구분하여 진행을 하였다. 이 작업을 통해 우리는 엄청난 장점을 가진 코드 구성을 할수 있다. data를 읽어 오는 것과 data를 publish하는 것을 다른 주기로 진행할 수 있다.

## ROS Timer을 활용한 oversampling, averaging

먼저 oversampling에 대해서 간략하게 설명하겠다. oversampling이란? 데이터를 읽는 빈도를 데이터를 publish하는 빈도보다 증가시키는 것을 의미한다.

```python
#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64

class TemperatureSensor:

    def read_temperature_sensor_data(self, event=None):
        # Here you read the data from your sensor
        # And you return the real value
        if self.temp_index < self.temp_max_index:
            self.temp_data.append(30.0)
            self.temp_index += 1
        else:
            self.temperature = sum(self.temp_data) / len(self.temp_data)
            self.temp_index = 0
            self.temp_data = []

    def __init__(self):
        # Create a ROS publisher
        self.temperature_publisher = rospy.Publisher("/temperature", Float64, queue_size=1)

        # Initialize temperature data
        self.temperature = 0

        self.temp_data = []
        self.temp_index = 0
        self.temp_max_index = 1

    def publish_temperature(self, event=None):
        msg = Float64()
        msg.data = self.temperature
        self.temperature_publisher.publish(msg)

if __name__ == '__main__':
    rospy.init_node("your_sensor_node")

    # Create an instance of Temperature sensor
    ts = TemperatureSensor()

    # Create a ROS Timer for reading data
    rospy.Timer(rospy.Duration(1.0/100.0), ts.read_temperature_sensor_data)

    # Create another ROS Timer for publishing data
    rospy.Timer(rospy.Duration(1.0/10.0), ts.publish_temperature)

    # Don't forget this or else the program will exit
    rospy.spin()
```

이 코드는 100Hz에서 온도 데이터를 읽고, 10Hz에서 데이터를 publish한다.

이 코드는 필터를 사용하여 읽어온 두개의 data씩을 average하여 계산한뒤, 진동수를 50hz로 업데이트한다.

우리는 필터를 통해 업데이트된 값들이 5배로 oversampling을 하고 있음을 알 수 있다.

> 결론 : rostimer을 사용하여 비동기적으로 read와 publish를 하는 것은 효율적으로 코드를 구현할수 있게 해준다.

[https://roboticsbackend.com/how-to-use-a-ros-timer-in-python-to-publish-data-at-a-fixed-rate/](https://roboticsbackend.com/how-to-use-a-ros-timer-in-python-to-publish-data-at-a-fixed-rate/)
