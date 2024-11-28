from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "User Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/user_db"
    TEST_DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/test_user_db"
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    SES_SOURCE_EMAIL: str
    
    class Config:
        case_sensitive = True
        env_file = ".env" 