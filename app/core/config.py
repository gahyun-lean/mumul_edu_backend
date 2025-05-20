from pydantic import field_validator, Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional, Any
import os
from pathlib import Path

# 앱 루트 디렉토리 찾기
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = ROOT_DIR / ".env"
print(f"ENV_FILE_PATH: {ENV_FILE_PATH}")
# 로드된 환경 변수 디버깅
print(f"SUPABASE_KEY in env: {'SUPABASE_KEY' in os.environ}")
print(f"Available env vars: {list(os.environ.keys())}")

class Settings(BaseSettings):
    # 앱 설정
    APP_NAME: str = "Mumul Edu"
    API_PREFIX: str = "/api"
    DEBUG: bool = Field(True, env="DEBUG")  # 기본값을 True로 설정
    
    # 환경
    ENVIRONMENT: str = Field(..., env="ENVIRONMENT")
    
    # Supabase 설정 - 타입을 변경하고 기본값 추가
    SUPABASE_URL: str = Field(..., env="SUPABASE_URL")
    SUPABASE_KEY: str = Field(..., env="SUPABASE_KEY")
    SUPABASE_SERVICE_KEY: Optional[str] = None
    
    # 프론트엔드 설정
    FRONTEND_URL: str = Field("http://localhost:3000", env="FRONTEND_URL")  # AnyHttpUrl에서 str로 변경
    
    # 코스 코드 설정
    COURSE_CODE_LENGTH: int = 6
    
    # Dify API 설정
    DIFY_API_KEY: str = Field(..., env="DIFY_API_KEY")
    DIFY_API_BASE_URL: Optional[str] = None
    
    # CORS 설정
    CORS_ORIGINS: List[str] = Field(default_factory=list, env="CORS_ORIGINS")
    
    @field_validator("CORS_ORIGINS", mode="before")
    def split_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v
    
    # GCS 설정
    GCS_BUCKET_NAME: str = Field(..., env="GCS_BUCKET_NAME")
    
    # JWT 설정
    JWT_SECRET: str = Field("dev-secret-key-for-testing", env="JWT_SECRET")  # SecretStr에서 str로 변경
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # 로깅 설정
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Pydantic V2 호환성
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra="ignore",
        env_nested_delimiter='__',
        validate_default=False  # 기본값 검증 비활성화
    )

# 디버깅을 위한 정보 출력
print(f"Looking for .env file at: {ENV_FILE_PATH} (exists: {ENV_FILE_PATH.exists()})")

# settings 인스턴스 생성
try:
    settings = Settings()
    print("Settings loaded successfully")
    print(f"SUPABASE_URL: {settings.SUPABASE_URL}")
    print(f"SUPABASE_KEY length: {len(settings.SUPABASE_KEY) if settings.SUPABASE_KEY else 0}")
    print(f"JWT_SECRET set: {'Yes' if settings.JWT_SECRET else 'No'}")
except Exception as e:
    print(f"Error loading settings: {e}")
    # 임시 설정으로 계속
    settings = Settings(
        _env_file=None,  # 환경 파일 무시
        SUPABASE_URL="https://example.supabase.co",
        SUPABASE_KEY="dummy-key-for-development",
        FRONTEND_URL="http://localhost:3000",
        JWT_SECRET="dev-secret-key-do-not-use-in-production"
    )
    print("Using fallback settings")
