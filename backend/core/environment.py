import os
from typing import Literal
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

# 환경 타입 정의
Environment = Literal["development", "production", "staging"]

class Settings(BaseSettings):
    # 환경 설정
    ENVIRONMENT: Environment = "development"
    
    # 데이터베이스 설정
    DATABASE_URL: str | None = None
    
    # Google OAuth 설정
    GOOGLE_CLIENT_ID: str | None = None
    
    # 서버 설정
    FRONTEND_URL: str = "http://localhost:3000"
    API_PORT: int = 8000
    HOST: str = "127.0.0.1"
    
    # CORS 설정
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    ENABLE_DEBUG: bool = False
    
    # 보안 설정
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    USE_HTTPS: bool = False

    model_config = ConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._configure_environment_defaults()

    def _configure_environment_defaults(self):
        """환경별 기본값 설정"""
        if self.ENVIRONMENT == "development":
            self.HOST = "0.0.0.0"  # Docker 환경에서 외부 접근 허용
            self.ENABLE_DEBUG = True
            self.LOG_LEVEL = "DEBUG"
            self.ALLOWED_ORIGINS = [
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "http://0.0.0.0:3000"
            ]
            
        elif self.ENVIRONMENT == "staging":
            self.HOST = "0.0.0.0"
            self.ENABLE_DEBUG = True
            self.LOG_LEVEL = "INFO"
            self.USE_HTTPS = True
            
        elif self.ENVIRONMENT == "production":
            self.HOST = "0.0.0.0"
            self.ENABLE_DEBUG = False
            self.LOG_LEVEL = "WARNING"
            self.USE_HTTPS = True

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def is_staging(self) -> bool:
        return self.ENVIRONMENT == "staging"

# 환경 감지
def get_environment() -> Environment:
    """현재 환경을 감지합니다"""
    # 명시적 환경변수 확인
    explicit_env = os.getenv("ENVIRONMENT")
    if explicit_env in ["development", "production", "staging"]:
        return explicit_env  # type: ignore
    
    # 기타 환경변수 기반 추론
    if os.getenv("AWS_EXECUTION_ENV"):  # AWS Lambda/ECS
        return "production"
    if os.getenv("KUBERNETES_SERVICE_HOST"):  # Kubernetes
        return "production"
    if os.getenv("DOCKER_CONTAINER"):  # Docker 운영환경
        return "production"
    
    # 개발환경 지표
    if os.getenv("NODE_ENV") == "development":
        return "development"
    if os.path.exists("/.dockerenv") and not os.getenv("PRODUCTION"):
        return "development"
    
    # 기본값: development (로컬 개발)
    return "development"

# 전역 설정 객체
settings = Settings(ENVIRONMENT=get_environment())
