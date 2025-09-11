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
    std::cout << std::endl;

    std::vector<std::string> debugLogs = manager.readLogs("debug.log");
    std::cout << "debug.log contents:" << std::endl;
    for (const auto& line : debugLogs) {
        std::cout << line << std::endl;
    }
    std::cout << std::endl;
    
    std::vector<std::string> infoLogs = manager.readLogs("info.log");
    std::cout << "info.log contents:" << std::endl;
    for (const auto& line : infoLogs) {
        std::cout << line << std::endl;
    }
    std::cout << std::endl;

    // 복사 생성자 테스트
    LogFileManager copyManager(manager);
    std::cout << "Copy Constructor - error.log:" << std::endl;
    for (const auto& line : copyManager.readLogs("error.log")) {
        std::cout << line << std::endl;
    }
    
    // 복사 대입 연산자 테스트
    LogFileManager assignManager;
    assignManager = manager;
    std::cout << "Copy Assignment Operator - error.log:" << std::endl;
    for (const auto& line : assignManager.readLogs("error.log")) {
        std::cout << line << std::endl;
    }

    // 이동 생성자 테스트
    LogFileManager moveManager(std::move(manager));
    std::cout << "Move Constructor - error.log:" << std::endl;
    for (const auto& line : moveManager.readLogs("error.log")) {
        std::cout << line << std::endl;
    }

    // 이동 대입 연산자 테스트
    LogFileManager moveAssignManager;
    moveAssignManager = std::move(copyManager);
    std::cout << "Move Assignment Operator - error.log:" << std::endl;
    for (const auto& line : moveAssignManager.readLogs("error.log")) {
        std::cout << line << std::endl;
    }

    // 파일 닫기
    moveManager.closeLogFile("error.log");
    moveManager.closeLogFile("debug.log");
    moveManager.closeLogFile("info.log");

    moveAssignManager.closeLogFile("error.log");
    moveAssignManager.closeLogFile("debug.log");
    moveAssignManager.closeLogFile("info.log");

    assignManager.closeLogFile("error.log");
    assignManager.closeLogFile("debug.log");
    assignManager.closeLogFile("info.log");

    return 0;
}