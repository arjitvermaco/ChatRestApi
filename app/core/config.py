from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    ENVIRONMENT: str = "development"
    MAX_TOKENS: int = 2000
    MODEL_NAME: str = "gpt-3.5-turbo"

    class Config:
        env_file = ".env"

settings = Settings() 