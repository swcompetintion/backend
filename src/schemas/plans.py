from decimal import Decimal
from typing import Annotated
from datetime import datetime
from pydantic.types import condecimal
from pydantic import BaseModel, Field, ConfigDict

Decimal_range = Annotated[
    Decimal,
    condecimal(ge=0, le=30, max_digits=3, decimal_places=1)
]


class Plan(BaseModel):
    title: str
    content: str | None = None
    important: Decimal_range = Decimal("0.0")
    duration: Decimal_range = Decimal("0.0")
    created_at: datetime = Field(default_factory=datetime.now())
    model_config = ConfigDict(extra="forbid")
