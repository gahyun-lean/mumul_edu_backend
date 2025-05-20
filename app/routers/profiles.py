from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.profile import ProfileCreate, ProfileRead
from app.dependencies.auth import get_current_user
from app.dependencies.services import get_services, Services

router = APIRouter(prefix="/api/profiles", tags=["profiles"])

@router.post("", response_model=ProfileRead, status_code=status.HTTP_201_CREATED, summary="프로필 생성")
async def create_profile(
    payload: ProfileCreate, 
    user: dict = Depends(get_current_user), 
    services: Services = Depends(get_services)
):
    return services.profile.create_profile(payload, user["id"], user["email"])

@router.get("/me", response_model=ProfileRead, status_code=status.HTTP_200_OK, summary="프로필 조회")
async def read_my_profile(
    user: dict = Depends(get_current_user), 
    services: Services = Depends(get_services)
):
    return services.profile.read_my_profile(user["id"])