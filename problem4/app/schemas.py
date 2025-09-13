from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# 사용자 스키마
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# 도서 스키마
class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    category: str
    total_copies: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    is_available: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# 대출 스키마
class LoanBase(BaseModel):
    user_id: int
    book_id: int

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int
    loan_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    is_returned: bool
    
    class Config:
        from_attributes = True

# 인증 스키마
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None