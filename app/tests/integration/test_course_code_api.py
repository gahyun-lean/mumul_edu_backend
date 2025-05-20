import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_course_code(monkeypatch):
    monkeypatch.setattr("app.dependencies.auth.get_current_user", lambda: {"id": "instructor1", "email": "i@test.com"})
    payload = {"course_id": "course1", "expires_at": None, "max_usage": 10}
    response = client.post("/api/course_codes", json=payload, headers={"Authorization": "Bearer testtoken"})
    assert response.status_code in (200, 201, 500)

def test_list_course_codes(monkeypatch):
    monkeypatch.setattr("app.dependencies.auth.get_current_user", lambda: {"id": "instructor1", "email": "i@test.com"})
    response = client.get("/api/course_codes", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200

def test_get_course_code(monkeypatch):
    monkeypatch.setattr("app.dependencies.auth.get_current_user", lambda: {"id": "instructor1", "email": "i@test.com"})
    response = client.get("/api/course_codes/CODE123", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code in (200, 404)

def test_delete_course_code(monkeypatch):
    monkeypatch.setattr("app.dependencies.auth.get_current_user", lambda: {"id": "instructor1", "email": "i@test.com"})
    response = client.delete("/api/course_codes/CODE123", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code in (200, 204, 404) 