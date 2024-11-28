import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate

def test_valid_user_creation():
    user_data = {
        "email": "test@example.com",
        "password": "strongpassword123",
        "username": "testuser"
    }
    user = UserCreate(**user_data)
    assert user.email == user_data["email"]
    assert user.username == user_data["username"]
    assert user.password == user_data["password"]

def test_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            email="invalid-email",
            password="strongpassword123",
            username="testuser"
        )

def test_invalid_password_too_short():
    with pytest.raises(ValidationError):
        UserCreate(
            email="test@example.com",
            password="short",  # Too short password
            username="testuser"
        ) 