from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash, verify_password
from datetime import datetime, timedelta

# 사용자 CRUD 작업
def get_user(db: Session, user_id: int):
    """ID로 사용자 조회"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """사용자명으로 사용자 조회"""
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """이메일로 사용자 조회"""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """새 사용자 생성"""
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
    """사용자 인증"""
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    """사용자 정보 업데이트"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.username = user.username
        db_user.email = user.email
        db_user.full_name = user.full_name
        if user.password:  # 비밀번호가 제공된 경우에만 업데이트
            db_user.hashed_password = get_password_hash(user.password)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """사용자 계정 삭제"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# 도서 CRUD 작업
def get_book(db: Session, book_id: int):
    """ID로 도서 조회"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    """모든 도서 조회"""
    return db.query(models.Book).offset(skip).limit(limit).all()

def search_books_by_title(db: Session, title: str):
    """제목으로 도서 검색 (대소문자 구분 없는 부분 일치)"""
    return db.query(models.Book).filter(models.Book.title.ilike(f"%{title}%")).all()

def create_book(db: Session, book: schemas.BookCreate):
    """새 도서 생성"""
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book_availability(db: Session, book_id: int, is_available: bool):
    """도서 대출 가능 상태 업데이트"""
    db_book = get_book(db, book_id)
    if db_book:
        db_book.is_available = is_available
        db.commit()
        db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    """도서 정보 업데이트"""
    db_book = get_book(db, book_id)
    if db_book:
        db_book.title = book.title
        db_book.author = book.author
        db_book.isbn = book.isbn
        db_book.category = book.category
        db_book.total_copies = book.total_copies
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    """도서 삭제"""
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    
    # 현재 대출 중인 도서가 있는지 확인 (아직 반납되지 않은 대출)
    active_loans = db.query(models.Loan).filter(
        models.Loan.book_id == book_id,
        models.Loan.is_returned == False
    ).first()
    
    if active_loans:
        return "has_active_loans"  # 현재 대출 중임을 나타내는 특별한 값 반환
    
    # 반납된 대출 기록들을 먼저 삭제 (외래 키 제약 조건 해결)
    returned_loans = db.query(models.Loan).filter(
        models.Loan.book_id == book_id,
        models.Loan.is_returned == True
    ).all()
    
    for loan in returned_loans:
        db.delete(loan)
    
    # 이제 도서 삭제
    db.delete(db_book)
    db.commit()
    return db_book

# 대출 CRUD 작업
def create_loan(db: Session, loan: schemas.LoanCreate):
    """새 대출 생성"""
    db_loan = models.Loan(
        user_id=loan.user_id,
        book_id=loan.book_id,
        due_date=datetime.utcnow() + timedelta(days=14)  # 2주 대출 기간
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def return_book(db: Session, loan_id: int):
    """도서 반납"""
    db_loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if db_loan and not db_loan.is_returned:
        db_loan.return_date = datetime.utcnow()
        db_loan.is_returned = True
        db.commit()
        db.refresh(db_loan)
    return db_loan

def get_user_loans(db: Session, user_id: int):
    """사용자의 모든 대출 조회"""
    return db.query(models.Loan).filter(models.Loan.user_id == user_id).all()