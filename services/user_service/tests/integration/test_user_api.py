import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "strongpassword123",
                "username": "testuser"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert "id" in data

@pytest.mark.asyncio
async def test_register_duplicate_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Register first user
        await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "strongpassword123",
                "username": "testuser"
            }
        )
        
        # Try to register duplicate user
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "strongpassword123",
                "username": "testuser"
            }
        )
        assert response.status_code == 400 