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
    """Create a new loan (borrow a book)"""
    # Check if book exists and is available
    book = crud.get_book(db, book_id=loan.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.is_available:
        raise HTTPException(status_code=400, detail="Book is not available")
    
    # Create loan
    db_loan = crud.create_loan(db=db, loan=loan)
    
    # Update book availability
    crud.update_book_availability(db, book_id=loan.book_id, is_available=False)
    
    return db_loan

@router.put("/{loan_id}/return")
def return_book(loan_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """Return a borrowed book"""
    db_loan = crud.return_book(db, loan_id=loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    # Update book availability
    crud.update_book_availability(db, book_id=db_loan.book_id, is_available=True)
    
    return {"message": "Book returned successfully"}

@router.get("/my-loans", response_model=List[schemas.Loan])
def get_my_loans(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """Get current user's loans"""
    return crud.get_user_loans(db, user_id=current_user.id)