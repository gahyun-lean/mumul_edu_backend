from fastapi import HTTPException, status
import string
import random
from app.core.config import settings
from app.schemas.course_code import (
    CourseCodeCreate, CourseCodeRead, CourseCodeUpdate
)
from app.repositories.implementations.supabase.course_code_repository import CourseCodeRepository

CODE_LENGTH = settings.COURSE_CODE_LENGTH

def _generate_code(length: int = CODE_LENGTH) -> str:
    # CODE_LENGTH 길이의 랜덤 알파벳대문자+숫자 문자열 생성
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(random.choices(alphabet, k=length))

class CourseCodeService:
    def __init__(self, repository: CourseCodeRepository):
        self.repository = repository

    def create_course_code(self, payload: CourseCodeCreate, instructor_id: str) -> CourseCodeRead:
        # 강의 존재 여부 확인 등은 서비스에서 처리, 실제 insert는 repository에 위임
        # (조인 등 복잡 쿼리는 추후 별도 메서드로 분리 가능)
        for _ in range(3):
            code = _generate_code()
            if not self.repository.get_by_code(code):
                break
        else:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to generate code")
        insert_data = payload.dict()
        insert_data["code"] = code
        course_code = self.repository.create(insert_data)
        return course_code

    def list_course_codes(self, instructor_id: str) -> list[CourseCodeRead]:
        return self.repository.get_by_instructor(instructor_id)

    def get_course_code(self, code: str, instructor_id: str) -> CourseCodeRead:
        course_code = self.repository.get_by_code(code)
        if not course_code:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Course code not found")
        # instructor_id 체크 등은 서비스에서 처리
        return course_code

    def update_course_code(self, code: str, data: CourseCodeUpdate, instructor_id: str) -> CourseCodeRead:
        self.get_course_code(code, instructor_id)
        course_code = self.repository.update(code, data.dict(exclude_unset=True))
        return course_code

    def delete_course_code(self, code: str, instructor_id: str) -> None:
        self.get_course_code(code, instructor_id)
        self.repository.delete(code)

    def increment_usage(self, code: str, instructor_id: str) -> CourseCodeRead:
        cc = self.get_course_code(code, instructor_id)
        new_count = cc.usage_count + 1
        return self.update_course_code(code, CourseCodeUpdate(max_usage=cc.max_usage, expires_at=cc.expires_at, usage_count=new_count), instructor_id)
