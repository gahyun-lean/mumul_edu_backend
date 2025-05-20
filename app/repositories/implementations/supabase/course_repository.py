from typing import Optional, List
from app.repositories.implementations.supabase.base import SupabaseRepository
from app.schemas.course import CourseRead

class CourseRepository(SupabaseRepository[CourseRead]):
    def __init__(self, supabase_client):
        super().__init__(supabase_client, "courses", model=CourseRead)

    async def get_by_instructor(self, instructor_id: str) -> List[CourseRead]:
        return await self.list({"instructor_id": instructor_id})

    async def get_by_id(self, course_id: str) -> Optional[CourseRead]:
        resp = await self.supabase.from_(self.table_name).select("*").eq("id", course_id).single().execute()
        if resp.error or not resp.data:
            return None
        return CourseRead(**resp.data) 