#include "LogFileManager.h"
#include <iostream>

int main() {
    LogFileManager manager;

    // 로그 파일 열기
    manager.openLogFile("error.log");
    manager.openLogFile("debug.log");

    // 로그 쓰기
    manager.writeLog("error.log", "Database connection failed");
    manager.writeLog("debug.log", "User login attempt");

    // 로그 읽기
    std::vector<std::string> errorLogs = manager.readLogs("error.log");
    std::cout << "error.log contents:" << std::endl;
    for (const auto& line : errorLogs) {
        std::cout << line << std::endl;
    }

    // 파일 닫기
    manager.closeLogFile("error.log");
    manager.closeLogFile("debug.log");

    return 0;
}