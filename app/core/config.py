from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MYSQL_DSN: str = "mysql://user:password@localhost:3306/analytics"
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "analytics"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
