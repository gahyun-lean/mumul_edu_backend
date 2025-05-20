from pydantic import EmailStr
from uuid import UUID
from datetime import datetime
from enum import Enum

EmailString = EmailStr
UUIDType    = UUID
DateTime    = datetime

class EnrollmentStatus(str, Enum):
    pending = "pending"
    active  = "active"
    expired = "expired"

class Role(str, Enum):
    student = "student"
    instructor = "instructor"

class SourceType(str, Enum):
    pdf     = "pdf"
    youtube = "youtube"
    webpage = "webpage"

class DocumentStatus(str, Enum):
    pending    = "pending"
    processing = "processing"
    ready      = "ready"
    error      = "error"


# default 상수 (많아지면 추후 분리)
DEFAULT_ENROLLMENT_STATUS = EnrollmentStatus.pending
DEFAULT_DOCUMENT_STATUS = DocumentStatus.pending