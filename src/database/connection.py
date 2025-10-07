import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document, PydanticObjectId
from src.core.config import settings
from src.models.plans import PlanModel
from src.models.users import UserModel
from src.models.jwts import JwtModel
from src.schemas.plans import PlanUpdate


def get_mongodb_url():
    """환경에 따라 MongoDB URL을 반환"""
    # 기존 DATABASE_URL이 있으면 사용
    if settings.DATABASE_URL:
        return settings.DATABASE_URL
    
    # 환경 설정에 따른 기본 URL
    environment = settings.environment.lower()
    
    if environment == 'production' or environment == 'ec2':
        return os.getenv('DATABASE_URL_PRODUCTION', 'mongodb://localhost:27017/bedrock_prod')
    elif environment == 'development' or environment == 'dev':
        return os.getenv('DATABASE_URL_DEV', 'mongodb://localhost:27017/bedrock_dev')
    elif environment == 'docker':
        return 'mongodb://mongodb_container:27017/bedrock'
    else:  # local
        return os.getenv('DATABASE_URL_LOCAL', 'mongodb://localhost:27017/bedrock')


async def initialize_database():
    try:
        URL = get_mongodb_url()
        print(f"MongoDB 연결 시도: {URL}")
        print(f"감지된 환경: {settings.environment}")
        
        client = AsyncIOMotorClient(URL)
        
        # 연결 테스트
        await client.admin.command('ping')
        
        await init_beanie(
            database=client.get_default_database(),
            document_models=[PlanModel, UserModel, JwtModel]
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

    async def update(self, id: str, body: PlanUpdate):
        from beanie import PydanticObjectId
        doc = await self.model.get(PydanticObjectId(id))
        if doc:
            body_dict = body.model_dump(exclude_unset=True)
            update_data = {"$set": {k: v for k, v in body_dict.items() if v is not None}}
            await doc.update(update_data)
        return doc
