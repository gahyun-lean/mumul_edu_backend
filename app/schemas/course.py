from app.schemas.base import BaseSchema
from app.schemas.types import UUIDType, DateTime

class CourseCreate(BaseSchema):
    title: str

class CourseRead(CourseCreate):
    id: UUIDType
    title: str
    instructor_id: UUIDType
    created_at: DateTime