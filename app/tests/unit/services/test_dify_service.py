import pytest
from unittest.mock import AsyncMock, patch
from app.services.dify_service import DifyService

@pytest.fixture
def dify_service():
    return DifyService(api_key="test_api_key")

@pytest.mark.asyncio
async def test_create_document(dify_service):
    # Mock response
    mock_response = AsyncMock()
    mock_response.json.return_value = {"id": "doc_123", "status": "processing"}
    mock_response.raise_for_status = AsyncMock()
    
    # Mock client
    with patch.object(dify_service.client, 'post', return_value=mock_response):
        result = await dify_service.create_document(
            source="https://example.com/doc.pdf",
            source_type="pdf"
        )
        
        assert result == {"id": "doc_123", "status": "processing"}
        dify_service.client.post.assert_called_once_with(
            "https://api.dify.ai/v1/documents",
            json={
                "source": "https://example.com/doc.pdf",
                "source_type": "pdf"
            },
            headers=dify_service.headers
        )

@pytest.mark.asyncio
async def test_get_document_status(dify_service):
    # Mock response
    mock_response = AsyncMock()
    mock_response.json.return_value = {"status": "completed"}
    mock_response.raise_for_status = AsyncMock()
    
    # Mock client
    with patch.object(dify_service.client, 'get', return_value=mock_response):
        result = await dify_service.get_document_status("doc_123")
        
        assert result == {"status": "completed"}
        dify_service.client.get.assert_called_once_with(
            "https://api.dify.ai/v1/documents/doc_123",
            headers=dify_service.headers
        )

@pytest.mark.asyncio
async def test_chat(dify_service):
    # Mock response
    mock_response = AsyncMock()
    mock_response.json.return_value = {"answer": "테스트 응답입니다."}
    mock_response.raise_for_status = AsyncMock()
    
    # Mock client
    with patch.object(dify_service.client, 'post', return_value=mock_response):
        result = await dify_service.chat(
            question="테스트 질문입니다.",
            document_ids=["doc_123"]
        )
        
        assert result == {"answer": "테스트 응답입니다."}
        dify_service.client.post.assert_called_once_with(
            "https://api.dify.ai/v1/chat/completions",
            json={
                "question": "테스트 질문입니다.",
                "document_ids": ["doc_123"]
            },
            headers=dify_service.headers
        )

@pytest.mark.asyncio
async def test_close(dify_service):
    # Mock client
    with patch.object(dify_service.client, 'aclose') as mock_close:
        await dify_service.close()
        mock_close.assert_called_once() 