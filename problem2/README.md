# Problem 2 :  템플릿과 STL을 활용한 컨테이너 설계
### 요구 역량
- C++ 템플릿 프로그래밍 능력
- STL 컨테이너 및 이터레이터 설계/구현 능력
- 클래스 캡슐화 및 접근 제한자 활용
- STL 알고리즘과의 호환성(이터레이터, 범위 기반 for문 등)
- 예외 안전성 및 const-correctness(상수/비상수 메서드 구분)

### 주요 작업 포인트
- 템플릿 클래스 CircularBuffer<T> 직접 구현
- 고정 크기 원형 버퍼 구조 설계 및 데이터 관리
- STL 호환 forward iterator 구현(begin(), end())
- 필수 메서드: size(), capacity(), empty(), push_back(), pop_front(), front(), back()
- const/non-const 버전 메서드 모두 제공
- 범위 기반 for문 및 STL 알고리즘 사용 가능하도록 설계

### 예시
- CircularBuffer<double> tempBuffer(5); 선언 후 여러 센서 데이터 push_back 및 범위 기반 for문 순회
- std::max_element, std::accumulate 등 STL 알고리즘을 사용해 버퍼 내 데이터 처리

### 컴파일 방법
```
cd problem2/
g++ -std=c++17 -o test main.cpp
test.exe
```