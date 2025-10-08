from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta


class Jwt(BaseModel):
    access_token: str
    refresh_token: str = None


class JwtRequest(BaseModel):
    jti: str
    sub: int
    email: EmailStr
    exp: datetime = datetime.now()+timedelta(days=1)
