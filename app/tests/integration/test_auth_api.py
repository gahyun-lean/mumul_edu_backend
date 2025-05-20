import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.mark.integration
def test_sign_up_success(test_client, mock_services):
    """회원가입 성공 테스트"""
    # 회원가입 성공 응답 모킹
    mock_services.auth.sign_up.return_value = {
        "user": {
            "id": "test-user-id",
            "email": "new@example.com",
            "email_confirmed_at": "2023-01-01T00:00:00Z"
        },
        "session": {
            "access_token": "fake_access_token",
            "refresh_token": "fake_refresh_token",
            "expires_at": 9999999999
        }
    }
    
    # API 호출
    response = test_client.post(
        "/api/auth/signup",
        json={
            "email": "new@example.com",
            "password": "securePassword123!"
        }
    )
    
    # 결과 검증
    assert response.status_code == 201
    data = response.json()
    assert "user" in data
    assert "session" in data
    assert data["user"]["email"] == "new@example.com"
    assert "access_token" in data["session"]
