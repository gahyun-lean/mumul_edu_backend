from fastapi import APIRouter, Depends, status
from app.schemas.enrollment import EnrollmentCreate, EnrollmentRead, EnrollmentUpdate
from app.dependencies.auth import get_current_user  
from app.dependencies.services import get_services, Services

router = APIRouter(prefix="/api/enrollments", tags=["enrollments"])

@router.post("", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED, summary="(학생용)강의 코드로 참여신청")
async def create_enrollment(
    payload: EnrollmentCreate,
    student_id: str,
    services: Services = Depends(get_services)
):
    return services.enrollment.create_enrollment(payload, student_id)


@router.get("", response_model=list[EnrollmentRead], status_code=status.HTTP_200_OK, summary="(학생용)참여신청 목록조회")
async def list_enrolled_courses_for_student(
    student: dict = Depends(get_current_user),
    services: Services = Depends(get_services)
):
    return services.enrollment.list_enrolled_courses_for_student(student["id"])   


@router.patch("/{enrollment_id}", response_model=EnrollmentRead, status_code=status.HTTP_200_OK, summary="(강사용)참여신청 상태 변경 (승인/거절)")
async def update_enrollment(
    enrollment_id: str,
    payload: EnrollmentUpdate,
    instructor: dict = Depends(get_current_user),
    services: Services = Depends(get_services)
):
    return services.enrollment.update_enrollment(enrollment_id, payload, instructor["id"])