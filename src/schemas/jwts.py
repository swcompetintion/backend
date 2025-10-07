from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class JwtCreate(BaseModel):
    jti: str
    exp: datetime
    user_id: str
    token_type: str = "refresh"
    
    model_config = ConfigDict(extra='allow')


class JwtResponse(BaseModel):
    id: str = Field(alias="_id")
    jti: str
    exp: datetime
    user_id: str
    token_type: str
    
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
