from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from app.core.logging import logger
from app.core.exceptions import APIError
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.core.config import settings

from app.routers import (
    auth_router,
    profiles_router,
    courses_router,
    course_codes_router,
    enrollments_router,
    documents_router,
    # chat_router,
)

app = FastAPI(
    title="Mumul Edu API",
    version="0.1.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "defaultModelExpandDepth": -1,
        "defaultModelRendering": "example",
        "docExpansion": "list",
        "showRequestHeaders": True,
        "filter": True,
        "displayRequestDuration": True,
        "persistAuthorization": True,
    },
)

# (선택) CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Authorization", 
        "Content-Type", 
        "Accept", 
        "Origin", 
        "X-Requested-With",
        "X-CSRF-Token",
    ],
    expose_headers=[
        "X-RateLimit-Limit", 
        "X-RateLimit-Remaining", 
        "X-RateLimit-Reset"
    ],
    max_age=600  # 프리플라이트 캐시 시간 (초)
)

# 인증 관련 (OAuth, SignUp, SignIn 등)
app.include_router(auth_router)

# 프로필 생성/조회
app.include_router(profiles_router)

# 강의(Courses) 관리
app.include_router(courses_router)

# 수강 코드(Course Codes) 관리
app.include_router(course_codes_router)

# 수강 등록(Enrollments) 관리
app.include_router(enrollments_router)

# 문서 파싱 관리
app.include_router(documents_router)

# 챗 및 파일 업로드
# app.include_router(chat_router)



# HTTPS 리다이렉트 미들웨어 (프로덕션 환경에서만 활성화)
if settings.ENVIRONMENT != "development":
    app.add_middleware(
        HTTPSRedirectMiddleware,
        https_enabled=True
    )


# 전역 예외 핸들러
@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    logger.error(f"API 오류: {exc.detail}", 
                extra={"path": request.url.path, "status_code": exc.status_code})
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# 미들웨어 - 요청 로깅
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # 요청 로깅
    logger.info(
        f"요청 시작: {request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else None,
        }
    )
    
    # 응답 처리
    response = await call_next(request)
    
    # 처리 시간 계산
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}ms"
    
    # 응답 로깅
    logger.info(
        f"요청 완료: {request.method} {request.url.path} - {response.status_code} ({formatted_process_time})",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "processing_time": formatted_process_time,
        }
    )
    
    return response
