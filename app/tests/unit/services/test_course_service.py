import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.course import CourseService
from app.schemas.course import CourseCreate

@pytest.fixture
def course_service():
    repo = AsyncMock()
    return CourseService(repo)

@pytest.mark.asyncio
async def test_create_course_success(course_service):
    course_service.repository.create.return_value = {"id": "course1", "title": "테스트강의", "instructor_id": "instructor1"}
    payload = CourseCreate(title="테스트강의")
    result = await course_service.create_course(payload, instructor_id="instructor1")
    assert result.id == "course1"
    course_service.repository.create.assert_awaited()

@pytest.mark.asyncio
async def test_get_course_not_found(course_service):
    course_service.repository.get_by_id.return_value = None
    with pytest.raises(Exception):
        await course_service.get_course("notfound")

@pytest.mark.asyncio
async def test_list_courses(course_service):
    course_service.repository.get_by_instructor.return_value = [MagicMock(id="course1"), MagicMock(id="course2")]
    result = await course_service.list_courses("instructor1")
    assert len(result) == 2 