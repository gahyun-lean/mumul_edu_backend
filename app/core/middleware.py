from fastapi import FastAPI, Request, Response
import time
from app.core.logging import logger

# 요청 로깅 미들웨어
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
