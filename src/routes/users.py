from fastapi import APIRouter, Depends, Response
from src.models.users import UserModel
from src.utils.security import get_current_user
from src.services.auth_service import AuthService

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@user_router.get("/me", response_model=dict)
async def get_current_user_info(current_user: UserModel = Depends(get_current_user)):
    """현재 사용자 정보 조회 - 테스트에서 사용하는 API"""
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "created_at": current_user.created_at if hasattr(current_user, 'created_at') else None
    }


@user_router.delete("/me")
async def delete_user_me(response: Response, current_user: UserModel = Depends(get_current_user), auth_service: AuthService = Depends()):

    await auth_service.delete_all_refresh_tokens_for_user(str(current_user.id))

    await current_user.delete() # 몽고 디비에서 사용자 문서 완전 삭제

    response.delete_cookie(key="refresh_token") # 클라이언트 쿠키에서 refresh_token 제거

    return {"message": "User and all associated tokens have been deleted."}
