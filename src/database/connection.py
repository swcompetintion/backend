from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document
from src.core.config import settings
from src.models.plans import PlanModel
from src.schemas.plans import PlanUpdate


async def initialize_database():
    try:
        URL = ''
        client = AsyncIOMotorClient(URL)
        await init_beanie(
            database=client.get_default_database(),
            document_models=[PlanModel]
        )
        print("데이터베이스 연결 성공")
    except Exception as e:
        print(f"데이터베이스 연결 실패: {e}")


class Database:
    def __init__(self, model: Document):
        self.model = model

    async def save(self, document: Document) -> None:
        await document.create()
        return

    async def get_all(self) -> list:
        docs = await self.model.find_all().to_list()
        return docs

    async def delete(self, id: int):
        doc = await self.model.find_one(self.model.id == id)
        if doc:
            await doc.delete()

    async def get(self, id: int):
        doc = await self.model.find_one(self.model.id == id)
        return doc

    async def update(self, id: int, body: PlanUpdate):
        doc = await self.model.find_one(self.model.id == id)
        if doc:
            body_dict = body.model_dump(exclude_unset=True)
            update_data = {"$set": {k: v for k,
                                    v in body_dict.items() if v is not None}}
            await doc.update(update_data)
