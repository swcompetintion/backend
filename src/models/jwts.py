from beanie import Document, Indexed
from pydantic import ConfigDict, Field
from datetime import datetime
import pymongo


class RefreshTokenModel(Document):
    user_id: str
    jti: str
    expire_at: datetime = Field(..., alias="exp")

    model_config = ConfigDict(
        extra='forbid',
        json_schema_extra={
            "example": {
                "user_id": "user_123",
                "jti": "jwt_unique_id_123",
                "expire_at": "2023-10-01T18:00:00Z",
            }
        }
    )

    class Settings:
        name = "refresh_tokens"
        indexes = [
            [["expire_at", pymongo.ASCENDING]],
            "jti"
        ]
