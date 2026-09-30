from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "BharatVerify API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    GEMINI_API_KEY: Optional[str] = None
    
    # Database
    DATABASE_URL: str
    
    # CORS
    FRONTEND_URL: str = "http://localhost:5173"
    
    # ML settings
    EMBEDDING_DEVICE: str = "auto"
    
    model_config = SettingsConfigDict(env_file="../../.env", env_ignore_empty=True, extra="ignore")

settings = Settings()
