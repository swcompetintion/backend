from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document, PydanticObjectId
from src.core.config import settings
from src.models.plans import PlanModel
from src.models.users import UserModel
from src.models.jwts import JwtModel
from src.schemas.plans import PlanUpdate


async def initialize_database():
    try:
        if not settings.DATABASE_URL:
            raise ValueError("DATABASE_URL이 설정되지 않았습니다")
        
        print(f"데이터베이스 연결 시도: {settings.DATABASE_URL}")
        client = AsyncIOMotorClient(settings.DATABASE_URL)
        await init_beanie(
            database=client.get_default_database(),
            document_models=[PlanModel, UserModel, JwtModel]
        )
        print("데이터베이스 연결 성공")
    except Exception as e:
        print(f"데이터베이스 연결 실패: {e}")
        raise


class Database:
    def __init__(self, model: Document):
        self.model = model

    async def save(self, document: Document) -> None:
        await document.create()
        return

    async def get_all(self) -> list:
        docs = await self.model.find_all().to_list()
        return docs

    async def delete(self, id: str):
        from beanie import PydanticObjectId
        doc = await self.model.get(PydanticObjectId(id))
        if doc:
            await doc.delete()

    async def get(self, id: str):
        from beanie import PydanticObjectId
        doc = await self.model.get(PydanticObjectId(id))
        return doc

    async def update(self, id: str, body: PlanUpdate):
        from beanie import PydanticObjectId
        doc = await self.model.get(PydanticObjectId(id))
        if doc:
            body_dict = body.model_dump(exclude_unset=True)
            update_data = {"$set": {k: v for k, v in body_dict.items() if v is not None}}
            await doc.update(update_data)
