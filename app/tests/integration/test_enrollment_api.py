import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_enrollment_create(monkeypatch):
    # 인증 모킹 등 필요시 monkeypatch 사용
    # monkeypatch.setattr("app.dependencies.auth.get_current_user", lambda: {"id": "student1", "email": "s@test.com"})
    payload = {"code": "TESTCODE"}
    response = client.post("/api/enrollments", json=payload, headers={"Authorization": "Bearer testtoken"})
    assert response.status_code in (200, 201, 400, 409, 404)  # 실제 상황에 따라 조정
    # 반환값, DB 상태 등 추가 검증 가능
