import logging
from logging.config import dictConfig
import sys
from typing import ClassVar, Dict, Any, List
from pydantic import BaseModel, Field
from app.core.config import settings

class LogConfig(BaseModel):
    """로깅 설정"""
    
    # ClassVar로 타입 어노테이션 추가
    version: ClassVar[int] = 1
    disable_existing_loggers: ClassVar[bool] = False
    LOGGER_NAME: str = "mumul_edu"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"
    
    @staticmethod
    def get_config() -> Dict[str, Any]:
        log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
        
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": sys.stdout,
                    "formatter": "default",
                    "level": log_level,
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "logs/app.log",
                    "formatter": "default",
                    "maxBytes": 10485760,  # 10MB
                    "backupCount": 5,
                    "level": log_level,
                },
            },
            "loggers": {
                "app": {
                    "handlers": ["console", "file"],
                    "level": log_level,
                    "propagate": False,
                },
                "uvicorn": {
                    "handlers": ["console", "file"],
                    "level": log_level,
                },
                "fastapi": {
                    "handlers": ["console", "file"],
                    "level": log_level,
                },
            },
        }

# 로그 디렉토리 생성
def setup_logging():
    """애플리케이션 로깅 설정"""
    import os
    
    # logs 디렉토리 생성
    os.makedirs("logs", exist_ok=True)
    
    # 로깅 설정 적용
    dictConfig(LogConfig.get_config())
    
    # 루트 로거 설정
    logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    
    return logging.getLogger("app")

# 로거 인스턴스 생성
logger = setup_logging()
