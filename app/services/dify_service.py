import httpx
from typing import List
from contextlib import asynccontextmanager

class DifyService:
    BASE_URL = "https://api.dify.ai/v1"

    def __init__(self, api_key: str):
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.client = None

    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        self.client = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        if self.client:
            await self.client.aclose()
            self.client = None

    @asynccontextmanager
    async def get_client(self):
        """클라이언트 컨텍스트 매니저"""
        if not self.client:
            self.client = httpx.AsyncClient()
        try:
            yield self.client
        finally:
            if self.client:
                await self.client.aclose()
                self.client = None

    async def create_document(self, source: str, source_type: str) -> dict:
        async with self.get_client() as client:
            resp = await client.post(
                f"{self.BASE_URL}/documents",
                json={"source": source, "source_type": source_type},
                headers=self.headers,
            )
            resp.raise_for_status()
            return resp.json()

    async def get_document_status(self, doc_id: str) -> dict:
        async with self.get_client() as client:
            resp = await client.get(
                f"{self.BASE_URL}/documents/{doc_id}",
                headers=self.headers,
            )
            resp.raise_for_status()
            return resp.json()

    async def chat(self, question: str, document_ids: List[str]) -> dict:
        async with self.get_client() as client:
            resp = await client.post(
                f"{self.BASE_URL}/chat/completions",
                json={"question": question, "document_ids": document_ids},
                headers=self.headers,
            )
            resp.raise_for_status()
            return resp.json()
