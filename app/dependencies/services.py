from fastapi import Depends
from app.core.config import settings
from app.core.supabase_client import supabase
from app.dependencies.core import get_supabase

from app.services.dify_service import DifyService
from app.services.auth import AuthService
from app.services.profile import ProfileService
from app.services.course import CourseService
from app.services.course_code import CourseCodeService
from app.services.enrollment import EnrollmentService
from app.services.document import DocumentService

from app.repositories.implementations.supabase.profile_repository import ProfileRepository
from app.repositories.implementations.supabase.course_repository import CourseRepository
from app.repositories.implementations.supabase.course_code_repository import CourseCodeRepository
from app.repositories.implementations.supabase.enrollment_repository import EnrollmentRepository
from app.repositories.implementations.supabase.document_repository import DocumentRepository

class Services:
    def __init__(
        self, 
        supabase_client,
        auth_service = None,
        profile_service = None,
        dify_service = None,
        course_service = None,
        course_code_service = None,
        enrollment_service = None,
        document_service = None
    ):
        self.supabase = supabase_client
        self.auth = auth_service or AuthService(supabase_client)
        self.profile = profile_service or ProfileService(ProfileRepository(supabase_client))
        self.dify = dify_service or DifyService(api_key=settings.DIFY_API_KEY)
        self.course = course_service or CourseService(CourseRepository(supabase_client))
        self.course_code = course_code_service or CourseCodeService(CourseCodeRepository(supabase_client))
        self.enrollment = enrollment_service or EnrollmentService(
            EnrollmentRepository(supabase_client),
            CourseCodeRepository(supabase_client),
            CourseRepository(supabase_client)
        )
        self.document = document_service or DocumentService(DocumentRepository(supabase_client), dify=self.dify)

# 서비스 의존성 함수
def get_services(supabase=Depends(get_supabase)) -> Services:
    return Services(supabase)

def get_dify_service():
    from app.services.dify_service import DifyService
    return DifyService(api_key=settings.DIFY_API_KEY)
