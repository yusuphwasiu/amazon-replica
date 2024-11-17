from pydantic import BaseModel, EmailStr, constr

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    # Password must be min 8 chars, max 100 chars
    password: constr(min_length=8, max_length=100)

class User(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True 