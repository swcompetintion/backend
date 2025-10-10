
import pytest
from httpx import AsyncClient

from src.main import app
from src.models.users import UserModel
from src.schemas.plans import Plan
from src.utils.security import get_current_user


@pytest.fixture
def setup_dependency_override():
    initial_plans = [
        Plan(title="Initial Plan 1", content="Content 1"),
        Plan(title="Initial Plan 2", content="Content 2"),
    ]
    mock_user = UserModel(email="test@example.com", plans=initial_plans)

    async def override_get_current_user() -> UserModel:
        return mock_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    yield
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_plans(test_client: AsyncClient, setup_dependency_override):
    response = await test_client.get("/plans")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "Initial Plan 1"

@pytest.mark.asyncio
async def test_update_plans(test_client: AsyncClient, setup_dependency_override):
    new_plans_data = [
        {"title": "Updated Plan 1", "content": "New Content 1"},
        {"title": "Updated Plan 2", "content": "New Content 2"},
        {"title": "Updated Plan 3", "content": "New Content 3"},
    ]

    response = await test_client.put("/plans", json=new_plans_data)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 3
    assert response_data[0]["title"] == "Updated Plan 1"
    assert response_data[2]["title"] == "Updated Plan 3"

    get_response = await test_client.get("/plans")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 3
    assert get_response.json()[0]["title"] == "Updated Plan 1"
