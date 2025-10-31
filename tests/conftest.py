import pytest_asyncio # 비동기 테스트를 도와주는 pytest용 플러그인, 테스트에서 async def로 쓸 수 있게 해줌
from httpx import AsyncClient, ASGITransport 
# AsyncClient: HTTP 요청을 보내고 응답을 받는  클라이언트
# ASGITransport: AsynClient가 요청을 보낼 때 메모리 안에서 직접 호출하는 전달체(네트워크 계층 건너띄무로 속도 빠름)
from beanie import init_beanie
# DB 초기화 및 모델 연결(mongoDB용 ORM) 
from motor.motor_asyncio import AsyncIOMotorClient
# motor: MongoDB 공식 비동기 python 드라이버
# 몽고DB에 비동기로 연결하고 쿼리할 수 있게 해주는 라이브러리
import asyncio
# 파이썬의 비동기 엔진
import re
# 글자에서 패턴 찾기

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
    await UserModel.delete_all() # 테스트 후 모든 사용자 삭제
    await RefreshTokenModel.delete_all() # 모든 토큰 삭제
