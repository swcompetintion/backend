from pydantic import BaseModel


class GoogleVerifyRequest(BaseModel):
    code: str # 프론트엔드에서 받은 구글 코드 저장
