from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import AppException
from app.models.user import User
from app.schemas.auth import SignupRequest, UserResponse
from app.security import hash_password


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise AppException("Email is already registered", status_code=409)

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_active=True,
    )

    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise AppException("Email is already registered", status_code=409) from exc

    db.refresh(user)
    return user
