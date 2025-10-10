from beanie import Document
from pydantic import ConfigDict, EmailStr
from ..schemas.plans import Plan


class UserModel(Document):
    email: EmailStr
    plans: list[Plan] = []

    model_config = ConfigDict(
        extra='allow',
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "google_123456789",
                "email": "user@example.com",
                "plans": ["68e4b374fe8048d7bf5336bb"]
            }
        }
    )

    class Settings:
        name = "user"
        indexes = ["email"]
