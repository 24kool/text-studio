from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Keys
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    # App Settings
    app_name: str = "Text Studio API"
    debug: bool = False
    
    # File Upload Settings
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list[str] = [".txt", ".pdf", ".png", ".jpg", ".jpeg", ".webp"]
    upload_dir: str = "uploads"
    
    # AI Model Settings
    default_ai_provider: str = "gemini"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
