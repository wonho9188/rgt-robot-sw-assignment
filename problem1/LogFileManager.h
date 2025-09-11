#pragma once
#include <string>
#include <vector>
#include <memory>
#include <map>
#include <fstream>

class LogFileManager {
public:
    LogFileManager();
    ~LogFileManager();

    // 열기/쓰기/읽기/닫기 메서드
    void openLogFile(const std::string& filename);
    void writeLog(const std::string& filename, const std::string& message);
    std::vector<std::string> readLogs(const std::string& filename);
    void closeLogFile(const std::string& filename);

    // 복사/이동 생성자 및 대입 연산자
    LogFileManager(const LogFileManager& other);
    LogFileManager& operator=(const LogFileManager& other);
    LogFileManager(LogFileManager&& other) noexcept;
    LogFileManager& operator=(LogFileManager&& other) noexcept;

private:
    std::map<std::string, std::shared_ptr<std::fstream>> logFiles;
};