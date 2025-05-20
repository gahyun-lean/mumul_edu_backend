from app.schemas.base import BaseSchema
from app.schemas.types import UUIDType, SourceType, DocumentStatus, DateTime, DEFAULT_DOCUMENT_STATUS
from pydantic import AnyHttpUrl

class DocumentCreate(BaseSchema):
    source_url: str
    source_type: SourceType
    course_id:   UUIDType

class DocumentRead(BaseSchema):
    id:            UUIDType
    inspector_id:  UUIDType
    course_id:     UUIDType
    source_url:    str
    source_type:   SourceType
    status:        DocumentStatus = DEFAULT_DOCUMENT_STATUS
    dify_doc_id:   str | None
    error_message: str | None
    created_at:    DateTime
    updated_at:    DateTime

class FileUploadResponse(BaseSchema):
    url: AnyHttpUrl
