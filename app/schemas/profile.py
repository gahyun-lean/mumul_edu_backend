from app.schemas.base import BaseSchema
from app.schemas.types import UUIDType, DateTime, Role


class ProfileCreate(BaseSchema):
    full_name: str
    role: Role
    phone: str | None = None

class ProfileRead(ProfileCreate):
    id: UUIDType
    created_at: DateTime
