from beanie import Document, before_event, Insert
from pydantic import ConfigDict
from typing import Optional
from datetime import datetime


class PlanModel(Document):
    plan_id: Optional[str] = None
    title: str
    content: Optional[str] = None
    important: Optional[bool] = False
    date: Optional[str] = None
    created_at: Optional[str] = None
    
    @before_event(Insert)
    def set_created_at(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    model_config = ConfigDict(
        extra='allow',
        json_schema_extra={
            "example": {
                "plan_id": "PLAN001",
                "title": "팀 미팅 준비",
                "content": "프로젝트 진행상황 정리 및 발표자료 준비",
                "important": True,
                "date": "2023-10-15",
                "created_at": "2023-10-01T12:00:00Z"
            }
        }
    )
    
    class Settings:
        name = "plans"
        indexes = ["plan_id", "created_at"]
