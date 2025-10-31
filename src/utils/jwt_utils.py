from datetime import datetime, timedelta
import uuid
from jose import jwt
from src.core.config import settings

ALGORITHM = "HS256" # 대칭키 암호화
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 30분
REFRESH_TOKEN_EXPIRE_DAYS = 14 # 14일


def create_access_token(data: dict) -> str:
    to_encode = data.copy() # 입력 데이터 복사
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # 30분 후 만료
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())}) # 만료시간 + 고유ID 추가
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> tuple[str, datetime]:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt, expire # 토큰과 만료시간 둘 다 반환, DB 저장을 위해 만료시간도 함께 반환
