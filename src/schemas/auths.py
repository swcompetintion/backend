from pydantic import BaseModel


class GoogleVerifyRequest(BaseModel):
    code: str # 프론트엔드에서 받은 구글 코드 저장
    redirect_url: str | None = "postmessage" # 리다이렉트 URL, 기본값은 "postmessage"
    
