from pydantic import ConfigDict
from src.core.base import Plan
from beanie import Document
from typing import Optional


class PlanModel(Plan, Document):
    id: Optional[int] = None
    model_config = ConfigDict(
        extra='allow',  # Allow extra fields
        json_schema_extra={
            "example": {
                "id": '68e4b374fe8048d7bf5336bb', # 몽고디비는 이렇게 됨
                "title": "Plan",
                "description": "Plan",
                "tags": ["#test", "#Plan"],
                "location": "삼육대",
                "created_at": "2023-10-01T12:00:00Z"
            }
        }
    )
