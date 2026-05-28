from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.exceptions import AppException
from app.models.user import User
from app.services.user_service import get_user_by_id

settings = get_settings()

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise AppException(
            "Authentication credentials were not provided",
            status_code=401,
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except ExpiredSignatureError as exc:
        raise AppException("Token has expired", status_code=401) from exc
    except JWTError as exc:
        raise AppException("Invalid authentication token", status_code=401) from exc

    user_id = payload.get("user_id")
    email = payload.get("sub")

    if user_id is None or not email:
        raise AppException("Invalid authentication token", status_code=401)

    user = get_user_by_id(db, user_id)
    if not user or user.email != email:
        raise AppException("Invalid authentication token", status_code=401)

    if not user.is_active:
        raise AppException("User account is inactive", status_code=403)

    return user
