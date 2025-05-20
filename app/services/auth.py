from fastapi import HTTPException, status
from httpx import HTTPStatusError

from app.schemas.auth import (
    SignUpRequest,
    SignInRequest,
    AuthResponse,
    SignUpUser,
    AuthSession,
)
from app.core.config import settings


class AuthService:
    def __init__(self, supabase):
        self.supabase = supabase

    def sign_up(self, payload: SignUpRequest) -> AuthResponse:
        try:
            raw = self.supabase.auth.sign_up({
                "email":    payload.email,
                "password": payload.password,
            })
        except HTTPStatusError as e:
            # GoTrue HTTP 에러
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.response.text or str(e),
            )

        if raw.error:
            msg = raw.error.message or str(raw.error)
            if any(keyword in msg.lower() for keyword in ("duplicate", "already")):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="이미 존재하는 이메일입니다.",
                )
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

        # 스펙에 맞춘 SignUpUser 생성
        user = raw.user
        user_data = SignUpUser(
            id                   = user.id,
            email                = user.email,
            email_confirmed_at   = user.email_confirmed_at,
        )

        # 세션 매핑
        session = raw.session
        session_data = (
            AuthSession(
                access_token = session.access_token,
                refresh_token= session.refresh_token,
                expires_at   = session.expires_at,
            )
            if session else None
        )

        # SignUpUser 인스턴스를 dict로 변환하여 전달
        return AuthResponse(
            user=user_data.model_dump(),
            session=session_data,
            error=None,
        )


    def sign_in(self, payload: SignInRequest) -> AuthResponse:
        raw = self.supabase.auth.sign_in_with_password({
            "email":    payload.email,
            "password": payload.password,
        })

        if raw.error:
            msg = raw.error.message or str(raw.error)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)

        user = raw.user
        user_data = {
            "id": user.id,
            "email": user.email,
            "email_confirmed_at": user.email_confirmed_at,
        }

        session = raw.session
        session_data = (
            AuthSession(
                access_token = session.access_token,
                refresh_token= session.refresh_token,
                expires_at   = session.expires_at,
            )
            if session else None
        )

        return AuthResponse(user=user_data, session=session_data, error=None)

    def get_oauth_redirect_url(self, provider: str) -> str:
        base = settings.SUPABASE_URL
        return f"{base}/auth/v1/authorize?provider={provider}"
