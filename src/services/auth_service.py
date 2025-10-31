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
        user = await UserModel.find_one(UserModel.email == email) # 이메일로 검색
        if not user:
            user = UserModel(email=email) # 없으면 새로 생성
            await user.create()
        return user

    async def get_user_by_id(self, user_id: str) -> Optional[UserModel]:
        return await UserModel.get(user_id)

    async def store_refresh_token(self, user_id: str, jti: str, expire_at: datetime) -> None:
        """
        DB에 Refresh Token 정보 저장
        """
        refresh_token = RefreshTokenModel(
            user_id=user_id, jti=jti, expire_at=expire_at)
        await refresh_token.create()

    async def validate_refresh_token(self, token: str) -> dict:
        """
        1. JWT 디코딩
        2. DB에서 jti 존재 확인 (화이트리스트 방식)
        3. 유효하면 payload 반환
        """
        try:
            payload = jwt.decode(token, settings.secret_key,
                                 algorithms=[ALGORITHM])
            jti = payload.get("jti")
            if not jti:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

            token_in_db = await RefreshTokenModel.find_one(RefreshTokenModel.jti == jti) # 발급한 모든 유효한 토큰을 DB에 저장,  확실한 제어 및 강제 로그아웃 쉬움, 하지만 DB조회 필요(성능 부담)
            if not token_in_db: # DB에 없으면 무효한 토큰
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found")

            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    async def delete_refresh_token(self, jti: str) -> None:
        """
        개별 토큰 삭제(로그아웃)
        """
        token_to_delete = await RefreshTokenModel.find_one(RefreshTokenModel.jti == jti)
        if token_to_delete:
            await token_to_delete.delete()

    async def delete_all_refresh_tokens_for_user(self, user_id: str) -> None:
        """
        사용자의 모든 토큰 삭제 (전체 로그아웃)
        """
        await RefreshTokenModel.find(RefreshTokenModel.user_id == user_id).delete()

# 블랙리스트를 사용하면 대부분 DB 조회 안함, 단 강제 로그아웃 복잡해짐
# 성능 최적화 방법:
# Redis 캐싱: 자주 사용하는 토큰 정보 캐시
# 토큰 수명 단축: 자주 갱신하지만 DB 조회 빈도 감소
# 배치 삭제: 만료된 토큰 주기적으로 일괄 삭제