from pydantic import BaseModel
from typing import Optional


class Plan(BaseModel):
    title: str
    content: Optional[str] = None
    tags: Optional[list[str]] = None
    location: Optional[str] = None
    created_at: Optional[str] = None
