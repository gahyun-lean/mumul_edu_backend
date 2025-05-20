from pydantic import BaseModel
from app.schemas.types import UUIDType, EnrollmentStatus, DateTime, DEFAULT_ENROLLMENT_STATUS
from app.schemas.base import BaseSchema

class EnrollmentCreate(BaseSchema):
    code: str

class EnrollmentRead(EnrollmentCreate):
    id: UUIDType
    student_id: UUIDType
    course_id: UUIDType
    code: str
    status: EnrollmentStatus = DEFAULT_ENROLLMENT_STATUS
    joined_at: DateTime

class EnrollmentUpdate(BaseSchema):
    status: EnrollmentStatus
