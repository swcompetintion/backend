
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_google_api():
    google_user_info = {"email": "test@example.com", "sub": "12345"}
    id_token = "mock_id_token"
    # This mock is for the first httpx call inside the route (to Google's token endpoint)
    mock_token_resp = AsyncMock()
    mock_token_resp.status_code = 200
    # The .json() method of the response is an async method, so its return value is what we configure
    mock_token_resp.json.return_value = {"id_token": id_token}

    # This mock is for the second httpx call (to Google's tokeninfo endpoint)
    mock_verify_resp = AsyncMock()
    mock_verify_resp.status_code = 200
    mock_verify_resp.json.return_value = google_user_info
    return mock_token_resp, mock_verify_resp, google_user_info

@pytest.mark.asyncio
async def test_google_verify(test_client, mock_google_api):
    mock_token_resp, mock_verify_resp, _ = mock_google_api
    with (
        patch('src.routes.auths.httpx.AsyncClient.post', AsyncMock(return_value=mock_token_resp)),
        patch('src.routes.auths.httpx.AsyncClient.get', AsyncMock(return_value=mock_verify_resp)),
    ):
        response = await test_client.post("/auth/google-verify", json={"code": "mock_code"})
    
    assert response.status_code == 200
    json_response = await response.json()
    assert "access_token" in json_response
    assert "refresh_token" in response.cookies

@pytest.mark.asyncio
async def test_refresh_token(test_client, mock_google_api):
    mock_token_resp, mock_verify_resp, _ = mock_google_api
    with (
        patch('src.routes.auths.httpx.AsyncClient.post', AsyncMock(return_value=mock_token_resp)),
        patch('src.routes.auths.httpx.AsyncClient.get', AsyncMock(return_value=mock_verify_resp)),
    ):
        login_response = await test_client.post("/auth/google-verify", json={"code": "mock_code"})

    refresh_cookie = login_response.cookies.get("refresh_token")
    assert refresh_cookie is not None

    cookies = {"refresh_token": refresh_cookie}
    refresh_response = await test_client.post("/auth/refresh", cookies=cookies)
    
    assert refresh_response.status_code == 200
    assert "access_token" in await refresh_response.json()

@pytest.mark.asyncio
async def test_protected_route_and_logout(test_client, mock_google_api):
    mock_token_resp, mock_verify_resp, google_user_info = mock_google_api
    with (
        patch('src.routes.auths.httpx.AsyncClient.post', AsyncMock(return_value=mock_token_resp)),
        patch('src.routes.auths.httpx.AsyncClient.get', AsyncMock(return_value=mock_verify_resp)),
    ):
        login_response = await test_client.post("/auth/google-verify", json={"code": "mock_code"})
    
    access_token = (await login_response.json())["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    me_response = await test_client.get("/users/me", headers=headers)
    assert me_response.status_code == 200
    assert (await me_response.json())["email"] == google_user_info["email"]
    
    refresh_cookie = login_response.cookies.get("refresh_token")
    cookies = {"refresh_token": refresh_cookie}
    logout_response = await test_client.post("/auth/logout", cookies=cookies)
    assert logout_response.status_code == 200
    
    refresh_fail_response = await test_client.post("/auth/refresh", cookies=cookies)
    assert refresh_fail_response.status_code == 401

@pytest.mark.asyncio
async def test_delete_user(test_client, mock_google_api):
    mock_token_resp, mock_verify_resp, _ = mock_google_api
    with (
        patch('src.routes.auths.httpx.AsyncClient.post', AsyncMock(return_value=mock_token_resp)),
        patch('src.routes.auths.httpx.AsyncClient.get', AsyncMock(return_value=mock_verify_resp)),
    ):
        login_response = await test_client.post("/auth/google-verify", json={"code": "mock_code"})
    
    access_token = (await login_response.json())["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    delete_response = await test_client.delete("/users/me", headers=headers)
    assert delete_response.status_code == 200
    
    me_response_fail = await test_client.get("/users/me", headers=headers)
    assert me_response_fail.status_code == 401
