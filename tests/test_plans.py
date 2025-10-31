
import pytest
from httpx import AsyncClient

from src.main import app
from src.models.users import UserModel
from src.schemas.plans import Plan
from src.utils.security import get_current_user


@pytest.fixture
def setup_dependency_override(): # 가짜 사용자 생성 (실제 DB 없이)
    initial_plans = [
        Plan(title="Initial Plan 1", content="Content 1"),
        Plan(title="Initial Plan 2", content="Content 2"),
    ]
    mock_user = UserModel(email="test@example.com", plans=initial_plans)

    async def override_get_current_user() -> UserModel:
        return mock_user
    # FastAPI 의존성 오버라이드
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_plans(test_client: AsyncClient, setup_dependency_override):
    # 계획 조회 테스트
    response = await test_client.get("/plans")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "Initial Plan 1"

@pytest.mark.asyncio
async def test_update_plans(test_client: AsyncClient, setup_dependency_override):
    # 계획 업데이트 테스트
    new_plans_data = [
        {"title": "Updated Plan 1", "content": "New Content 1"},
        {"title": "Updated Plan 2", "content": "New Content 2"},
        {"title": "Updated Plan 3", "content": "New Content 3"},
    ] # 실제 api에서 받는 타입인 plan 객체로 변경해야 함

    response = await test_client.put("/plans", json=new_plans_data) # put 요청으로 계획 업데이트(실제 라우터에서 쓰는 걸로 post로 변경해야 함
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 3 # 업데이트 확인
    assert response_data[0]["title"] == "Updated Plan 1"
    assert response_data[2]["title"] == "Updated Plan 3"

    get_response = await test_client.get("/plans") # 다시 조회해서 변경 확인
    assert get_response.status_code == 200
    assert len(get_response.json()) == 3
    assert get_response.json()[0]["title"] == "Updated Plan 1"


# 에러 케이스 테스트 추가