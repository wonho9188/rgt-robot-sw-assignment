from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    # TODO: Define base user fields
    pass

class UserCreate(UserBase):
    # TODO: Define user creation fields
    pass

class User(UserBase):
    # TODO: Define user response fields
    pass

# Book Schemas
class BookBase(BaseModel):
    # TODO: Define base book fields
    pass

class BookCreate(BookBase):
    # TODO: Define book creation fields
    pass

class Book(BookBase):
    # TODO: Define book response fields
    pass

# Loan Schemas
class LoanBase(BaseModel):
    # TODO: Define base loan fields
    pass

class LoanCreate(LoanBase):
    # TODO: Define loan creation fields
    pass

class Loan(LoanBase):
    # TODO: Define loan response fields
    pass

# Authentication Schemas
class Token(BaseModel):
    # TODO: Define token response fields
    pass

class TokenData(BaseModel):
    # TODO: Define token data fields
    pass