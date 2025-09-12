from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db
from .auth import get_current_user

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """Create a new book"""
    return crud.create_book(db=db, book=book)

@router.get("/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all books"""
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Get a specific book by ID"""
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.put("/{book_id}/availability")
def update_book_availability(book_id: int, is_available: bool, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """Update book availability"""
    db_book = crud.update_book_availability(db, book_id=book_id, is_available=is_available)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book availability updated successfully"}