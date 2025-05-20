from app.schemas.base import BaseSchema
from app.schemas.types import EmailString, DateTime
from pydantic import Field, EmailStr, field_validator
from typing import Optional, Dict, Any


class SignUpRequest(BaseSchema):
    email: EmailStr
    password: str

    @field_validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('비밀번호는 8자 이상이어야 합니다')
        if not any(char.isdigit() for char in v):
            raise ValueError('비밀번호는 최소 하나의 숫자를 포함해야 합니다')
        if not any(char in '!@#$%^&*()_+' for char in v):
            raise ValueError('비밀번호는 최소 하나의 특수문자를 포함해야 합니다')
        return v


class SignInRequest(BaseSchema):
    email: EmailStr
    password: str


class SignUpUser(BaseSchema):
    id: str
    email: str
    email_confirmed_at: Optional[DateTime] = None


class AuthSession(BaseSchema):
    access_token: str
    refresh_token: str
    expires_at: int


class AuthResponse(BaseSchema):
    user: Dict[str, Any]
    session: Optional[AuthSession] = None
    error: Optional[str] = None


