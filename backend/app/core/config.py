from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("BACKEND_DATABASE_URL", "sqlite:///./dev.db")
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

settings = Settings()
