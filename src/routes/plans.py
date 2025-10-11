from fastapi import APIRouter, Depends
from typing import List

from src.schemas.plans import Plan
from src.models.users import UserModel
from src.utils.security import get_current_user
from src.services.plan_service import PlanService
import logging

logger = logging.getLogger('dev')

plan_router = APIRouter(
    prefix="/plans",
    tags=["plans"]
)


@plan_router.get("/", response_model=List[Plan])
async def get_my_plans(current_user: UserModel = Depends(get_current_user)):

    return current_user.plans


@plan_router.post("/", response_model=List[Plan])
async def update_my_plans(
    plans: List[Plan],
    current_user: UserModel = Depends(get_current_user),
    plan_service: PlanService = Depends()
):
    updated_user = await plan_service.update_user_plans(user=current_user, plans=plans)
    return updated_user.plans
