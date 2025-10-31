from typing import List
from src.models.users import UserModel
from src.schemas.plans import Plan


class PlanService:
    async def update_user_plans(self, user: UserModel, plans: List[Plan]) -> UserModel:
        for i in range(len(plans)):
            plans[i].id = i # id를 순서대로 자동 할당
        user.plans = plans # 사용자의 계획을 통째로 교체
        await user.save() # MongoDB에 저장
        return user # 업데이트된 사용자 변환
    
# 추가하면 좋은 검증들
# 하루 총 시간이 24시간 초과하지 않는지
# 제목 중복 검사
# 최대 계획 개수 제한