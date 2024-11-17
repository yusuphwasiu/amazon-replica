from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import get_current_user
from app.schemas.user import UserProfile, ProfileUpdate, PasswordChange
from app.services.user import UserService
from app.db.base import get_db

router = APIRouter()

@router.get("/me", response_model=UserProfile)
async def get_profile(current_user: UserProfile = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserProfile)
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: UserProfile = Depends(get_current_user),
    user_service: UserService = Depends()
):
    return await user_service.update_profile(current_user.id, profile_data)

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: UserProfile = Depends(get_current_user),
    user_service: UserService = Depends()
):
    await user_service.change_password(
        current_user.id,
        password_data.current_password,
        password_data.new_password
    )
    return {"message": "Password changed successfully"}

@router.post("/reset-password")
async def request_password_reset(
    email: str,
    user_service: UserService = Depends()
):
    try:
        reset_token = await user_service.request_password_reset(email)
        return {"message": "Password reset instructions sent to email"}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        ) 