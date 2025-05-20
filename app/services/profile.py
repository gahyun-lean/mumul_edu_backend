from app.schemas.profile import ProfileCreate, ProfileRead
from fastapi import HTTPException
from app.repositories.implementations.supabase.profile_repository import ProfileRepository
from app.core.logging import logger

class ProfileService:
    def __init__(self, repository: ProfileRepository, logger=None):
        self.repository = repository
        from app.core.logging import logger as default_logger
        self.logger = logger or default_logger.getChild("profile_service")

    async def create_profile(self, payload: ProfileCreate, user_id: str, user_email: str) -> ProfileRead:
        self.logger.info(f"프로필 생성 시작: user_id={user_id}")
        
        existing = await self.repository.get_by_user_id(user_id)
        if existing:
            self.logger.warning(f"프로필 생성 실패: user_id={user_id}, 이미 존재하는 프로필")
            raise HTTPException(status_code=409, detail="Profile already exists")

        insert_data = {
            "id":        user_id,
            "full_name": payload.full_name,
            "role":      payload.role.value,
            "email":     user_email,
            "phone":     payload.phone or "",
        }

        try:
            resp = await self.repository.create(insert_data)
        except Exception as e:
            self.logger.error(f"프로필 생성 실패: user_id={user_id}, error={str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create profile")

        self.logger.info(f"프로필 생성 완료: user_id={user_id}")
        return ProfileRead(**resp)

    async def read_my_profile(self, user_id: str) -> ProfileRead:
        self.logger.info(f"프로필 조회: user_id={user_id}")
        profile = await self.repository.get_by_user_id(user_id)
        if not profile:
            self.logger.error(f"프로필 조회 실패: user_id={user_id}")
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile
