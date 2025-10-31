from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.models.users import UserModel
from src.services.auth_service import AuthService
from src.utils.jwt_utils import ALGORITHM
from src.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
# 자동 토큰 추출: Authorization: Bearer <token> 헤더에서
# Swagger UI: 자동으로 인증 버튼 생성
# 토큰 URL: /auth/token (실제로는 사용 안함, 문서용)
# 실제 토큰 엔드포인트는 /auth/google-verify

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends()
) -> UserModel:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ) # 에러 응답
    print(f"Decoding token: {token}")
    try:
        payload = jwt.decode(token, key=settings.secret_key,
                             algorithms=[ALGORITHM])
        user_id: str = payload.get("sub") # JWT의 "subject" 클레임에서 사용자 ID 추출
        if user_id is None:
            print('User ID not found in token')
            raise credentials_exception  # 토큰에 사용자 ID가 없으면 에러
    except JWTError as e:
        print('JWTError occurred', e)
        raise credentials_exception  # DB에 사용자가 없으면 에러

    user = await auth_service.get_user_by_id(user_id) # DB에서 사용자 조회 -> 캐시에서 가져오도록 변경 할 것
    if user is None:
        print('User not found')
        raise credentials_exception
    return user

'''
1. 클라이언트: Authorization: Bearer eyJ0eXAiOiJKV1Q...
2. oauth2_scheme: 헤더에서 토큰 자동 추출
3. jwt.decode(): 토큰 검증 + payload 추출
4. get_user_by_id(): DB에서 사용자 조회
5. API 엔드포인트: 인증된 UserModel로 로직 실행
'''