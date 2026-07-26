from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI HealthCare Backend"
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    MONGODB_URL: str = "mongodb://127.0.0.1:27017"
    DATABASE_NAME: str = "ai_healthcare"
    SECRET_KEY: str = "change-this-development-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GEMINI_API_KEY: str = ""
    UPLOAD_DIR: str = "./static/uploads"
    PRESCRIPTION_DIR: str = "./static/prescriptions"
    REPORTS_DIR: str = "./static/reports"
    IMAGES_DIR: str = "./static/images"
    AUDIO_DIR: str = "./static/audio"
    TEMP_DIR: str = "./static/temp"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def get_absolute_path(self, path: str) -> Path:
        candidate = Path(path)
        return candidate if candidate.is_absolute() else Path.cwd() / candidate

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, str) and value.lower() in {"release", "production"}:
            return False
        return value


settings = Settings()
