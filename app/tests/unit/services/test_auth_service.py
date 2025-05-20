import pytest
from unittest.mock import MagicMock, patch
from app.services.auth import AuthService
from app.schemas.auth import SignUpRequest, SignInRequest

@pytest.fixture
def auth_service():
    supabase = MagicMock()
    return AuthService(supabase)

def test_sign_up_success(auth_service):
    payload = SignUpRequest(email="test@test.com", password="password123")
    mock_resp = MagicMock()
    mock_resp.error = None
    mock_resp.user = MagicMock(id="user1", email="test@test.com", email_confirmed_at="2023-01-01T00:00:00Z")
    mock_resp.session = MagicMock(access_token="tok", refresh_token="ref", expires_at=0)
    auth_service.supabase.auth.sign_up.return_value = mock_resp
    result = auth_service.sign_up(payload)
    assert result.user["id"] == "user1"
    assert result.session.access_token == "tok"

def test_sign_up_duplicate(auth_service):
    payload = SignUpRequest(email="dup@test.com", password="password123")
    mock_resp = MagicMock()
    mock_resp.error = MagicMock(message="duplicate")
    auth_service.supabase.auth.sign_up.return_value = mock_resp
    with pytest.raises(Exception):
        auth_service.sign_up(payload)

def test_sign_in_success(auth_service):
    payload = SignInRequest(email="test@test.com", password="password123")
    mock_resp = MagicMock()
    mock_resp.error = None
    mock_resp.user = MagicMock(id="user1", email="test@test.com", email_confirmed_at="2023-01-01T00:00:00Z")
    mock_resp.session = MagicMock(access_token="tok", refresh_token="ref", expires_at=0)
    auth_service.supabase.auth.sign_in_with_password.return_value = mock_resp
    result = auth_service.sign_in(payload)
    assert result.user["id"] == "user1"
    assert result.session.access_token == "tok"

def test_sign_in_fail(auth_service):
    payload = SignInRequest(email="wrong@test.com", password="wrong")
    mock_resp = MagicMock()
    mock_resp.error = MagicMock(message="Invalid login credentials")
    auth_service.supabase.auth.sign_in_with_password.return_value = mock_resp
    with pytest.raises(Exception):
        auth_service.sign_in(payload) 