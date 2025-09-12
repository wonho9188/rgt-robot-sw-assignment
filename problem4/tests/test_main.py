import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_read_root(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Library Management API"}

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_register_user(client):
    """Test user registration"""
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_login_user(client):
    """Test user login"""
    # First register a user
    client.post(
        "/auth/register",
        json={"username": "logintest", "email": "login@example.com", "password": "testpassword"}
    )
    
    # Then login
    response = client.post(
        "/auth/token",
        data={"username": "logintest", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_book(client):
    """Test book creation"""
    # Register and login user first
    client.post(
        "/auth/register",
        json={"username": "bookuser", "email": "book@example.com", "password": "testpassword"}
    )
    
    login_response = client.post(
        "/auth/token",
        data={"username": "bookuser", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create book
    response = client.post(
        "/books/",
        json={"title": "Test Book", "author": "Test Author", "isbn": "123456789", "published_year": 2023},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"

def test_get_books(client):
    """Test getting all books"""
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)