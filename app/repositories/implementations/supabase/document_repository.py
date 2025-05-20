from typing import Optional, List
from app.repositories.implementations.supabase.base import SupabaseRepository
from app.schemas.document import DocumentRead

class DocumentRepository(SupabaseRepository[DocumentRead]):
    def __init__(self, supabase_client):
        super().__init__(supabase_client, "documents", model=DocumentRead)

    async def get_by_inspector(self, inspector_id: str) -> List[DocumentRead]:
        """검사자 ID로 문서 목록 조회"""
        return await self.list({"inspector_id": inspector_id})

    async def get_by_course(self, course_id: str) -> List[DocumentRead]:
        """강의 ID로 문서 목록 조회"""
        return await self.list({"course_id": course_id})

    async def update_status(self, doc_id: str, status: str, error_message: str = None) -> Optional[DocumentRead]:
        """문서 상태 업데이트"""
        update_data = {"status": status}
        if error_message is not None:
            update_data["error_message"] = error_message
        return await self.update(doc_id, update_data) 