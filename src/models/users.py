from beanie import Document
from typing import Optional, List
from pydantic import ConfigDict


class UserModel(Document):
    user_id: str
    email: str
    plans: Optional[List[str]] = []
    
    model_config = ConfigDict(
        extra='allow',
        json_schema_extra={
            "example": {
                "user_id": "google_123456789",
                "email": "user@example.com",
                "plans": ["68e4b374fe8048d7bf5336bb"]
            }
        }
    )
    
    class Settings:
        name = "users"
        indexes = ["user_id", "email"]
