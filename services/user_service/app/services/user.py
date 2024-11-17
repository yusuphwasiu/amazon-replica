from typing import Optional
from app.schemas.user import UserCreate, User
from app.core.exceptions import UserAlreadyExistsError
from app.core.security import get_password_hash
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.core.security import get_password_hash, verify_password
from app.schemas.user import ProfileUpdate, UserProfile
from app.core.exceptions import InvalidCredentialsError

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def create_user(self, user_data: UserCreate) -> User:
        # This is a temporary implementation until we add database
        # In TDD, we start with the minimal implementation to make tests pass
        if hasattr(self, '_users') and any(u.email == user_data.email for u in self._users):
            raise UserAlreadyExistsError()
            
        if not hasattr(self, '_users'):
            self._users = []
            
        hashed_password = get_password_hash(user_data.password)
        user = User(
            id=len(self._users) + 1,
            email=user_data.email,
            username=user_data.username
        )
        self._users.append(user)
        return user 

    async def update_profile(self, user_id: int, profile_data: ProfileUpdate) -> UserProfile:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
            
        # Update user profile
        for field, value in profile_data.dict(exclude_unset=True).items():
            setattr(user, field, value)
            
        await self.user_repo.update(user)
        return UserProfile.from_orm(user)

    async def change_password(
        self, 
        user_id: int, 
        current_password: str, 
        new_password: str
    ) -> bool:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
            
        # Verify current password
        if not verify_password(current_password, user.hashed_password):
            raise InvalidCredentialsError()
            
        # Update password
        user.hashed_password = get_password_hash(new_password)
        await self.user_repo.update(user)
        return True

    async def request_password_reset(self, email: str) -> str:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("User not found")
            
        # Generate reset token
        reset_token = self._generate_reset_token(user.id)
        
        # TODO: Send email with reset token
        # This would integrate with an email service
        
        return reset_token

    def _generate_reset_token(self, user_id: int) -> str:
        # Generate a secure reset token
        # This is a simplified version - in production, use more secure method
        return f"reset_{user_id}_{datetime.utcnow().timestamp()}"