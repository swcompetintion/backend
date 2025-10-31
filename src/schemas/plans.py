from decimal import Decimal
from typing import Annotated
from datetime import datetime
from pydantic.types import condecimal
from pydantic import BaseModel, Field, ConfigDict, field_validator
from bson import Decimal128

Decimal_range = Annotated[
    Decimal,
    condecimal(ge=0, le=30, max_digits=3, decimal_places=1)
] # 0.0 ~ 30.0
 

class Plan(BaseModel):
    id: int | None = None # 계획 ID
    title: str # 계획 제목 (필수)
    content: str | None = None # 상세 설명 (선택)
    important: Decimal_range = Decimal("0.0") # 중요도 (0.0~30.0)
    duration: Decimal_range = Decimal("0.0") # 소요 시간 (0.0~30.0), 하루 일정을 시간 단위로 계획 가능
    created_at: datetime = Field(default_factory=datetime.now) # 생성 시간
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    @field_validator('important', 'duration', mode='before')
    @classmethod
    def validate_decimal128(cls, v):
        if isinstance(v, Decimal128): # MongoDB의 Decimal 타입 변환
            return v.to_decimal()
        return v
