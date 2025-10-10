from fastapi import APIRouter, HTTPException, Depends, Response, Cookie
from typing import Annotated
from ..schemas.auths import GoogleVerifyRequest
import httpx
from ..core.config import settings
from ..services.auth_service import AuthService
from ..utils.jwt_utils import create_access_token, create_refresh_token
from jose import jwt, JWTError
auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.post("/google-verify")
async def google_verify(payload: GoogleVerifyRequest, response: Response, auth_service: AuthService = Depends()):
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
        token_resp = await client.post(token_endpoint, data=data)

    if token_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Token exchange failed")

    id_token = token_resp.json()["id_token"]
    verify_endpoint = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"

    async with httpx.AsyncClient() as client:
        verify_resp = await client.get(verify_endpoint)

    if verify_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid Google token")

    user_info = verify_resp.json()
    user = await auth_service.get_or_create_user(user_info["email"])

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token, expire_at = create_refresh_token(
        data={"sub": str(user.id)})

    await auth_service.store_refresh_token(user_id=str(user.id), jti=jwt.get_unverified_claims(refresh_token)['jti'], expire_at=expire_at)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.use_https == "true",
        samesite='strict'
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/refresh")
async def refresh_access_token(refresh_token: Annotated[str | None, Cookie()] = None, auth_service: AuthService = Depends()):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not found")

    payload = await auth_service.validate_refresh_token(refresh_token)
    user = await auth_service.get_user_by_id(payload['sub'])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/logout")
async def logout(response: Response, refresh_token: Annotated[str | None, Cookie()] = None, auth_service: AuthService = Depends()):
    if refresh_token:
        try:
            payload = jwt.get_unverified_claims(refresh_token)
            await auth_service.delete_refresh_token(payload['jti'])
        except JWTError:
            pass

    response.delete_cookie(key="refresh_token")
    return {"message": "Logout successful"}
