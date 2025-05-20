import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.profile import ProfileService
from app.schemas.profile import ProfileCreate, ProfileRead
from app.schemas.types import Role
from app.core.exceptions import ResourceNotFound, ResourceAlreadyExists, DatabaseError

@pytest.fixture
def profile_service():
    """프로필 서비스 인스턴스 생성"""
    repo = AsyncMock()
    return ProfileService(repo)

@pytest.mark.asyncio
async def test_create_profile_success(profile_service):
    """프로필 생성 성공 케이스 테스트"""
    profile_service.repository.get_by_user_id.return_value = None
    profile_service.repository.create.return_value = {"id": "user1", "full_name": "홍길동", "role": "student", "email": "test@test.com", "phone": "010-0000-0000"}
    payload = ProfileCreate(full_name="홍길동", role="student", phone="010-0000-0000")
    result = await profile_service.create_profile(payload, user_id="user1", user_email="test@test.com")
    assert result.id == "user1"
    profile_service.repository.create.assert_awaited()

@pytest.mark.asyncio
async def test_create_profile_duplicate(profile_service):
    """이미 존재하는 프로필 생성 시도 테스트"""
    profile_service.repository.get_by_user_id.return_value = MagicMock()
    payload = ProfileCreate(full_name="홍길동", role="student", phone="010-0000-0000")
    with pytest.raises(Exception):
        await profile_service.create_profile(payload, user_id="user1", user_email="test@test.com")

@pytest.mark.asyncio
async def test_read_my_profile_not_found(profile_service):
    profile_service.repository.get_by_user_id.return_value = None
    with pytest.raises(Exception):
        await profile_service.read_my_profile("user1")
