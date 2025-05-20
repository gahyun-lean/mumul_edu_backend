import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_course(monkeypatch):
    monkeypatch.setattr("app.dependencies.auth.get_current_user", lambda: {"id": "instructor1", "email": "i@test.com"})
    payload = {"title": "테스트강의"}
    response = client.post("/api/courses", json=payload, headers={"Authorization": "Bearer testtoken"})
    assert response.status_code in (200, 201)

def test_list_courses(monkeypatch):
    monkeypatch.setattr("app.dependencies.auth.get_current_user", lambda: {"id": "instructor1", "email": "i@test.com"})
    response = client.get("/api/courses", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200

def test_get_course(monkeypatch):
    monkeypatch.setattr("app.dependencies.auth.get_current_user", lambda: {"id": "instructor1", "email": "i@test.com"})
    response = client.get("/api/courses/course1", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code in (200, 404) 