import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import UploadFile
from app.services.document import DocumentService
from app.schemas.types import SourceType

@pytest.fixture
def document_service():
    repo = AsyncMock()
    dify = AsyncMock()
    gcs = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()
    gcs.bucket.return_value = bucket
    bucket.blob.return_value = blob
    return DocumentService(repo, dify=dify, gcs=gcs)

@pytest.mark.asyncio
async def test_upload_file(document_service):
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.pdf"
    document_service.bucket.blob.return_value.upload_from_file = AsyncMock()
    document_service.bucket.blob.return_value.public_url = "https://storage.example.com/test.pdf"
    result = await document_service.upload_file(
        course_id="course_123",
        inspector_id="inspector_123",
        file=mock_file
    )
    assert result == "https://storage.example.com/test.pdf"
    document_service.bucket.blob.assert_called_once_with("course_123/inspector_123/test.pdf")

@pytest.mark.asyncio
async def test_create_document(document_service):
    document_service.repository.create.return_value = {"id": "doc_123", "inspector_id": "inspector_123", "course_id": "course_123", "source_url": "https://example.com/doc.pdf", "source_type": "pdf", "status": "pending"}
    document_service.dify.ingest_document.return_value = "dify_doc_123"
    document_service.repository.update_status.return_value = MagicMock()
    result = await document_service.create_documnet(
        inspector_id="inspector_123",
        course_id="course_123",
        source_url="https://example.com/doc.pdf",
        source_type=SourceType.PDF
    )
    assert result.id == "doc_123"
    assert result.inspector_id == "inspector_123"
    assert result.course_id == "course_123"

@pytest.mark.asyncio
async def test_get_document_status(document_service):
    doc = MagicMock()
    doc.inspector_id = "inspector_123"
    doc.dify_doc_id = "dify_123"
    document_service.repository.get_by_id.return_value = doc
    document_service.dify.get_document_status.return_value = {"status": "done", "error_message": None}
    document_service.repository.update_status.return_value = doc
    result = await document_service.get_document_status(
        inspector_id="inspector_123",
        document_id="doc_123"
    )
    assert result.status == "done" 