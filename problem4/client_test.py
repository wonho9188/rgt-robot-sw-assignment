import requests
import json

BASE_URL = "http://localhost:8000"

class LibraryAPIClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.token = None
    
    def signup(self, username, email, password, full_name):
        """Register a new user"""
        data = {
            "username": username,
            "email": email,
            "password": password,
            "full_name": full_name
        }
        response = requests.post(f"{self.base_url}/auth/signup", json=data)
        return response.json()
    
    def login(self, username, password):
        """Login and get access token"""
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
        """Get authorization headers"""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}
    
    def get_profile(self):
        """Get current user profile"""
        response = requests.get(f"{self.base_url}/auth/me", headers=self.get_headers())
        return response.json()
    
    def create_book(self, title, author, isbn, category, published_year, total_copies):
        """Create a new book"""
        data = {
            "title": title,
            "author": author,
            "isbn": isbn,
            "category": category,
            "published_year": published_year,
            "total_copies": total_copies
        }
        response = requests.post(f"{self.base_url}/books/", json=data, headers=self.get_headers())
        return response.json()
    
    def get_books(self):
        """Get all books"""
        response = requests.get(f"{self.base_url}/books/")
        return response.json()
    
    def get_book(self, book_id):
        """Get a specific book"""
        response = requests.get(f"{self.base_url}/books/{book_id}")
        return response.json()
    
    def borrow_book(self, book_id, user_id):
        """Borrow a book"""
        data = {
            "book_id": book_id,
            "user_id": user_id
        }
        response = requests.post(f"{self.base_url}/loans/", json=data, headers=self.get_headers())
        return response.json()
    
    def return_book(self, loan_id):
        """Return a book"""
        response = requests.put(f"{self.base_url}/loans/{loan_id}/return", headers=self.get_headers())
        return response.json()
    
    def get_my_loans(self):
        """Get current user's loans"""
        response = requests.get(f"{self.base_url}/loans/my-loans", headers=self.get_headers())
        return response.json()

# Example usage
if __name__ == "__main__":
    client = LibraryAPIClient()
    
    print("=== Library Management API Test Client ===")
    
    # Test registration
    print("\n1. Testing user registration...")
    try:
        result = client.signup("testuser", "test@example.com", "testpassword", "Test User")
        print(f"Registration result: {result}")
    except Exception as e:
        print(f"Registration error: {e}")
    
    # Test login
    print("\n2. Testing user login...")
    try:
        result = client.login("testuser", "testpassword")
        print(f"Login result: {result}")
    except Exception as e:
        print(f"Login error: {e}")
    
    # Test profile
    print("\n3. Testing user profile...")
    try:
        result = client.get_profile()
        print(f"Profile result: {result}")
    except Exception as e:
        print(f"Profile error: {e}")
    
    # Test create book
    print("\n4. Testing book creation...")
    try:
        result = client.create_book("Test Book", "Test Author", "123456789", "Fiction", 2023, 5)
        print(f"Book creation result: {result}")
    except Exception as e:
        print(f"Book creation error: {e}")
    
    # Test get books
    print("\n5. Testing get books...")
    try:
        result = client.get_books()
        print(f"Books result: {result}")
    except Exception as e:
        print(f"Get books error: {e}")