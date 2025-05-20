import os
from typing import BinaryIO
from google.cloud import storage
from google.cloud.storage.blob import Blob
import asyncio
from functools import partial

class AsyncStorageClient:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    async def upload_file(self, file: BinaryIO, destination: str) -> str:
        """파일을 비동기적으로 업로드"""
        blob = self.bucket.blob(destination)
        
        # 스레드 풀에서 동기 업로드 실행
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            partial(blob.upload_from_file, file)
        )
        
        return blob.public_url

    async def download_file(self, source: str) -> bytes:
        """파일을 비동기적으로 다운로드"""
        blob = self.bucket.blob(source)
        
        # 스레드 풀에서 동기 다운로드 실행
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            blob.download_as_bytes
        )

    async def delete_file(self, file_path: str) -> bool:
        """파일을 비동기적으로 삭제"""
        blob = self.bucket.blob(file_path)
        
        # 스레드 풀에서 동기 삭제 실행
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            blob.delete
        )
        
        return True 