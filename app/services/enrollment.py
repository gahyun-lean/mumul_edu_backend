from fastapi import HTTPException, status
from app.repositories.implementations.supabase.enrollment_repository import EnrollmentRepository
from app.repositories.implementations.supabase.course_code_repository import CourseCodeRepository
from app.repositories.implementations.supabase.course_repository import CourseRepository
from app.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentRead,
    EnrollmentUpdate
)
from app.schemas.types import DEFAULT_ENROLLMENT_STATUS

class EnrollmentService:
    def __init__(self, enrollment_repo: EnrollmentRepository, course_code_repo: CourseCodeRepository, course_repo: CourseRepository):
        self.enrollment_repo = enrollment_repo
        self.course_code_repo = course_code_repo
        self.course_repo = course_repo

    async def create_enrollment(self, payload: EnrollmentCreate, student_id: str) -> EnrollmentRead:
        # 코드 존재 여부 확인
        code = await self.course_code_repo.get_by_code(payload.code)
        if not code:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Course or code not found")
        if code.usage_count >= code.max_usage:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Course code usage limit reached")
        course_id = code.course_id
        # 수강신청 생성
        insert_data = {
            "student_id": student_id,
            "course_id": course_id,
            "code": payload.code,
            "status": DEFAULT_ENROLLMENT_STATUS
        }
        enrollment = await self.enrollment_repo.create(insert_data)
        # instructor_id 조회 및 코드 사용 카운트 증가
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to get course")
        await self.course_code_repo.update(code.code, {"usage_count": code.usage_count + 1})
        return enrollment

    # 학생용 수강신청 목록조회
    async def list_enrolled_courses_for_student(self, student_id: str) -> list[EnrollmentRead]:
        return await self.enrollment_repo.get_by_student(student_id)

    # 강사용 수강신청학생 목록조회
    async def list_enrolled_course_for_instructor(self, course_id: str, instructor_id: str) -> list[EnrollmentRead]:
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to get course")
        if course.instructor_id != instructor_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Instructor access required")
        return await self.enrollment_repo.get_by_course(course_id)
    

    async def update_enrollment(self, enrollment_id: str, payload: EnrollmentUpdate, instructor_id: str) -> EnrollmentRead:
        enrollment = await self.enrollment_repo.get_by_id(enrollment_id)
        if not enrollment:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Enrollment not found")
        course = await self.course_repo.get_by_id(enrollment.course_id)
        if not course or course.instructor_id != instructor_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Instructor access required")
        updated = await self.enrollment_repo.update(enrollment_id, payload.dict())
        return updated