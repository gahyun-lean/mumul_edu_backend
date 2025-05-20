import os
import pytest
from dotenv import load_dotenv, find_dotenv
from app.core.supabase_client import supabase
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from unittest.mock import MagicMock, patch, AsyncMock
from app.schemas.auth import AuthResponse, SignUpUser, AuthSession
import datetime
import uuid

# ⬇️ pytest가 시작되기 전에 .env를 찾아 로드
load_dotenv(find_dotenv())

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """전체 테스트 실행 전후에 TESTING 환경변수 설정/해제"""
    os.environ["TESTING"] = "1"
    yield
    os.environ.pop("TESTING", None)

@pytest.fixture(autouse=True)
def reset_supabase_data():
    """
    각 테스트 후 Supabase 데이터 정리
    (테스트 중 생성된 레코드를 삭제하여 상태 고정)
    """
    yield
    # 테스트에서 생성한 user id 목록 예시
    test_user_ids = ["테스트에서 생성된 사용자 ID들"]
    for user_id in test_user_ids:
        try:
            supabase.from_("profiles").delete().eq("id", user_id).execute()
            supabase.from_("courses").delete().eq("instructor_id", user_id).execute()
        except Exception as e:
            print(f"테스트 데이터 정리 중 오류: {e}")

@pytest.fixture
def test_client():
    """API 테스트를 위한 클라이언트"""
    return TestClient(app)

@pytest.fixture
def mock_supabase():
    """Supabase 클라이언트 모킹"""
    with patch("app.supabase_client.supabase") as mock:
        yield mock

@pytest.fixture
def mock_services(mock_supabase):
    """모든 서비스 모킹"""
    with patch("app.dependencies.services.get_services") as mock_get_services:
        mock_auth = MagicMock()
        mock_profile = MagicMock()
        mock_course = MagicMock()
        mock_course_code = MagicMock()
        mock_enrollment = MagicMock()
        mock_document = MagicMock()
        
        # Services 인스턴스 모킹
        mock_services = MagicMock()
        mock_services.auth = mock_auth
        mock_services.profile = mock_profile
        mock_services.course = mock_course
        mock_services.course_code = mock_course_code
        mock_services.enrollment = mock_enrollment
        mock_services.document = mock_document
        
        mock_get_services.return_value = mock_services
        yield mock_services

@pytest.fixture
def mock_auth_user():
    """인증된 사용자 모킹"""
    return {
        "id": str(uuid.uuid4()),
        "email": "test@example.com",
        "email_confirmed_at": datetime.datetime.now().isoformat()
    }

@pytest.fixture
def mock_auth_token(mock_auth_user):
    """유효한 인증 토큰 모킹"""
    user_data = SignUpUser(
        id=mock_auth_user["id"],
        email=mock_auth_user["email"],
        email_confirmed_at=mock_auth_user["email_confirmed_at"]
    )
    
    session_data = AuthSession(
        access_token="fake_access_token",
        refresh_token="fake_refresh_token",
        expires_at=int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())
    )
    
    return AuthResponse(
        user=user_data.model_dump(),
        session=session_data,
        error=None
    )

@pytest.fixture
def mock_repo():
    return AsyncMock()
