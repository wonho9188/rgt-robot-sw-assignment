#include "CircularBuffer.h"
#include <iostream>
#include <algorithm>
#include <numeric>

int main() {
    try {
        // 기본 생성 테스트
        CircularBuffer<double> tempBuffer(5);
        
        // 데이터 추가
        tempBuffer.push_back(23.5);
        tempBuffer.push_back(24.1);
        tempBuffer.push_back(23.8);
        tempBuffer.push_back(25.2);
        tempBuffer.push_back(24.7);
        tempBuffer.push_back(26.1); 
        
        // 데이터 출력
        std::cout << "=== CircularBuffer Test ===" << std::endl;

        // CircularBuffer 상태 출력
        std::cout << "Buffer Contents (index order): ";
        for (auto value : tempBuffer) {
            std::cout << value << " ";
        }
        std::cout << std::endl;

        std::cout << "Using begin() to end(): ";
        for (auto it = tempBuffer.begin(); it != tempBuffer.end(); ++it) {
            std::cout << *it << " ";
        }
        std::cout << std::endl << std::endl;

        // CircularBuffer 메서드 테스트
        std::cout << "tempBuffer.size() : " << tempBuffer.size() << std::endl;
        std::cout << "tempBuffer.capacity() : " << tempBuffer.capacity() << std::endl;
        std::cout << "tempBuffer.empty() : " << std::boolalpha << tempBuffer.empty() << std::endl;
        
        // STL 알고리즘과 함께 사용
        auto maxTemp = std::max_element(tempBuffer.begin(), tempBuffer.end());
        std::cout << "maxTemp: " << *maxTemp << std::endl;
        
        double avgTemp = std::accumulate(tempBuffer.begin(), tempBuffer.end(), 0.0) / tempBuffer.size();
        std::cout << "avgTemp: " << avgTemp << std::endl;

        std::cout << "tempBuffer.front() : " << tempBuffer.front() << std::endl;
        std::cout << "tempBuffer.back() : " << tempBuffer.back() << std::endl;

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}