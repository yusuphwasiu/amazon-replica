import pytest
from app.services.auth import AuthService
from app.schemas.auth import TokenResponse
from app.core.exceptions import InvalidCredentialsError

@pytest.mark.asyncio
async def test_login_success(db_session):
    auth_service = AuthService(db_session)
    # First create a user
    await auth_service.register(
        email="test@example.com",
        password="strongpassword123",
        username="testuser"
    )
    
    # Try to login
    token = await auth_service.login(
        email="test@example.com",
        password="strongpassword123"
    )
    assert isinstance(token, TokenResponse)
    assert token.token_type == "bearer"
    assert token.access_token is not None

@pytest.mark.asyncio
async def test_login_invalid_credentials(db_session):
    auth_service = AuthService(db_session)
    with pytest.raises(InvalidCredentialsError):
        await auth_service.login(
            email="test@example.com",
            password="wrongpassword"
        ) 