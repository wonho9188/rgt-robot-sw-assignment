# Problem 4 : Flask/FastAPI를 활용한 RESTful API 서버 구현 

온라인 도서관 관리 시스템의 백엔드 API를 구현하는 문제입니다. 사용자 인증, 도서 관리, 대출/반납 기능을 제공하는 RESTful API 서버를 작성합니다.

### 요구 역량
- **웹 프레임워크**: FastAPI/Flask 활용 능력
- **데이터베이스**: SQLAlchemy ORM, 관계형 데이터베이스 모델링
- **인증/보안**: JWT 토큰 기반 인증, 패스워드 해싱
- **RESTful API 설계**: HTTP 메서드(GET, POST, DELETE) 적절한 활용
- **데이터 검증**: Pydantic을 통한 입력 데이터 유효성 검사
- **에러 핸들링**: HTTP 상태 코드와 예외 처리
- **API 문서화**: 자동 생성되는 Swagger/OpenAPI 문서

### 주요 작업 포인트
1. **사용자 관리 시스템**
   - 회원가입 (`POST /auth/signup`)
   - 로그인 및 JWT 토큰 발급 (`POST /auth/login`)
   - 패스워드 해싱 (bcrypt)

2. **도서 관리 시스템**
   - 도서 추가 (`POST /books`) - 인증 필요
   - 도서 목록 조회 (`GET /books`)
   - 카테고리별 검색, 이용 가능한 도서 필터링
   - 도서 재고 관리 (total_copies, available_copies)

3. **대출/반납 시스템**
   - 도서 대출 (`POST /loans`) - 인증 필요
   - 내 대출 현황 조회 (`GET /users/me/loans`) - 인증 필요
   - 대출 날짜 관리, 반납 상태 추적

4. **데이터베이스 모델링**
   - User, Book, Loan 엔티티 간의 관계 설정
   - 외래키 제약조건 및 데이터 무결성 보장

5. **보안 및 인증**
   - Bearer 토큰 기반 API 접근 제어
   - 인증이 필요한 엔드포인트와 공개 엔드포인트 구분

### 예시

#### API 엔드포인트
```python
# 회원가입
POST /auth/signup
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "full_name": "John Doe"
}

# 로그인
POST /auth/login
{
    "username": "john_doe",
    "password": "securepass123"
}
# Response: {"access_token": "eyJ...", "token_type": "bearer"}

# 도서 추가 (인증 필요)
POST /books
Authorization: Bearer <token>
{
    "title": "Python Programming",
    "author": "John Smith",
    "isbn": "978-0123456789",
    "category": "Programming",
    "total_copies": 5
}

# 도서 검색
GET /books?category=Programming&available=true

# 도서 대출 (인증 필요)
POST /loans
Authorization: Bearer <token>
{
    "book_id": 1,
    "user_id": 1
}

# 내 대출 현황 (인증 필요)
GET /users/me/loans
Authorization: Bearer <token>
```

#### 데이터베이스 스키마
```python
# User 모델
class User(Base):
    id: int
    username: str (unique)
    email: str (unique)
    full_name: str
    hashed_password: str

# Book 모델  
class Book(Base):
    id: int
    title: str
    author: str
    isbn: str (unique)
    category: str
    total_copies: int
    available_copies: int

# Loan 모델
class Loan(Base):
    id: int
    book_id: int (ForeignKey)
    user_id: int (ForeignKey)
    loan_date: datetime
    return_date: datetime (nullable)
    is_returned: bool
```

#### 클라이언트 테스트 예시
```python
import requests

base_url = "http://localhost:8000"

# 1. 회원가입
signup_response = requests.post(f"{base_url}/auth/signup", json=signup_data)

# 2. 로그인 및 토큰 획득
auth_response = requests.post(f"{base_url}/auth/login", json=login_data)
token = auth_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 3. 인증이 필요한 API 호출
book_response = requests.post(f"{base_url}/books", json=book_data, headers=headers)
```

### 실행 방법

#### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

#### 2. 서버 실행
```bash
# 방법 1: Python으로 직접 실행
python main.py

# 방법 2: uvicorn으로 실행 (개발 모드)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. API 문서 확인
서버 실행 후 브라우저에서 접속:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### 4. 클라이언트 테스트
```bash
# 서버가 실행된 상태에서 별도 터미널에서
python client_test.py
```

#### 5. 프로젝트 구조
```
problem4/
├── app/
│   ├── __init__.py
│   ├── database.py        # 데이터베이스 연결 설정
│   ├── models.py          # SQLAlchemy 모델 (User, Book, Loan)
│   ├── schemas.py         # Pydantic 스키마
│   ├── auth.py           # JWT 인증 관련 함수
│   ├── crud.py           # 데이터베이스 CRUD 작업
│   └── routers/
│       ├── __init__.py
│       ├── auth.py       # 인증 API 엔드포인트
│       ├── books.py      # 도서 관리 API 엔드포인트
│       └── loans.py      # 대출/반납 API 엔드포인트
├── tests/
│   ├── __init__.py
│   └── test_main.py      # 단위 테스트
├── main.py               # FastAPI 앱 메인 파일
├── client_test.py        # API 테스트용 클라이언트
├── requirements.txt      # 패키지 의존성
└── README.md            # 프로젝트 문서
```

#### 6. 성능 확인 항목
- [ ] 회원가입/로그인 기능 동작
- [ ] JWT 토큰 기반 인증 작동
- [ ] 도서 CRUD 작업 수행
- [ ] 대출/반납 시스템 동작
- [ ] 데이터 검증 및 에러 처리
- [ ] API 문서 자동 생성
- [ ] 클라이언트 테스트 스크립트 통과

### 참고사항
- SQLite 데이터베이스를 사용하여 별도 DB 설치 불필요
- FastAPI의 자동 문서화 기능으로 API 명세 확인 가능
- Bearer 토큰 방식의 인증으로 보안성 확보
- 관계형 데이터베이스 설계로 데이터 일관성 보장