from fastapi import APIRouter, HTTPException
from src.schemas.plans import PlanUpdate, PlanCreate, PlanResponse
from src.database.connection import Database
from src.models.users import UserModel
from src.utils.logger import logger
from datetime import datetime

plan_router = APIRouter(
    prefix="/plans",
    tags=["plans"]
)
plan_db = Database(UserModel)


@plan_router.get("/", response_model=list[PlanResponse])
async def get_all_plans():
    logger.info("Fetching all plans")
    plans = await plan_db.get_all()
    return [
        PlanResponse(
            id=str(plan.id),
            plan_id=plan.plan_id,
            title=plan.title,
            content=plan.content,
            important=plan.important,
            date=plan.date,
            created_at=plan.created_at
        )
        for plan in plans
    ]


@plan_router.get("/{id}", response_model=PlanResponse)
async def get_plan(id: str):
    try:
        plan = await plan_db.get(id)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        return PlanResponse(
            id=str(plan.id),
            plan_id=plan.plan_id,
            title=plan.title,
            content=plan.content,
            important=plan.important,
            date=plan.date,
            created_at=plan.created_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid ID format: {str(e)}")


@plan_router.post("/")
async def create_plan(plan: PlanCreate):
    plan_data = plan.model_dump()

    if not plan_data.get('created_at'):
        plan_data['created_at'] = datetime.now().isoformat()

    plan_model = PlanModel(**plan_data)
    await plan_db.save(plan_model)
    return {"message": "plan created successfully"}


@plan_router.delete("/{id}")
async def delete_plan(id: str):
    try:
        await plan_db.delete(id)
        return {"message": "plan deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid ID format: {str(e)}")


@plan_router.put("/{id}")
async def update_plan(id: str, plan: PlanUpdate):
    try:
        await plan_db.update(id, plan)
        return {"message": "plan updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid ID format: {str(e)}")
