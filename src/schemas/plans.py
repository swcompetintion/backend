from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class PlanCreate(BaseModel):
    plan_id: Optional[str] = None
    title: str
    content: Optional[str] = None
    important: Optional[bool] = False
    date: Optional[str] = None
    
    model_config = ConfigDict(extra='allow')


class PlanUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    important: Optional[bool] = None
    date: Optional[str] = None
    
    model_config = ConfigDict(extra='allow')


class PlanResponse(BaseModel):
    id: str = Field(alias="_id")
    plan_id: Optional[str] = None
    title: str
    content: Optional[str] = None  # description → content  
    important: Optional[bool] = False
    date: Optional[str] = None
    created_at: Optional[str] = None  # datetime → str
    
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
