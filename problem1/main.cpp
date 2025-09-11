#include "LogFileManager.h"
#include <iostream>

int main() {
    LogFileManager manager;

    // 로그 파일 열기
    manager.openLogFile("error.log");
    manager.openLogFile("debug.log");
    manager.openLogFile("info.log");

    // 로그 쓰기
    manager.writeLog("error.log", "Database connection failed");
    manager.writeLog("debug.log", "User login attempt");
    manager.writeLog("info.log", "Server started successfully");

    // 로그 읽기
    std::vector<std::string> errorLogs = manager.readLogs("error.log");
    std::cout << "error.log contents:" << std::endl;
    for (const auto& line : errorLogs) {
        std::cout << line << std::endl;
    }
    std::cout << "errorLogs[0] = " << errorLogs[0] << std::endl;
    
    std::vector<std::string> debugLogs = manager.readLogs("debug.log");
    std::cout << "debug.log contents:" << std::endl;
    for (const auto& line : debugLogs) {
        std::cout << line << std::endl;
    }

    std::vector<std::string> infoLogs = manager.readLogs("info.log");
    std::cout << "info.log contents:" << std::endl;
    for (const auto& line : infoLogs) {
        std::cout << line << std::endl;
    }

    // 파일 닫기
    manager.closeLogFile("error.log");
    manager.closeLogFile("debug.log");
    manager.closeLogFile("info.log");

    return 0;
}