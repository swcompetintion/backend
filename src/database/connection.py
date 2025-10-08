import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document
from src.core.config import settings
from src.models.users import UserModel
from src.models.jwts import RefreshTokenModel


async def initialize_database():
    try:
        URL = os.getenv('DATABASE_URL')
        print(f"MongoDB 연결 시도: {URL}")
        print(f"감지된 환경: {settings.environment}")

        client = AsyncIOMotorClient(URL)

        await client.admin.command('ping')

        await init_beanie(
            database=client.get_default_database(),
            document_models=[UserModel, RefreshTokenModel]
        )
        print(f"데이터베이스 연결 성공 - Environment: {settings.environment}")
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

    async def update(self, id: str):
        from beanie import PydanticObjectId
        doc = await self.model.get(PydanticObjectId(id))
        if doc:
            body_dict = body.model_dump(exclude_unset=True)
            update_data = {"$set": {k: v for k,
                                    v in body_dict.items() if v is not None}}
            await doc.update(update_data)
        return doc
