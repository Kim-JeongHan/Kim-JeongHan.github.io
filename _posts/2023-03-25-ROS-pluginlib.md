# pluginlib은 왜 사용할까?

무언가를 하기 전에는 왜 이것을 사용하는 지에 대한 이야기를 해야하기에 먼저 pluginlib을 사용하는 이유를 말하려고자한다.

plungin은 ROS package안에 있는 C++ library에서 loading과 unloading하는 것들을 위해서 만들어졌다. 즉 라이브러리를 실행하는데 있어서 오래걸리는 시간을 단축하기 위해서 만들어 졌다고 보면된다.

즉,우리는 어떠한 라이브러리를 들고올때 불필요한 것들은 사용하지 않을 수 있고 필요한 것에 초점을 맞추어 사용하면 되는것이다! 또한 우리가 대규모 프로젝트를 진행할떄 이전 헤더와 정의 등등 다양한 것들을 무시하고 진행하려고 하는 것이다.
 
 **굉장히 편리하지 않나??**

그럼 기본적인 개념부터 설명해보겠다.
이는 ROS에서 기본적으로 제공하는 tutorials를 따라 설명을 진행하고 다음 step으로는 ROS Navigation에서 사용한 plugins방식을 하나하나 뜯어보는 걸로 하자.

# ROS Pluginlib
<!--stackedit_data:
eyJoaXN0b3J5IjpbMjA1MDQ3NzQ5OCwtMjExNDE5OTc3Nl19
-->