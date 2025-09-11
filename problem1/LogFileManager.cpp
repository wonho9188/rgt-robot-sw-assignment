#include "LogFileManager.h"
#include <chrono>
#include <iomanip>
#include <sstream>

// 기본 생성자 및 소멸자
LogFileManager::LogFileManager() {}
LogFileManager::~LogFileManager() {
    for (auto& pair : logFiles) {
        if (pair.second && pair.second->is_open()) {
            pair.second->close();
        }
    }
    logFiles.clear();
}

// 로그 파일 관리 메서드
void LogFileManager::openLogFile(const std::string& filename) {
    if (logFiles.find(filename) == logFiles.end()) {
        auto fs = std::make_unique<std::fstream>(filename, std::ios::in | std::ios::out | std::ios::app);
        if (!fs->is_open()) {
            throw std::runtime_error("파일 열기 실패: " + filename);
        }
        logFiles[filename] = std::move(fs);
    }
}

void LogFileManager::writeLog(const std::string& filename, const std::string& message) {
    auto it = logFiles.find(filename);
    if (it == logFiles.end() || !it->second || !it->second->is_open()) {
        throw std::runtime_error("파일이 열려있지 않음: " + filename);
    }

    // 타임스탬프 생성
    auto now = std::chrono::system_clock::now();
    std::time_t now_c = std::chrono::system_clock::to_time_t(now);
    std::tm tm;
#ifdef _WIN32
    localtime_s(&tm, &now_c);
#else
    localtime_r(&now_c, &tm);
#endif
    std::ostringstream oss;
    oss << "[" << std::put_time(&tm, "%Y-%m-%d %H:%M:%S") << "] " << message;

    *(it->second) << oss.str() << std::endl;
    if (it->second->fail()) {
        throw std::runtime_error("로그 쓰기 실패: " + filename);
    }
}

std::vector<std::string> LogFileManager::readLogs(const std::string& filename) {
    std::vector<std::string> logs;
    std::ifstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error("로그 파일 열기 실패: " + filename);
    }
    std::string line;
    while (std::getline(file, line)) {
        logs.push_back(line);
    }
    return logs;
}

void LogFileManager::closeLogFile(const std::string& filename) {
    auto it = logFiles.find(filename);
    if (it != logFiles.end()) {
        it->second->close();
        logFiles.erase(it);
    }
}

// 복사/이동 생성자 및 대입 연산자
LogFileManager::LogFileManager(const LogFileManager& other) {

}

LogFileManager& LogFileManager::operator=(const LogFileManager& other) {
    return *this;
}

LogFileManager::LogFileManager(LogFileManager&& other) noexcept {

}

LogFileManager& LogFileManager::operator=(LogFileManager&& other) noexcept {
    return *this;
}