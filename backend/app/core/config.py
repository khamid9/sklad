from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = 'postgresql+psycopg://postgres:postgres@localhost:5432/my_sklad'
    secret_key: str = 'change-this-secret-in-production'
    access_token_expire_minutes: int = 1440
    cors_origins: str = 'http://localhost:5173'
    admin_email: str = ''
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
