from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from pathlib import Path
import os
BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):

    DATABASE_URL: str | None = os.getenv('DATABASE_URL')

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

    model_config = ConfigDict(
        env_file=BASE_DIR/".env",
        extra='allow'
    )


settings = Settings()
