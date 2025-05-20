import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.course_code import CourseCodeService
from app.schemas.course_code import CourseCodeCreate, CourseCodeUpdate

@pytest.fixture
def course_code_service():
    repo = AsyncMock()
    return CourseCodeService(repo)

@pytest.mark.asyncio
async def test_create_course_code_success(course_code_service):
    course_code_service.repository.get_by_code.return_value = None
    course_code_service.repository.create.return_value = MagicMock(code="CODE123")
    payload = CourseCodeCreate(course_id="course1", expires_at=None, max_usage=10)
    result = course_code_service.create_course_code(payload, instructor_id="instructor1")
    assert result.code == "CODE123"

@pytest.mark.asyncio
async def test_create_course_code_duplicate(course_code_service):
    course_code_service.repository.get_by_code.return_value = MagicMock()
    payload = CourseCodeCreate(course_id="course1", expires_at=None, max_usage=10)
    with pytest.raises(Exception):
        course_code_service.create_course_code(payload, instructor_id="instructor1")

@pytest.mark.asyncio
async def test_get_course_code_not_found(course_code_service):
    course_code_service.repository.get_by_code.return_value = None
    with pytest.raises(Exception):
        course_code_service.get_course_code("notfound", instructor_id="instructor1") 