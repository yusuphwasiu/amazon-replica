import pytest
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.models.user import User

@pytest.mark.asyncio
async def test_create_user_in_db(db_session):
    repo = UserRepository(db_session)
    user_data = UserCreate(
        email="test@example.com",
        password="strongpassword123",
        username="testuser"
    )
    user = await repo.create(user_data)
    assert user.email == user_data.email
    assert user.username == user_data.username

@pytest.mark.asyncio
async def test_get_user_by_email(db_session):
    repo = UserRepository(db_session)
    user_data = UserCreate(
        email="test@example.com",
        password="strongpassword123",
        username="testuser"
    )
    created_user = await repo.create(user_data)
    found_user = await repo.get_by_email(user_data.email)
    assert found_user.id == created_user.id
    assert found_user.email == created_user.email 