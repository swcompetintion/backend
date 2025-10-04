from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from pathlib import Path
BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str | None = "mongodb://mongodb_container:27017/bedrock"
    
    # Environment
    environment: str = "development"
    
    # Google OAuth
    google_client_id: str | None = None
    
    # Server configuration
    frontend_url: str = "http://localhost:3000"
    api_port: str = "8000"
    host: str = "0.0.0.0"
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # Logging
    log_level: str = "INFO"
    enable_debug: str = "false"
    
    # Security
    secret_key: str = "default-secret-key-change-in-production"
    use_https: str = "false"

    model_config = ConfigDict(
        env_file=BASE_DIR/".env",
        extra='allow'  # Allow extra fields from environment variables
    )


settings = Settings()
