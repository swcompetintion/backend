from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta


class Jwt(BaseModel):
    access_token: str
    refresh_token: str = None


class JwtRequest(BaseModel):
    jti: str # JWT ID
    sub: int # Subject (user ID) -> str로 변경해야 함
    email: EmailStr
    exp: datetime = datetime.now()+timedelta(days=1) # 1일 만료

# 사용되지 않는 스키마