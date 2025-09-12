
# rgt-robot-sw-assignment
### 개요
- 로봇 소프트웨어 개발 역량 평가를 위한 과제 모음
- 각 문제는 별도 폴더에 정리되어 있습니다.

### 폴더 구조
```
rgt-robot-sw-assignment/
│
├─ problem1/   # 문제 1: 스마트 포인터를 활용한 리소스 관리
├─ problem2/   # 문제 2: 템플릿과 STL을 활용한 컨테이너 설계
├─ problem3/   # 문제 3: 멀티스레딩과 함수형 프로그래밍을 활용한 병렬 처리
├─ problem4/   # 문제 4: (추가 예정)
└─ problem5/   # 문제 5: (추가 예정)
```

### 문제별 안내
- 각 문제 폴더에 상세 설명 및 예시, 코드가 포함되어 있습니다.
- 보안상 문제 원문 대신 핵심 역량 및 작업 포인트 위주로 정리되어 있습니다.

### 빌드 및 실행 방법
- 각 문제 폴더의 README.md 참고

### 커밋 메세지 형식
- 형식 : [타입] 문제번호 : 작업 요약

| 타입      | 설명                           |
|-----------|-------------------------------|
| feat      | 새로운 기능/구현               |
| fix       | 버그 수정                      |
| docs      | 문서/README 수정               |
| refactor  | 리팩토링(동작 변화 없음)        |
| test      | 테스트 코드 추가/수정           |
| chore     | 기타(빌드, 설정 등)            |

 - 예시:
```
[feat] problem1: LogFileManager 클래스 선언
[fix] problem1: 파일 열기 예외 처리 추가
[docs] problem1: README 핵심 역량 정리
```

--- 
### 실행 환경 및 설치 안내

- **운영체제:** Windows 10/11
- **필수 소프트웨어:**
  - [MSYS2](https://www.msys2.org/) 또는 [MinGW-w64](https://www.mingw-w64.org/) (g++ 컴파일러 포함)

#### MSYS2/MinGW-w64 설치 및 g++ 사용법
1. MSYS2 또는 MinGW-w64 설치 후, 환경 변수 PATH에 `mingw64\bin` 폴더 추가
2. MSYS2 터미널(MINGW64)에서 아래 명령어 실행:
    ```
    (1번 문제 예시)
    cd /c/Users/본인계정/Desktop/rgt-robot-sw-assignment/problem1 (예시 경로입니다. 해당 레포지토리가 저장된 경로에 맞춰주세요.)
    g++ -std=c++17 -o test main.cpp LogFileManager.cpp
    ./test.exe
    ```

#### Visual Studio 사용법
1. Visual Studio에서 새 콘솔 프로젝트 생성
2. main.cpp, LogFileManager.cpp, LogFileManager.h 파일을 프로젝트에 추가
3. 빌드 후 실행

---
### g++ 컴파일 안될 때
MSYS2의 bin 폴더(예: bin)를 Windows 환경 변수 PATH에 추가해야
Windows 터미널(명령 프롬프트, PowerShell, VS Code 터미널 등)에서 g++ 명령을 쓸 수 있습니다.

추가 방법

bin 폴더 경로 복사 (예: `C:\msys64\mingw64\bin`)

환경 변수 편집
```
Windows 검색창에 “환경 변수” 입력 →
시스템 환경 변수 편집 클릭 →
아래쪽 “환경 변수(N)...” 버튼 클릭
“시스템 변수” 또는 “사용자 변수”에서 Path 선택 → “편집” 클릭
“새로 만들기” 클릭 →
bin 폴더 경로 붙여넣기 → “확인”으로 창 닫기
터미널 재시작
```

모든 터미널(명령 프롬프트, PowerShell, VS Code 터미널 등)을 완전히 닫았다가 다시 엽니다.