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

@pytest.mark.asyncio
async def test_update_user_profile(db_session):
    user_service = UserService(db_session)
    # Create user first
    user = await user_service.create_user(UserCreate(
        email="test@example.com",
        password="strongpassword123",
        username="testuser"
    ))
    
    # Update profile
    updated_user = await user_service.update_profile(
        user.id,
        {
            "full_name": "Test User",
            "phone_number": "+1234567890",
            "address": "123 Test St"
        }
    )
    
    assert updated_user.full_name == "Test User"
    assert updated_user.phone_number == "+1234567890"
    assert updated_user.address == "123 Test St"

@pytest.mark.asyncio
async def test_change_password(db_session):
    user_service = UserService(db_session)
    # Create user
    user = await user_service.create_user(UserCreate(
        email="test@example.com",
        password="oldpassword123",
        username="testuser"
    ))
    
    # Change password
    await user_service.change_password(
        user.id,
        "oldpassword123",
        "newpassword123"
    )
    
    # Verify new password works
    auth_result = await user_service.verify_credentials(
        user.email,
        "newpassword123"
    )
    assert auth_result is True

@pytest.mark.asyncio
async def test_request_password_reset(db_session):
    user_service = UserService(db_session)
    # Create user
    user = await user_service.create_user(UserCreate(
        email="test@example.com",
        password="password123",
        username="testuser"
    ))
    
    # Request password reset
    reset_token = await user_service.request_password_reset(user.email)
    assert reset_token is not None 