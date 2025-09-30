from pydantic import ConfigDict
from backend.core.base import Plan
from beanie import Document
from typing import Optional


class PlanModel(Plan, Document):
    id: Optional[int] = None
    model_config = ConfigDict(
        extra='allow',  # Allow extra fields
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Plan",
                "description": "Plan",
                "tags": ["#test", "#Plan"],
                "location": "삼육대",
                "created_at": "2023-10-01T12:00:00Z"
            }
        }
    )
