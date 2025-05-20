from fastapi import APIRouter, Depends, status
from app.schemas.course_code import CourseCodeCreate, CourseCodeRead, CourseCodeUpdate
from app.dependencies.auth import get_current_user
from app.dependencies.services import get_services, Services

router = APIRouter(prefix="/api/course_codes", tags=["course_codes"])

@router.post("", response_model=CourseCodeRead, status_code=status.HTTP_201_CREATED, summary="수강코드 생성")
async def create_course_code(
    payload: CourseCodeCreate,
    user: dict      = Depends(get_current_user),
    services:Services = Depends(get_services),
):
    return services.course_code.create_course_code(payload, user["id"])

@router.get("", response_model=list[CourseCodeRead], status_code=status.HTTP_200_OK, summary="수강코드 목록조회")
async def list_course_codes(
    user: dict      = Depends(get_current_user),
    services:Services = Depends(get_services),
):
    return services.course_code.list_course_codes(user["id"])

@router.get("/{code}", response_model=CourseCodeRead, status_code=status.HTTP_200_OK, summary="수강코드 단건 조회")
async def get_course_code(
    code: str,
    user: dict      = Depends(get_current_user),
    services:Services = Depends(get_services),
):
    return services.course_code.get_course_code(code, user["id"])

@router.delete("/{code}", status_code=status.HTTP_204_NO_CONTENT, summary="수강코드 삭제")
async def delete_course_code(
    code: str,
    user: dict      = Depends(get_current_user),
    services:Services = Depends(get_services),
):
    services.course_code.delete_course_code(code, user["id"])

@router.patch("/{code}", response_model=CourseCodeRead, status_code=status.HTTP_200_OK, summary="수강코드 수정")
async def update_course_code(
    code: str,
    payload: CourseCodeUpdate,
    user: dict      = Depends(get_current_user),
    services:Services = Depends(get_services),
):
    return services.course_code.update_course_code(code, payload, user["id"])
