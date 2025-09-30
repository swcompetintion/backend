from fastapi import APIRouter, HTTPException
from ..schemas.auths import GoogleVerifyRequest
import httpx


auth_router = APIRouter(
    prefix="/auths"
)


@auth_router.post("/google-verify")
async def google_verify(payload: GoogleVerifyRequest):

    id_token = payload.id_token
    verify_endpoint = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(verify_endpoint)

    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid Google token")

    token_info = resp.json()

    user_email = token_info["email"]

    return {"access_token":  user_email, "token_type": "bearer"}
