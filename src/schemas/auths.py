from pydantic import BaseModel


class GoogleVerifyRequest(BaseModel):
    code: str
