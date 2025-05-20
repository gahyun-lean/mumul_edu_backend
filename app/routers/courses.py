from fastapi import APIRouter, Depends, status
from app.schemas.course import CourseCreate, CourseRead
from app.schemas.enrollment import EnrollmentRead
from app.dependencies.services import get_services, Services
from app.dependencies.auth import get_current_user


router = APIRouter(prefix="/api/courses", tags=["courses"])

@router.post("", response_model=CourseRead, status_code=status.HTTP_201_CREATED, summary="강의 생성")
async def create_course(
    payload: CourseCreate, 
    user: dict = Depends(get_current_user), 
    services: Services = Depends(get_services)
):
    return services.course.create_course(payload, user["id"])

@router.get("", response_model=list[CourseRead], status_code=status.HTTP_200_OK, summary="강의 목록조회")
async def list_courses(
    user: dict = Depends(get_current_user), 
    services: Services = Depends(get_services)
):
    return services.course.list_courses(user["id"])

@router.get("/{course_id}", response_model=CourseRead, status_code=status.HTTP_200_OK, summary="강의 단건 조회")
async def get_course(
    course_id: str, 
    user: dict = Depends(get_current_user), 
    services: Services = Depends(get_services)
):
    return services.course.get_course(course_id)

@router.get("/{course_id}/enrollments", response_model=list[EnrollmentRead], status_code=status.HTTP_200_OK, summary="특정강의에 수강신청한 학생 목록조회")
async def list_enrollments(
    course_id: str,
    instructor: dict = Depends(get_current_user),
    services: Services = Depends(get_services)
):
    return services.enrollment.list_enrollments_by_course(course_id, instructor["id"])