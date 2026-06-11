---
layout: post
title: 제네릭 포인터(generic pointer)
date: 2025-09-01 22:27:03 +0900
slug: generic-pointer
render_with_liquid: false
categories:
- 프로그래밍
- c++
tags:
- C++
- generic pointer
last_modified_at: 2025-09-01 22:27:03 +0900
source:
  provider: tistory
  id: 64
---

void* 자료형의 포인터를 제네릭 포인터라고 한다. 다른 포인터와 마찬가지로 제네릭 포인터도 주소를 가리킬 수 있지만, 실제 자료형은 알 수 없다. 제네릭 포인터는 다른 포인터의 내용을 담기 위해 주로 사용되나, 실젤 자료형을 담지 않는다. 하여, 역참조하는 것이 불가능하다.

```cpp
int main(int argc, char** argv) {
 int var = 9;
 int* ptr = &var;
 void* gptr = ptr;
 
 printf("%d\n", *gptr); //역참조 오류
 
 return 0;
}
```

### 유용한 예시 - 포인터 입력 인수

```cpp
void print_bytes(void* data, size_t length) {
  char delim = ' ';
  unsigned char* ptr = data;
  for (size_t i = 0; i < length; i++) {
    printf("%c 0x%x", delim, *ptr);
    delim = ',';
    ptr++;
  }
  printf("\n");
}
int main(int argc, char** argv) {
 int a = 9;
 double b = 18.9;

 print_bytes(&a, sizeof(int));
 print_bytes(&b, sizeof(double));

 return 0;
}
```

우리가 template을 사용하여 다양한 인자를 전송하는 방법도 있지만, generic pointer를 사용한 인자 전달 방식이 있다.
