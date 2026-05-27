from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class SignupRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized_email = value.strip().lower()
        if "@" not in normalized_email or "." not in normalized_email.split("@")[-1]:
            raise ValueError("A valid email address is required")
        return normalized_email

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    is_active: bool
    created_at: datetime
