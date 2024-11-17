from typing import Optional
from app.schemas.user import UserCreate, User
from app.core.exceptions import UserAlreadyExistsError
from app.core.security import get_password_hash

class UserService:
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