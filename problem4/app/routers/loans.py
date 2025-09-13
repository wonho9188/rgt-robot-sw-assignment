from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db
from .auth import get_current_user

router = APIRouter(
    prefix="/loans",
    tags=["loans"]
)

@router.post("/", response_model=schemas.Loan)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """새 대출 생성 (도서 대출)"""
    # 도서 존재 여부 및 대출 가능 여부 확인
    book = crud.get_book(db, book_id=loan.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.is_available:
        raise HTTPException(status_code=400, detail="Book is not available")
    
    # 대출 생성
    db_loan = crud.create_loan(db=db, loan=loan)
    
    # 도서 대출 가능 상태 업데이트
    crud.update_book_availability(db, book_id=loan.book_id, is_available=False)
    
    return db_loan

@router.put("/{loan_id}/return")
def return_book(loan_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """대출한 도서 반납"""
    db_loan = crud.return_book(db, loan_id=loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    # 도서 대출 가능 상태 업데이트
    crud.update_book_availability(db, book_id=db_loan.book_id, is_available=True)
    
    return {"message": "Book returned successfully"}

@router.get("/my-loans", response_model=List[schemas.Loan])
def get_my_loans(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """현재 사용자의 대출 목록 조회"""
    return crud.get_user_loans(db, user_id=current_user.id)