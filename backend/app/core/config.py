from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:prasad123@localhost:5432/clinic_management"
    SECRET_KEY: str = "change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    FRONTEND_URL: str = "http://localhost:5173"
    MAIL_FROM: str = "clinic@example.com"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
