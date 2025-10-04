from pydantic import BaseModel, ConfigDict
from typing import Optional


class PlanCreate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    location: Optional[str] = None
    created_at: Optional[str] = None
    
    model_config = ConfigDict(extra='allow')


class PlanUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    location: Optional[str] = None
    created_at: Optional[str] = None
    
    model_config = ConfigDict(extra='allow')


class PlanResponse(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    location: Optional[str] = None
    created_at: Optional[str] = None
    
    model_config = ConfigDict(extra='allow')
