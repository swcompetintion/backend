# 코드에 노출되지 않기를 바라는 설정 명시, 도커와 잘 어울림
from pydantic_settings import BaseSettings,SettingsConfigDict
#  BaseSettings에는 SettingsConfigDict로 설정 관리
from pathlib import Path
import os
BASE_DIR = Path(__file__).parent.parent.parent



class Settings(BaseSettings):
# 민감한 정보 (환경변수로만)
    DATABASE_URL: str | None = None

    GOOGLE_CLIENT_ID: str | None = None

    GOOGLE_CLIENT_SECRET: str | None = None
# 개발 설정 (기본값)
    frontend_url: str = "http://localhost:3002"
    api_port: str = "8888"
    host: str = "0.0.0.0" # 모든 인터페이스에서 접속 허용, 환경변수로 쉽게 오버라이딩 가능

    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    log_level: str = "INFO"
    enable_debug: str = "false"
# 보안 설정
    secret_key: str = "default-secret-key-change-in-production"
    use_https: str = "false"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR/".env",
        env_file_encoding='utf-8',
        extra='allow'
    ) #https://docs.pydantic.dev/2.0/usage/pydantic_settings/?utm_source=chatgpt.com#dotenv-env-support


settings = Settings()
