import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.enrollment import EnrollmentService
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate

@pytest.fixture
def enrollment_service():
    enrollment_repo = AsyncMock()
    course_code_repo = AsyncMock()
    course_repo = AsyncMock()
    return EnrollmentService(enrollment_repo, course_code_repo, course_repo)

@pytest.mark.asyncio
async def test_create_enrollment_success(enrollment_service):
    code = MagicMock()
    code.usage_count = 0
    code.max_usage = 5
    code.course_id = "course1"
    enrollment_service.course_code_repo.get_by_code.return_value = code
    enrollment_service.course_repo.get_by_id.return_value = MagicMock()
    enrollment_service.enrollment_repo.create.return_value = MagicMock()
    enrollment_service.course_code_repo.update.return_value = None

    payload = EnrollmentCreate(code="abc")
    result = await enrollment_service.create_enrollment(payload, student_id="student1")
    assert result is not None
    enrollment_service.enrollment_repo.create.assert_awaited()
    enrollment_service.course_code_repo.update.assert_awaited()

@pytest.mark.asyncio
async def test_create_enrollment_code_limit(enrollment_service):
    code = MagicMock()
    code.usage_count = 5
    code.max_usage = 5
    enrollment_service.course_code_repo.get_by_code.return_value = code
    payload = EnrollmentCreate(code="abc")
    with pytest.raises(Exception):
        await enrollment_service.create_enrollment(payload, student_id="student1")

@pytest.mark.asyncio
async def test_update_enrollment_permission(enrollment_service):
    enrollment = MagicMock()
    enrollment.course_id = "course1"
    course = MagicMock()
    course.instructor_id = "instructor1"
    enrollment_service.enrollment_repo.get_by_id.return_value = enrollment
    enrollment_service.course_repo.get_by_id.return_value = course
    payload = EnrollmentUpdate()
    with pytest.raises(Exception):
        await enrollment_service.update_enrollment("enroll1", payload, instructor_id="other") 