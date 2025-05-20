from app.routers.auth import router as auth_router
from app.routers.profiles import router as profiles_router
from app.routers.courses import router as courses_router
from app.routers.course_codes import router as course_codes_router
from app.routers.documents import router as documents_router
# from chat import router as chat_router
from app.routers.enrollments import router as enrollments_router

__all__ = [
    "auth_router", 
    "profiles_router", 
    "courses_router", 
    "course_codes_router", 
    "enrollments_router",
    "documents_router", 
    # "chat_router"
    ]
