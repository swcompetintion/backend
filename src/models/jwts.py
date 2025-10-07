from beanie import Document
from pydantic import ConfigDict
from datetime import datetime


class JwtModel(Document):
    jti: str
    exp: datetime
    user_id: str
    token_type: str = "refresh"
    
    model_config = ConfigDict(
        extra='allow',
        json_schema_extra={
            "example": {
                "jti": "jwt_unique_id_123",
                "exp": "2023-10-01T18:00:00Z",
                "user_id": "google_123456789",
                "token_type": "refresh"
            }
        }
    )
    
    class Settings:
        name = "jwts"
        indexes = ["jti", "user_id", "exp"]
