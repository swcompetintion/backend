from typing import List
from src.models.users import UserModel
from src.schemas.plans import Plan


class PlanService:
    async def update_user_plans(self, user: UserModel, plans: List[Plan]) -> UserModel:
        for i in range(len(plans)):
            plans[i].id = i
        user.plans = plans
        await user.save()
        return user
