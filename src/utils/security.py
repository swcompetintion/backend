from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.core.config import settings
from src.models.users import UserModel
from src.services.auth_service import AuthService
from src.utils.jwt_utils import ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/google-verify")


async def get_current_user(token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends()) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await auth_service.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user
