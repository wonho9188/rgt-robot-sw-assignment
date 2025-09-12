from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash, verify_password
from datetime import datetime, timedelta

# User CRUD operations
def get_user(db: Session, user_id: int):
    """Get user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """Get user by username"""
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """Get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Create new user"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate user"""
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Book CRUD operations
def get_book(db: Session, book_id: int):
    """Get book by ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    """Get all books"""
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    """Create new book"""
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book_availability(db: Session, book_id: int, is_available: bool):
    """Update book availability"""
    db_book = get_book(db, book_id)
    if db_book:
        db_book.is_available = is_available
        db.commit()
        db.refresh(db_book)
    return db_book

# Loan CRUD operations
def create_loan(db: Session, loan: schemas.LoanCreate):
    """Create new loan"""
    db_loan = models.Loan(
        user_id=loan.user_id,
        book_id=loan.book_id,
        due_date=datetime.utcnow() + timedelta(days=14)  # 2 weeks loan period
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def return_book(db: Session, loan_id: int):
    """Return book"""
    db_loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if db_loan and not db_loan.is_returned:
        db_loan.return_date = datetime.utcnow()
        db_loan.is_returned = True
        db.commit()
        db.refresh(db_loan)
    return db_loan

def get_user_loans(db: Session, user_id: int):
    """Get all loans for a user"""
    return db.query(models.Loan).filter(models.Loan.user_id == user_id).all()