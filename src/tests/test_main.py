import pytest
from fastapi.testclient import TestClient
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))


if "pytest" in sys.modules:
    from backend.main import app
    from backend.models.plans import PlanModel

    @pytest.fixture
    def clients():
        return TestClient(app)

    def test_get_plans(clients):
        with clients as client:
            response = client.get("/plans/")
            assert response.status_code == 200

    def test_create_plan(clients):
        with clients as client:

            plan_data = PlanModel(
                id=2,
                title="새로운 계획",
                description="테스트를 위한 계획입니다.",
                tags=["#새로운", "#계획"],
                location="테스트 장소",

            )

            response = client.post("/plans/", json=plan_data.model_dump())

            assert response.status_code == 200
            assert response.json() == {"message": "plan created successfully"}
