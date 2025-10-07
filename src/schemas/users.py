from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class UserCreate(BaseModel):
    user_id: str
    email: str
    plans: Optional[List[str]] = []
    
    model_config = ConfigDict(extra='allow')


class UserUpdate(BaseModel):
    email: Optional[str] = None
    plans: Optional[List[str]] = None
    
    model_config = ConfigDict(extra='allow')


class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    email: str
    plans: Optional[List[str]] = []
    
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
