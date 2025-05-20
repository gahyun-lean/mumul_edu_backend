from typing import Optional, List
from app.repositories.implementations.supabase.base import SupabaseRepository
from app.schemas.enrollment import EnrollmentRead

class EnrollmentRepository(SupabaseRepository[EnrollmentRead]):
    def __init__(self, supabase_client):
        super().__init__(supabase_client, "enrollments", model=EnrollmentRead)

    async def get_by_student(self, student_id: str) -> List[EnrollmentRead]:
        return await self.list({"student_id": student_id})

    async def get_by_course(self, course_id: str) -> List[EnrollmentRead]:
        return await self.list({"course_id": course_id}) 