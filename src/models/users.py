from beanie import Document
from pydantic import ConfigDict, EmailStr
from ..schemas.plans import Plan


class UserModel(Document):
    email: EmailStr # 구글 이메일 (고유 식별자), 이메일 형식 강제(데이터 무결성 보장)
    plans: list[Plan] = [] # 사용자의 계획들 ( 핵심 기능)

    model_config = ConfigDict(
        extra='allow', # 나중에 필드 추가 가능, 새로운 필드를 런타임에 추가 가능, 빠른 기능 확장 지원, user.new_field = "some_value"  이렇게 추가해도 에러 안남
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "google_123456789",
                "email": "user@example.com",
                "plans": ["68e4b374fe8048d7bf5336bb"]
            }
        }
    )

    class Settings:
        name = "user"
        indexes = ["email"] # 이메일로 빠른 검색

"""
성능향상 방법:
1. 별도 컬렉션 방식으로 변경 plans: list[str] =[] # Plan ID들만 저장
2. class PlanModel(Document): user_id: str title: str ...
대량 계획 처리 시 성능 향상, 복잡한 쿼리 가능
"""