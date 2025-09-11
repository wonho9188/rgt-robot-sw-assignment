#include "CircularBuffer.h"
#include <iostream>

int main() {
    try {
        // 기본 생성 테스트
        CircularBuffer<double> tempBuffer(5);
        
        std::cout << "Buffer created successfully!" << std::endl;
        std::cout << "Capacity: " << tempBuffer.capacity() << std::endl;
        std::cout << "Size: " << tempBuffer.size() << std::endl;
        std::cout << "Empty: " << (tempBuffer.empty() ? "true" : "false") << std::endl;
        
        // TODO: 더 많은 테스트를 여기에 추가
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}