from typing import Optional, List
from app.repositories.implementations.supabase.base import SupabaseRepository
from app.schemas.course_code import CourseCodeRead

class CourseCodeRepository(SupabaseRepository[CourseCodeRead]):
    def __init__(self, supabase_client):
        super().__init__(supabase_client, "course_codes", model=CourseCodeRead)

    async def get_by_instructor(self, instructor_id: str) -> List[CourseCodeRead]:
        # courses 테이블과 조인 필요시 별도 구현
        return await self.list({"instructor_id": instructor_id})

    async def get_by_code(self, code: str) -> Optional[CourseCodeRead]:
        rows = await self.list({"code": code})
        return rows[0] if rows else None 