# 코드에 노출되지 않기를 바라는 설정 명시, 도커와 잘 어울림
from pydantic_settings import BaseSettings,SettingsConfigDict
#  BaseSettings에는 SettingsConfigDict로 설정 관리
from pathlib import Path
import os
BASE_DIR = Path(__file__).parent.parent.parent



class Settings(BaseSettings):

    DATABASE_URL: str | None = None

    GOOGLE_CLIENT_ID: str | None = None

    GOOGLE_CLIENT_SECRET: str | None = None

    frontend_url: str = "http://localhost:3000"
    api_port: str = "8000"
    host: str = "0.0.0.0"

    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    log_level: str = "INFO"
    enable_debug: str = "false"

    secret_key: str = "default-secret-key-change-in-production"
    use_https: str = "false"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR/".env",
        env_file_encoding='utf-8',
        extra='allow'
    ) #https://docs.pydantic.dev/2.0/usage/pydantic_settings/?utm_source=chatgpt.com#dotenv-env-support


settings = Settings()
