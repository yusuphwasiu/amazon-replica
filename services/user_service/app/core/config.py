from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "User Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/user_db"
    TEST_DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/test_user_db"
    
    class Config:
        case_sensitive = True
        env_file = ".env" 