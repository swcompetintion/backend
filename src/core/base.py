
from pydantic import BaseModel
from typing import Optional


class Plan(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    location: Optional[str] = None
    created_at: Optional[str] = None
