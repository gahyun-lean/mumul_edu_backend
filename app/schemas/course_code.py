from app.schemas.base import BaseSchema
from app.schemas.types import UUIDType, DateTime
from pydantic import model_validator
from app.core.config import settings
from pydantic import AnyHttpUrl

class CourseCodeCreate(BaseSchema):
    course_id: UUIDType
    expires_at: DateTime
    max_usage: int

class CourseCodeUpdate(BaseSchema):
    expires_at: DateTime | None = None
    max_usage: int       | None = None

class CourseCodeRead(CourseCodeCreate):
    code: str
    usage_count: int
    created_at: DateTime
    share_url: AnyHttpUrl

    @model_validator(mode="before")
    def set_share_url(cls, values):
        values["share_url"] = f"{settings.FRONTEND_URL}/enroll?code={values['code']}"
        return values
