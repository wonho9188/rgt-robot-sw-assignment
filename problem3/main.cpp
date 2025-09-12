#include "ParallelProcessor.h"
#include <iostream>
#include <vector>
#include <chrono>
#include <numeric>
#include <string>
#include <cmath>
#include <iomanip>

int main() {
    try {
        std::cout << "=== ParallelProcessor Test Started ===" << std::endl;
        
        // 1. 테스트 데이터 생성 (1,000,000개 픽셀 데이터)
        std::vector<int> pixelData(1000000);
        std::iota(pixelData.begin(), pixelData.end(), 0); // 0, 1, 2, ..., 999999
        
        // 2. ParallelProcessor 생성 (4개 스레드)
        ParallelProcessor<int> processor(4);
        std::cout << "ParallelProcessor created successfully (Thread count: " 
                  << processor.get_thread_count() << ")" << std::endl;
        
        // 3. 순차 처리 시간 측정 (비교용) - CPU 집약적 작업
        std::cout << "\n=== Sequential Processing Test ===" << std::endl;
        auto start_seq = std::chrono::high_resolution_clock::now();
        std::vector<int> sequential_result(pixelData.size());
        for (size_t i = 0; i < pixelData.size(); ++i) {
            // CPU 집약적 작업
            double sum = 0;
            for (int j = 0; j < 100; ++j) {
                sum += std::sin(static_cast<double>(i + j)) * std::cos(static_cast<double>(i - j));
            }
            sequential_result[i] = std::min(255, static_cast<int>(sum) + 50);
        }
        auto end_seq = std::chrono::high_resolution_clock::now();
        auto sequential_time = std::chrono::duration_cast<std::chrono::milliseconds>(end_seq - start_seq);
        
        // 4. 병렬 처리 - 이미지 밝기 증가 테스트
        std::cout << "\n=== Parallel Processing Test ===" << std::endl;
        auto start_parallel = std::chrono::high_resolution_clock::now();
        
        auto brightenedImage = processor.parallel_map(pixelData, [](int pixel) {
            // 동일한 CPU 집약적 작업
            double sum = 0;
            for (int j = 0; j < 100; ++j) {
                sum += std::sin(static_cast<double>(pixel + j)) * std::cos(static_cast<double>(pixel - j));
            }
            return std::min(255, static_cast<int>(sum) + 50);
        });
        
        auto end_parallel = std::chrono::high_resolution_clock::now();
        auto parallel_time = std::chrono::duration_cast<std::chrono::milliseconds>(end_parallel - start_parallel);
        
        // 5. brightenedImage 결과 출력
        std::cout << "\n// brightenedImage results" << std::endl;
        std::cout << "brightenedImage[0] = " << brightenedImage[0] << "  // 0 + 50" << std::endl;
        std::cout << "brightenedImage[1] = " << brightenedImage[1] << "  // 1 + 50" << std::endl;
        std::cout << "brightenedImage[100] = " << brightenedImage[100] << " // 100 + 50" << std::endl;
        std::cout << "brightenedImage[999999] = " << brightenedImage[999999] << " // min(255, 999999 + 50)" << std::endl;
        
        // 6. 픽셀을 문자열로 변환 테스트
        auto pixelStrings = processor.parallel_map(pixelData, [](int pixel) -> std::string {
            return "pixel_" + std::to_string(pixel);
        });
        
        std::cout << "\n// pixelStrings results" << std::endl;
        std::cout << "pixelStrings[0] = \"" << pixelStrings[0] << "\"" << std::endl;
        std::cout << "pixelStrings[1] = \"" << pixelStrings[1] << "\"" << std::endl;
        std::cout << "pixelStrings[100] = \"" << pixelStrings[100] << "\"" << std::endl;
        
        // 7. 제곱 연산 테스트
        auto squaredPixels = processor.parallel_map(pixelData, [](int pixel) {
            return pixel * pixel;
        });
        
        std::cout << "\n// squaredPixels results" << std::endl;
        std::cout << "squaredPixels[0] = " << squaredPixels[0] << std::endl;
        std::cout << "squaredPixels[1] = " << squaredPixels[1] << std::endl;
        std::cout << "squaredPixels[10] = " << squaredPixels[10] << std::endl;
        
        // 8. 성능 측정 결과 출력
        std::cout << "\n// Performance measurement results" << std::endl;
        std::cout << "Processing 1,000,000 elements with 4 threads" << std::endl;
        std::cout << "Sequential time: ~" << sequential_time.count() << "ms" << std::endl;
        std::cout << "Parallel time: ~" << parallel_time.count() << "ms" << std::endl;
        
        // 9. 성능 향상 배수 계산
        double speedup = static_cast<double>(sequential_time.count()) / parallel_time.count();
        std::cout << "Speedup: " << std::fixed << std::setprecision(2) << speedup << "x" << std::endl;
        
        std::cout << "\n=== Test Completed ===" << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "Error occurred: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}