from fastapi import APIRouter, HTTPException
from src.schemas.plans import Plan
from src.database.connection import Database
from src.models.users import UserModel
from src.utils.logger import logger
from typing import List

plan_router = APIRouter(
    prefix="/plans",
    tags=["plans"]
)
user_db = Database(UserModel)


@plan_router.get("/{user_id}", response_model=List[Plan])
async def get_user_plans(user_id: str):
    logger.info(f"Fetching plans for user {user_id}")
    try:
        user = await user_db.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user["plans"]
    except Exception as e:
        logger.error(f"Error fetching plans for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Failed to fetch user plans")


@plan_router.put("/{user_id}")
async def update_user_plans(user_id: str, plans: List[Plan]):
    logger.info(f"Updating plans for user {user_id}")
    try:
        user = await user_db.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        plans_data = [plan.model_dump() for plan in plans]
        await user_db.update(user_id, {"plans": plans_data})

        return {"message": "Plans updated successfully"}
    except Exception as e:
        logger.error(f"Error updating plans for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update plans")
