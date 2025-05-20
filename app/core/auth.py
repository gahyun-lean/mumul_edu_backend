from datetime import datetime, timedelta
from typing import Dict, Optional, Union
import jwt
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import AuthenticationFailed
from fastapi.security import OAuth2PasswordBearer

# OAuth2 인증 방식
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """액세스 토큰 생성"""
    to_encode = data.copy()
    
    # 만료 시간 설정
    expires = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expires})
    
    # JWT 토큰 생성
    try:
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.JWT_SECRET.get_secret_value(), 
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"JWT 토큰 생성 오류: {str(e)}")
        raise AuthenticationFailed("인증 토큰 생성에 실패했습니다.")

def create_refresh_token(data: Dict) -> str:
    """리프레시 토큰 생성"""
    to_encode = data.copy()
    
    # 만료 시간 설정 (리프레시 토큰은 더 긴 유효 기간)
    expires = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expires})
    
    # JWT 토큰 생성
    try:
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.JWT_SECRET.get_secret_value(), 
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"리프레시 토큰 생성 오류: {str(e)}")
        raise AuthenticationFailed("리프레시 토큰 생성에 실패했습니다.")

def verify_token(token: str) -> Dict:
    """토큰 검증"""
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET.get_secret_value(), 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("만료된 토큰 사용 시도")
        raise AuthenticationFailed("인증 토큰이 만료되었습니다.")
    except jwt.InvalidTokenError:
        logger.warning("유효하지 않은 토큰 사용 시도")
        raise AuthenticationFailed("유효하지 않은 인증 토큰입니다.")
