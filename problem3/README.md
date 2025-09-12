# Problem 3 :  멀티스레딩과 함수형 프로그래밍을 활용한 병렬 처리 
### 요구 역량
- C++ 템플릿 프로그래밍 능력
- 멀티스레딩 프로그래밍 (std::thread, std::mutex, std::condition_variable)
- 함수형 프로그래밍 스타일 (람다 함수, std::function)
- 스레드 풀 설계 및 작업 큐 관리
- 병렬 처리 알고리즘 구현 및 성능 최적화
- 동기화 및 스레드 안전성 보장

### 주요 작업 포인트
- 템플릿 클래스 ParallelProcessor<T> 직접 구현
- 스레드 풀 기반 병렬 처리 시스템 설계
- parallel_map 함수로 함수형 프로그래밍 스타일 병렬 맵핑 구현
- 작업 큐와 스레드 동기화 메커니즘 구현 (std::mutex, std::condition_variable)
- 대용량 데이터 청크 분할 및 병렬 처리 최적화
- 예외 안전성 및 자원 관리 (RAII 패턴)

### 예시
- ParallelProcessor<int> processor(4); 선언 후 1,000,000개 픽셀 데이터 병렬 처리
- processor.parallel_map(pixels, [](int p) { return min(255, p + 50); }) 으로 이미지 밝기 조정 및 4배 성능 향상

### 컴파일 방법
```
cd problem3/
g++ -std=c++17 -pthread -Wall -Wextra -O2 -o test main.cpp
test.exe
```