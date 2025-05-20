from fastapi import Depends, Header, HTTPException, status
from app.core.supabase_client import supabase

def get_bearer_token(authorization: str = Header(...)) -> str:
    """
    Authorization 헤더에서 Bearer 토큰만 분리하여 반환
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )
    return authorization.split(" ", 1)[1]
    
async def get_current_user(token: str = Depends(get_bearer_token)) -> dict:
    """
    Supabase Auth API를 이용해 토큰 검증 후 사용자 정보를 반환
    """
    user_resp = await supabase.auth.get_user(token)
    if user_resp.get("error"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    user = user_resp.get("user")
    if not user or not user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    return user  # {"id": "...", "email": "...", ...}

async def require_instructor(
    user: dict = Depends(get_current_user)
) -> dict:
    """
    강사 전용 엔드포인트 접근 제어
    """
    if user.get("id") is None:
        # 안전장치, 사실 get_current_user 에서 이미 검사됨
        raise HTTPException(status_code=401, detail="Unauthorized")
    # 추가로 profiles 테이블에서 role 검사 필요 시, 조회 후 검사
    profile = await supabase.from_("profiles").select("role").eq("id", user["id"]).single().execute()
    if profile.error or profile.data.get("role") != "instructor":
        raise HTTPException(status_code=403, detail="Instructor access required")
    return user

async def require_student(
    user: dict = Depends(get_current_user)
) -> dict:
    """
    수강생 전용 엔드포인트 접근 제어
    """
    profile = await supabase.from_("profiles").select("role").eq("id", user["id"]).single().execute()
    if profile.error or profile.data.get("role") != "student":
        raise HTTPException(status_code=403, detail="Student access required")
    return user
