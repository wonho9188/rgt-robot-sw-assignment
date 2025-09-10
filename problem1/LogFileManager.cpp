#include "LogFileManager.h"

// 기본 생성자 및 소멸자
LogFileManager::LogFileManager() {}
LogFileManager::~LogFileManager() {}

// 로그 파일 관리 메서드
void LogFileManager::openLogFile(const std::string& filename) {
    if (logFiles.find(filename) == logFiles.end()) {
        logFiles[filename] = std::make_unique<std::fstream>(filename, std::ios::in | std::ios::out | std::ios::app);
    }
}

void LogFileManager::writeLog(const std::string& filename, const std::string& message) {
    auto it = logFiles.find(filename);
    if (it != logFiles.end() && it->second && it->second->is_open()) {
        *(it->second) << message << std::endl;
    }
}

std::vector<std::string> LogFileManager::readLogs(const std::string& filename) {
    std::vector<std::string> logs;
    std::ifstream file(filename);
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