from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import RedirectResponse

from app.schemas.auth import SignUpRequest, SignInRequest, AuthResponse
from app.dependencies.services import get_services, Services

router = APIRouter(prefix="/api/auth", tags=["인증"])

@router.post(
    "/signup", 
    response_model=AuthResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="이메일, 비밀번호 회원가입",
    description="""
    새로운 사용자 계정을 생성합니다.
    
    - 이메일 중복 확인이 자동으로 수행됩니다.
    - 비밀번호는 최소 8자 이상이어야 합니다.
    - 가입 후 이메일 인증이 필요할 수 있습니다.
    
    **반환값**:
    - `user`: 생성된 사용자 정보
    - `session`: 인증 세션 정보 (액세스/리프레시 토큰)
    """
)
def sign_up(
    payload: SignUpRequest, 
    services: Services = Depends(get_services)
):
    """
    새로운 사용자 계정을 생성합니다.
    """
    return services.auth.sign_up(payload)

@router.post(
    "/login", 
    response_model=AuthResponse, 
    status_code=status.HTTP_200_OK,
    summary="이메일, 비밀번호 로그인",
    description="""
    기존 계정으로 로그인합니다.
    
    - 이메일과 비밀번호를 검증합니다.
    - 로그인 성공 시 액세스 토큰과 리프레시 토큰이 발급됩니다.
    - 로그인 실패 시 401 Unauthorized 오류가 발생합니다.
    
    **참고**:
    - 소셜 로그인은 `/oauth` 엔드포인트를 사용하세요.
    """
)
def sign_in(
    payload: SignInRequest, 
    services: Services = Depends(get_services)
):
    """
    기존 계정으로 로그인합니다.
    """
    return services.auth.sign_in(payload)


@router.get(
    "/oauth", 
    status_code=status.HTTP_307_TEMPORARY_REDIRECT, 
    summary="OAuth 로그인 시작",
    description="""
    소셜 로그인(OAuth) 인증 과정을 시작합니다.
    
    - `provider` 파라미터로 인증 제공자를 지정합니다(google 또는 kakao).
    - 사용자는 해당 제공자의 인증 페이지로 리다이렉트됩니다.
    - 인증 성공 후 Supabase가 설정된 콜백 URL로 리다이렉트합니다.
    
    **provider**:
    - Google (`provider=google`)
    - Kakao (`provider=kakao`)
    """
)
def oauth_redirect(
    provider: str = Query(..., description="`google` 또는 `kakao`"), 
    services: Services = Depends(get_services)
):
    """
    OAuth 인증 페이지로 리다이렉트합니다.
    """
    url = services.auth.get_oauth_redirect_url(provider)
    return RedirectResponse(url)
