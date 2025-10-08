from beanie import Document
from pydantic import ConfigDict
from datetime import datetime


class RefreshTokenModel(Document):
    jti: str
    exp: datetime

    model_config = ConfigDict(
        extra='forbid',
        json_schema_extra={
            "example": {
                "jti": "jwt_unique_id_123",
                "exp": "2023-10-01T18:00:00Z",
            }
        }
    )

    class Settings:
        name = "jwt"
        indexes = ["jti"]
