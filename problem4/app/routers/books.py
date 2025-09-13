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
    """새 도서 생성"""
    return crud.create_book(db=db, book=book)

@router.get("/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """모든 도서 조회"""
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@router.get("/search/", response_model=List[schemas.Book])
def search_books_by_title(title: str, db: Session = Depends(get_db)):
    """제목으로 도서 검색"""
    books = crud.search_books_by_title(db, title=title)
    if not books:
        raise HTTPException(status_code=404, detail="No books found with that title")
    return books

@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """ID로 특정 도서 조회"""
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.put("/{book_id}/availability")
def update_book_availability(book_id: int, is_available: bool, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """도서 대출 가능 상태 업데이트"""
    db_book = crud.update_book_availability(db, book_id=book_id, is_available=is_available)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book availability updated successfully"}

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """도서 정보 업데이트"""
    db_book = crud.update_book(db, book_id=book_id, book=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """도서 삭제"""
    result = crud.delete_book(db, book_id=book_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    elif result == "has_active_loans":
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete book: Book is currently borrowed. Please wait for return."
        )
    return {"message": "Book deleted successfully"}