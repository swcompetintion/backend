import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import re

from src.main import app
from src.core.config import settings
from src.models.users import UserModel
from src.models.jwts import RefreshTokenModel

# Use the DATABASE_URL from settings and replace the db name with test_db
if settings.DATABASE_URL:
    test_db_url = re.sub(r"/(app|[^/]+)\?", "/test_db?", settings.DATABASE_URL, 1)
else:
    test_db_url = "mongodb://root:password@mongodb_container:27017/test_db?authSource=admin"

@pytest_asyncio.fixture(scope="function")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def test_client():
    client = AsyncIOMotorClient(test_db_url)
    await init_beanie(
        database=client.get_database(),
        document_models=[UserModel, RefreshTokenModel]
    )
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    await client.aclose()

@pytest_asyncio.fixture(autouse=True)
async def cleanup_database():
    yield
    await UserModel.delete_all()
    await RefreshTokenModel.delete_all()
