from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    MYSQL_DSN: str = "mysql+pymysql://user:password@localhost:3306/analytics"
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "analytics"
    DEBUG: bool = False
    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings(_env_file=".env")
