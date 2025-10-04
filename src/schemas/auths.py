from pydantic import BaseModel


class GoogleVerifyRequest(BaseModel):
    id_token: str
