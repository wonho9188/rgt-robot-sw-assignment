#pragma once
#include <stdexcept>
#include <iterator>

template<typename T>
class CircularBuffer {
private:
    T* buffer;           // 실제 데이터를 저장할 배열
    size_t capacity_;    // 버퍼의 최대 크기
    size_t size_;        // 현재 저장된 데이터 개수
    size_t head_;        // 첫 번째 데이터의 인덱스
    size_t tail_;        // 마지막 데이터의 다음 인덱스

public:
    // 생성자
    explicit CircularBuffer(size_t capacity);
    
    // 소멸자
    ~CircularBuffer();
    
    // 복사 생성자 및 대입 연산자 (나중에 구현)
    CircularBuffer(const CircularBuffer& other) = delete;
    CircularBuffer& operator=(const CircularBuffer& other) = delete;
    
    // 기본 메서드 선언
    size_t size() const;
    size_t capacity() const;
    bool empty() const;
    
    // 데이터 추가/삭제/접근 메서드 선언
    void push_back(const T& item);
    void pop_front();
    T& front();
    const T& front() const;
    T& back();
    const T& back() const;
    
    // Forward iterator 구현
    class iterator {
    private:
        CircularBuffer<T>* buffer_;
        size_t current_index_;
        size_t count_;
        
    public:
        // STL 호환을 위한 타입 정의
        using iterator_category = std::forward_iterator_tag;
        using value_type = T;
        using difference_type = std::ptrdiff_t;
        using pointer = T*;
        using reference = T&;
        
        // 생성자
        iterator(CircularBuffer<T>* buffer, size_t index, size_t count = 0)
            : buffer_(buffer), current_index_(index), count_(count) {}
        
        // 역참조 연산자
        T& operator*() {
            return buffer_->buffer[current_index_];
        }
        
        // 전위 증가 연산자
        iterator& operator++() {
            if (count_ < buffer_->size_) {
                current_index_ = (current_index_ + 1) % buffer_->capacity_;
                count_++;
            }
            return *this;
        }
        
        // 후위 증가 연산자
        iterator operator++(int) {
            iterator temp = *this;
            ++(*this);
            return temp;
        }
        
        // 비교 연산자
        bool operator==(const iterator& other) const {
            return count_ == other.count_;
        }
        
        bool operator!=(const iterator& other) const {
            return !(*this == other);
        }
    };
    
    // begin과 end 메서드 선언
    iterator begin();
    iterator end();
};

// 생성자 구현
template<typename T>
CircularBuffer<T>::CircularBuffer(size_t capacity) 
    : capacity_(capacity), size_(0), head_(0), tail_(0) {
    buffer = new T[capacity_];
}

// 소멸자 구현
template<typename T>
CircularBuffer<T>::~CircularBuffer() {
    delete[] buffer;
}

template<typename T>
size_t CircularBuffer<T>::size() const {
    return size_;
}

template<typename T>
size_t CircularBuffer<T>::capacity() const {
    return capacity_;
}

template<typename T>
bool CircularBuffer<T>::empty() const {
    return size_ == 0;
}

// push_back 구현
template<typename T>
void CircularBuffer<T>::push_back(const T& item) {
    buffer[tail_] = item;                    
    tail_ = (tail_ + 1) % capacity_;        
    
    if (size_ < capacity_) {
        size_++;                             
    } else {
        head_ = (head_ + 1) % capacity_;     
    }
}

// pop_front 구현
template<typename T>
void CircularBuffer<T>::pop_front() {
    if (empty()) {
        throw std::runtime_error("빈 버퍼에서 pop_front() 호출");
    }
    head_ = (head_ + 1) % capacity_;       
    size_--;                                
}

// front 구현 (non-const)
template<typename T>
T& CircularBuffer<T>::front() {
    if (empty()) {
        throw std::runtime_error("빈 버퍼에서 front() 호출");
    }
    return buffer[head_];                    // head 위치의 데이터 반환
}

// front 구현 (const)
template<typename T>
const T& CircularBuffer<T>::front() const {
    if (empty()) {
        throw std::runtime_error("빈 버퍼에서 front() 호출");
    }
    return buffer[head_];                    // head 위치의 데이터 반환
}

// back 구현 (non-const)
template<typename T>
T& CircularBuffer<T>::back() {
    if (empty()) {
        throw std::runtime_error("빈 버퍼에서 back() 호출");
    }
    size_t back_index = (tail_ - 1 + capacity_) % capacity_;  // tail 이전 위치
    return buffer[back_index];
}

// back 구현 (const)
template<typename T>
const T& CircularBuffer<T>::back() const {
    if (empty()) {
        throw std::runtime_error("빈 버퍼에서 back() 호출");
    }
    size_t back_index = (tail_ - 1 + capacity_) % capacity_;  // tail 이전 위치
    return buffer[back_index];
}

// begin() 구현
template<typename T>
typename CircularBuffer<T>::iterator CircularBuffer<T>::begin() {
    return iterator(this, head_, 0);  // head부터 시작, 0개 순회
}

// end() 구현  
template<typename T>
typename CircularBuffer<T>::iterator CircularBuffer<T>::end() {
    return iterator(this, 0, size_);  // size개 순회 완료 시점
}