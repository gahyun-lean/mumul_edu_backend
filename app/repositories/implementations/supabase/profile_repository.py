from typing import Optional, List
from app.repositories.implementations.supabase.base import SupabaseRepository
from app.schemas.profile import ProfileRead

class ProfileRepository(SupabaseRepository[ProfileRead]):
    def __init__(self, supabase_client):
        super().__init__(supabase_client, "profiles", model=ProfileRead)

    async def get_by_user_id(self, user_id: str) -> Optional[ProfileRead]:
        """사용자 ID로 프로필 조회"""
        return await self.get_by_id(user_id)

    async def get_by_role(self, role: str) -> List[ProfileRead]:
        """역할로 프로필 목록 조회"""
        return await self.list({"role": role}) 