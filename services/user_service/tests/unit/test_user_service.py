import pytest
from app.services.user import UserService
from app.schemas.user import UserCreate
from app.core.exceptions import UserAlreadyExistsError

@pytest.mark.asyncio
async def test_create_user():
    user_service = UserService()
    user_data = UserCreate(
        email="test@example.com",
        password="strongpassword123",
        username="testuser"
    )
    user = await user_service.create_user(user_data)
    assert user.email == user_data.email
    assert user.username == user_data.username

@pytest.mark.asyncio
async def test_create_duplicate_user():
    user_service = UserService()
    user_data = UserCreate(
        email="test@example.com",
        password="strongpassword123",
        username="testuser"
    )
    await user_service.create_user(user_data)
    
    with pytest.raises(UserAlreadyExistsError):
        await user_service.create_user(user_data) 