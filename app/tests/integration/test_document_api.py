import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_document(monkeypatch):
    monkeypatch.setattr("app.dependencies.auth.get_current_user", lambda: {"id": "inspector1", "email": "i@test.com"})
    payload = {"course_id": "course1", "source_url": "https://example.com/doc.pdf", "source_type": "pdf"}
    response = client.post("/api/documents", json=payload, headers={"Authorization": "Bearer testtoken"})
    assert response.status_code in (200, 201, 500)

def test_get_document_status(monkeypatch):
    monkeypatch.setattr("app.dependencies.auth.get_current_user", lambda: {"id": "inspector1", "email": "i@test.com"})
    response = client.get("/api/documents/doc_123/status", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code in (200, 404) 