from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import AppException
from app.schemas.auth import LoginRequest, LoginResponse, SignupRequest, UserResponse
from app.security import hash_password, verify_password
from app.services.user_service import create_user, get_user_by_email
from app.token import create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, payload.email)
    if existing_user:
        raise AppException("Email is already registered", status_code=409)

    try:
        user = create_user(db, payload.email, hash_password(payload.password))
    except IntegrityError as exc:
        raise AppException("Email is already registered", status_code=409) from exc

    return user


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user:
        raise AppException("Invalid email or password", status_code=401)

    if not verify_password(payload.password, user.password_hash):
        raise AppException("Invalid email or password", status_code=401)

    if not user.is_active:
        raise AppException("User account is inactive", status_code=403)

    access_token = create_access_token({"sub": user.email, "user_id": user.id})

    return LoginResponse(
        message="Login credentials verified successfully",
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )
