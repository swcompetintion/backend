from datetime import datetime
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from src.core.config import settings
from src.models.users import UserModel
from src.models.jwts import RefreshTokenModel
from src.utils.jwt_utils import ALGORITHM


class AuthService:
    async def get_or_create_user(self, email: str) -> UserModel:
        user = await UserModel.find_one(UserModel.email == email)
        if not user:
            user = UserModel(email=email)
            await user.create()
        return user

    async def get_user_by_id(self, user_id: str) -> Optional[UserModel]:
        return await UserModel.get(user_id)

    async def store_refresh_token(self, user_id: str, jti: str, expire_at: datetime) -> None:
        refresh_token = RefreshTokenModel(
            user_id=user_id, jti=jti, expire_at=expire_at)
        await refresh_token.create()

    async def validate_refresh_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.secret_key,
                                 algorithms=[ALGORITHM])
            jti = payload.get("jti")
            if not jti:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

            token_in_db = await RefreshTokenModel.find_one(RefreshTokenModel.jti == jti)
            if not token_in_db:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found")

            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    async def delete_refresh_token(self, jti: str) -> None:
        token_to_delete = await RefreshTokenModel.find_one(RefreshTokenModel.jti == jti)
        if token_to_delete:
            await token_to_delete.delete()

    async def delete_all_refresh_tokens_for_user(self, user_id: str) -> None:
        await RefreshTokenModel.find(RefreshTokenModel.user_id == user_id).delete()
