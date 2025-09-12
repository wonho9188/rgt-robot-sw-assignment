from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    """User model for authentication and user management"""
    __tablename__ = "users"
    
    # TODO: Define user table columns
    pass

class Book(Base):
    """Book model for library inventory"""
    __tablename__ = "books"
    
    # TODO: Define book table columns
    pass

class Loan(Base):
    """Loan model for tracking book borrowing"""
    __tablename__ = "loans"
    
    # TODO: Define loan table columns and relationships
    pass