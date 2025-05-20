from typing import TypeVar, Generic, Optional, List, Dict, Any, Type
from app.core.exceptions import DatabaseError

T = TypeVar('T')

class SupabaseRepository(Generic[T]):
    def __init__(self, supabase_client, table_name: str, model: Type[T] = None):
        self.supabase = supabase_client
        self.table_name = table_name
        self.model = model

    async def create(self, data: Dict[str, Any]) -> T:
        """데이터 생성"""
        resp = await self.supabase.from_(self.table_name).insert(data).select("*").single().execute()
        if resp.error:
            raise DatabaseError(f"데이터 생성 실패: {resp.error.message}")
        return self.model(**resp.data) if self.model else resp.data

    async def get_by_id(self, id: str) -> Optional[T]:
        """ID로 데이터 조회"""
        resp = await self.supabase.from_(self.table_name).select("*").eq("id", id).single().execute()
        if resp.error or not resp.data:
            return None
        return self.model(**resp.data) if self.model else resp.data

    async def list(self, filters: Dict[str, Any] = None) -> List[T]:
        """데이터 목록 조회"""
        query = self.supabase.from_(self.table_name).select("*")
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        resp = await query.execute()
        if resp.error:
            raise DatabaseError(f"데이터 목록 조회 실패: {resp.error.message}")
        return [self.model(**row) for row in resp.data] if self.model else resp.data

    async def update(self, id: str, data: Dict[str, Any]) -> T:
        """데이터 수정"""
        resp = await self.supabase.from_(self.table_name).update(data).eq("id", id).select("*").single().execute()
        if resp.error:
            raise DatabaseError(f"데이터 수정 실패: {resp.error.message}")
        return self.model(**resp.data) if self.model else resp.data

    async def delete(self, id: str) -> bool:
        """데이터 삭제"""
        resp = await self.supabase.from_(self.table_name).delete().eq("id", id).execute()
        if resp.error:
            raise DatabaseError(f"데이터 삭제 실패: {resp.error.message}")
        return True 