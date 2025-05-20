import os
from fastapi import HTTPException, UploadFile, status
from app.schemas.document import DocumentCreate, DocumentRead
from app.schemas.types import SourceType, DEFAULT_DOCUMENT_STATUS
from app.services.dify_service import DifyService
from google.cloud import storage
from app.repositories.implementations.supabase.document_repository import DocumentRepository

class DocumentService:
    def __init__(self, repository: DocumentRepository, dify: DifyService = None, gcs = None):
        self.repository = repository
        self.dify = dify or DifyService()
        self.gcs = gcs or storage.Client()
        self.bucket = self.gcs.bucket(os.getenv("GCS_BUCKET_NAME"))

    async def upload_file(
        self,
        course_id: str,
        inspector_id: str,
        file: UploadFile
    ) -> str:
        blob = self.bucket.blob(f"{course_id}/{inspector_id}/{file.filename}")
        await blob.upload_from_file(file.file)
        return blob.public_url
    
    async def create_documnet(
        self,
        inspector_id: str,
        course_id: str,
        source_url: str,
        source_type: SourceType
    ) -> DocumentRead:
        insert_data = {
            "inspector_id": inspector_id,
            "course_id": course_id,
            "source_url": source_url,
            "source_type": source_type,
            "status": DEFAULT_DOCUMENT_STATUS
        }
        document = await self.repository.create(insert_data)
        document_obj = DocumentRead(**document)

        dify_doc_id = await self.dify.ingest_document(
            source_url=source_url,
            source_type=source_type,
        )
        updated = await self.repository.update_status(document_obj.id, document_obj.status, None)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update document"
            )
        return document_obj

    async def get_document_status(
        self,
        inspector_id: str,
        document_id: str,
    ) -> DocumentRead:
        document = await self.repository.get_by_id(document_id)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        if document.inspector_id != inspector_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to access this document"
            )
        # dify 상태조회
        status_info = await self.dify.get_document_status(document.dify_doc_id)
        updated = await self.repository.update_status(document_id, status_info["status"], status_info["error_message"])
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update document"
            )
        merged_document = {
            **document.__dict__,
            "status": status_info["status"],
            "error_message": status_info["error_message"]
        }
        return DocumentRead(**merged_document)