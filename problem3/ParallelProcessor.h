#pragma once
#include <vector>
#include <thread>
#include <future>
#include <functional>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <chrono>
#include <stdexcept>
#include <type_traits>
#include <algorithm>

template<typename T>
class ParallelProcessor {
private:
    size_t thread_count_;
    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex queue_mutex_;
    std::condition_variable condition_;
    bool stop_;

public:
    // 생성자: 스레드 개수 지정
    explicit ParallelProcessor(size_t thread_count);
    
    // 소멸자: 스레드 정리
    ~ParallelProcessor();
    
    // 복사 방지
    ParallelProcessor(const ParallelProcessor&) = delete;
    ParallelProcessor& operator=(const ParallelProcessor&) = delete;
    
    // 병렬 맵 함수 - 핵심 기능
    template<typename Func, typename ReturnType = std::invoke_result_t<Func, T>>
    std::vector<ReturnType> parallel_map(const std::vector<T>& input, Func func);
    
    // 유틸리티 함수들
    size_t get_thread_count() const;

    // 대기 중인 작업 수 반환
    size_t pending_tasks() const;

private:
    // 스레드 풀 관련 내부 함수들
    void worker_thread();
    void enqueue_task(std::function<void()> task);

    // 스레드 풀 초기화/정리 함수
    void initialize_workers();
    void shutdown_workers();
};

// 구현부 
// TODO: 구현 예정