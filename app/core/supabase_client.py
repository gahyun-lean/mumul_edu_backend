import os
from dotenv import load_dotenv, find_dotenv
from supabase import create_client, Client

load_dotenv(find_dotenv())

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL:
    raise RuntimeError("환경변수 SUPABASE_URL 이 설정되지 않았습니다. .env 파일을 확인하세요.")
if not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("환경변수 SUPABASE_SERVICE_ROLE_KEY 가 설정되지 않았습니다. .env 파일을 확인하세요.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
