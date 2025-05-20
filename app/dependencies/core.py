from fastapi import Depends
from app.core.config import settings
from supabase import Client
from app.core.supabase_client import supabase

def get_settings():
    return settings

def get_supabase() -> Client:
    return supabase
