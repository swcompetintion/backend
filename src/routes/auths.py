from fastapi import APIRouter, HTTPException
from ..schemas.auths import GoogleVerifyRequest
from ..schemas.jwts import Jwt
import httpx
from ..core.config import settings

auth_router = APIRouter(
    prefix="/auth"
)


@auth_router.post("/google-verify")
async def google_verify(payload: GoogleVerifyRequest):
    code = payload.code
    token_endpoint = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": "postmessage",
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(token_endpoint, data=data)

    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Token exchange failed")

    tokens = resp.json()
    id_token = tokens["id_token"]

    verify_endpoint = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
    async with httpx.AsyncClient() as client:
        verify_resp = await client.get(verify_endpoint)

    if verify_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid Google token")

    token_info = verify_resp.json()
    user_email = token_info.get("email")

    return {"access_token": user_email, "token_type": "bearer"}
