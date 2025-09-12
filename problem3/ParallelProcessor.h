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

private:
    // 스레드 풀 관련 내부 함수들
    void worker_thread();
    void enqueue_task(std::function<void()> task);

    // 스레드 풀 초기화/정리 함수
    void shutdown_workers();
};

// 구현부 
template<typename T>
ParallelProcessor<T>::ParallelProcessor(size_t thread_count) 
    : thread_count_(thread_count), stop_(false) {
    
    if (thread_count_ == 0) {
        throw std::invalid_argument("Thread count must be greater than 0");
    }
    
    // 워커 스레드들 생성
    for (size_t i = 0; i < thread_count_; ++i) {
        workers_.emplace_back(&ParallelProcessor::worker_thread, this);
    }
}

template<typename T>
ParallelProcessor<T>::~ParallelProcessor() {
    shutdown_workers();
}

template<typename T>
void ParallelProcessor<T>::worker_thread() {
    while (true) {
        std::function<void()> task;
        
        {
            std::unique_lock<std::mutex> lock(queue_mutex_);
            condition_.wait(lock, [this] { return stop_ || !tasks_.empty(); });
            
            if (stop_ && tasks_.empty()) {
                return;
            }
            
            task = std::move(tasks_.front());
            tasks_.pop();
        }
        
        task();
    }
}

template<typename T>
void ParallelProcessor<T>::enqueue_task(std::function<void()> task) {
    {
        std::unique_lock<std::mutex> lock(queue_mutex_);
        if (stop_) {
            throw std::runtime_error("ParallelProcessor is stopped");
        }
        tasks_.emplace(std::move(task));
    }
    condition_.notify_one();
}

template<typename T>
template<typename Func, typename ReturnType>
std::vector<ReturnType> ParallelProcessor<T>::parallel_map(
    const std::vector<T>& input, Func func) {
    
    const size_t input_size = input.size();
    if (input_size == 0) {
        return std::vector<ReturnType>();
    }
    
    std::vector<ReturnType> result(input_size);
    std::vector<std::future<void>> futures;
    
    const size_t chunk_size = std::max(size_t(1), input_size / thread_count_);
    
    for (size_t i = 0; i < input_size; i += chunk_size) {
        const size_t end = std::min(i + chunk_size, input_size);
        
        auto promise = std::make_shared<std::promise<void>>();
        futures.push_back(promise->get_future());
        
        enqueue_task([&input, &result, func, i, end, promise]() {
            try {
                for (size_t j = i; j < end; ++j) {
                    result[j] = func(input[j]);
                }
                promise->set_value();
            } catch (...) {
                promise->set_exception(std::current_exception());
            }
        });
    }
    
    for (auto& future : futures) {
        future.get();
    }
    
    return result;
}

template<typename T>
size_t ParallelProcessor<T>::get_thread_count() const {
    return thread_count_;
}

template<typename T>
void ParallelProcessor<T>::shutdown_workers() {
    {
        std::unique_lock<std::mutex> lock(queue_mutex_);
        stop_ = true;
    }
    
    condition_.notify_all();
    
    for (std::thread& worker : workers_) {
        if (worker.joinable()) {
            worker.join();
        }
    }
}