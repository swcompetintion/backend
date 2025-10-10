from fastapi import APIRouter, Depends, Response
from src.models.users import UserModel
from src.utils.security import get_current_user
from src.services.auth_service import AuthService

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@user_router.delete("/me")
async def delete_user_me(response: Response, current_user: UserModel = Depends(get_current_user), auth_service: AuthService = Depends()):

    await auth_service.delete_all_refresh_tokens_for_user(str(current_user.id))

    await current_user.delete()

    response.delete_cookie(key="refresh_token")

    return {"message": "User and all associated tokens have been deleted."}
