import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_profile(monkeypatch):
    # 인증 모킹
    monkeypatch.setattr("app.dependencies.auth.get_current_user", lambda: {"id": "user1", "email": "test@test.com"})
    payload = {"full_name": "홍길동", "role": "student", "phone": "010-0000-0000"}
    response = client.post("/api/profiles", json=payload, headers={"Authorization": "Bearer testtoken"})
    assert response.status_code in (200, 201, 409)  # 성공 또는 중복


def test_read_my_profile(monkeypatch):
    monkeypatch.setattr("app.dependencies.auth.get_current_user", lambda: {"id": "user1", "email": "test@test.com"})
    response = client.get("/api/profiles/me", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code in (200, 404)  # 성공 또는 없음 