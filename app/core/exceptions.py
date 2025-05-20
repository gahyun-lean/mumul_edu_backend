from fastapi import HTTPException, status

class APIError(HTTPException):
    """기본 API 에러 클래스"""
    def __init__(self, status_code: int, detail: str, headers: dict = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

# 404 - 리소스를 찾을 수 없음
class ResourceNotFound(APIError):
    def __init__(self, resource: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{resource}를 찾을 수 없습니다."
        )

# 403 - 권한 없음
class PermissionDenied(APIError):
    def __init__(self, message: str = "이 작업을 수행할 권한이 없습니다."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=message
        )

# 401 - 인증 실패
class AuthenticationFailed(APIError):
    def __init__(self, message: str = "인증에 실패했습니다."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=message
        )

# 409 - 충돌 (이미 존재하는 리소스)
class ResourceAlreadyExists(APIError):
    def __init__(self, resource: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"{resource}가 이미 존재합니다."
        )

# 400 - 잘못된 요청
class BadRequest(APIError):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=message
        )

# 500 - 서버 에러
class ServerError(APIError):
    def __init__(self, message: str = "서버 내부 오류가 발생했습니다."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

# 데이터베이스 에러
class DatabaseError(ServerError):
    def __init__(self, message: str = "데이터베이스 작업 중 오류가 발생했습니다."):
        super().__init__(message)

# 외부 서비스 에러
class ExternalServiceError(ServerError):
    def __init__(self, service: str, message: str = None):
        detail = f"{service} 서비스와 통신 중 오류가 발생했습니다."
        if message:
            detail += f" 세부 내용: {message}"
        super().__init__(detail)
