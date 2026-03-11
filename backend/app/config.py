from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://app:changeme@localhost:5432/investor_tracking"
    secret_key: str = "changeme_jwt_secret_key_min_32_chars"
    admin_username: str = "admin"
    admin_password: str = "changeme"
    access_token_expire_hours: int = 24
    crawl_schedule_hour: int = 7
    crawl_schedule_minute: int = 0
    crawl_enabled: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
