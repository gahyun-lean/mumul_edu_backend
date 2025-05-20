from fastapi import HTTPException, status
from app.schemas.course import CourseCreate, CourseRead
from app.core.exceptions import ResourceNotFound, PermissionDenied, DatabaseError, ResourceAlreadyExists
from app.repositories.implementations.supabase.course_repository import CourseRepository

class CourseService:
    def __init__(self, repository: CourseRepository):
        self.repository = repository
    
    async def list_courses(self, instructor_id: str) -> list[CourseRead]:
        return await self.repository.get_by_instructor(instructor_id)
    
    async def get_course(self, course_id: str) -> CourseRead:
        course = await self.repository.get_by_id(course_id)
        if not course:
            raise ResourceNotFound("강의")
        return course

    async def create_course(self, payload: CourseCreate, instructor_id: str) -> CourseRead:
        insert_data = {
            "title": payload.title,
            "instructor_id": instructor_id,
        }
        try:
            course = await self.repository.create(insert_data)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return CourseRead(**course)