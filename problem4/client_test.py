import requests
import json

BASE_URL = "http://localhost:8000"

class LibraryAPIClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.token = None
    
    def signup(self, username, email, password, full_name):
        """새 사용자 등록"""
        data = {
            "username": username,
            "email": email,
            "password": password,
            "full_name": full_name
        }
        response = requests.post(f"{self.base_url}/auth/signup", json=data)
        return response.json()
    
    def login(self, username, password):
        """로그인 및 액세스 토큰 획득"""
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(f"{self.base_url}/auth/login", data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data["access_token"]
        return response.json()
    
    def get_headers(self):
        """인증 헤더 가져오기"""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}
    
    def get_profile(self):
        """현재 사용자 프로필 조회"""
        response = requests.get(f"{self.base_url}/auth/me", headers=self.get_headers())
        return response.json()
    
    def create_book(self, title, author, isbn, category, total_copies):
        """새 도서 생성"""
        data = {
            "title": title,
            "author": author,
            "isbn": isbn,
            "category": category,
            "total_copies": total_copies
        }
        response = requests.post(f"{self.base_url}/books/", json=data, headers=self.get_headers())
        return response.json()
    
    def get_books(self):
        """모든 도서 조회"""
        response = requests.get(f"{self.base_url}/books/")
        return response.json()
    
    def get_book(self, book_id):
        """특정 도서 조회"""
        response = requests.get(f"{self.base_url}/books/{book_id}")
        return response.json()
    
    def borrow_book(self, book_id, user_id):
        """도서 대출"""
        data = {
            "book_id": book_id,
            "user_id": user_id
        }
        response = requests.post(f"{self.base_url}/loans/", json=data, headers=self.get_headers())
        return response.json()
    
    def return_book(self, loan_id):
        """도서 반납"""
        response = requests.put(f"{self.base_url}/loans/{loan_id}/return", headers=self.get_headers())
        return response.json()
    
    def get_my_loans(self):
        """현재 사용자의 대출 목록 조회"""
        response = requests.get(f"{self.base_url}/loans/my-loans", headers=self.get_headers())
        return response.json()

# 사용 예시
if __name__ == "__main__":
    client = LibraryAPIClient()
    
    print("=== 도서관 관리 API 테스트 클라이언트 ===")
    
    # 회원가입 테스트
    print("\n1. 사용자 등록 테스트...")
    try:
        result = client.signup("testuser", "test@example.com", "testpassword", "Test User")
        print(f"Registration result: {result}")
    except Exception as e:
        print(f"Registration error: {e}")
    
    # 로그인 테스트
    print("\n2. 사용자 로그인 테스트...")
    try:
        result = client.login("testuser", "testpassword")
        print(f"Login result: {result}")
    except Exception as e:
        print(f"Login error: {e}")
    
    # 프로필 조회 테스트
    print("\n3. 사용자 프로필 테스트...")
    try:
        result = client.get_profile()
        print(f"Profile result: {result}")
    except Exception as e:
        print(f"Profile error: {e}")
    
    # 도서 생성 테스트
    print("\n4. 도서 생성 테스트...")
    try:
        result = client.create_book("Test Book", "Test Author", "123456789", "Fiction", 5)
        print(f"Book creation result: {result}")
    except Exception as e:
        print(f"Book creation error: {e}")
    
    # 도서 목록 조회 테스트
    print("\n5. 도서 목록 조회 테스트...")
    try:
        result = client.get_books()
        print(f"Books result: {result}")
    except Exception as e:
        print(f"Get books error: {e}")