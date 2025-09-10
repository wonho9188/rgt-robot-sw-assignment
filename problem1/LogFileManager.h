// LogFileManager.h

#ifndef LOG_FILE_MANAGER_H
#define LOG_FILE_MANAGER_H

#include <string>
#include <fstream>
#include <iostream>
#include <mutex>

class LogFileManager {
public:
    LogFileManager(const std::string& filename);
    ~LogFileManager();

    void log(const std::string& message);

private:
    std::ofstream logFile;
    std::mutex logMutex;
};

#endif // LOG_FILE_MANAGER_H