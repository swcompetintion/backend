
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_google_api():
    google_user_info = {"email": "test@example.com", "sub": "12345"} # 두 개의 HTTP 호출을 모킹, token 교환, 검증
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
    """
    google OAuth -> Jwt 발급 -> 토큰 형태 확인
    """
    mock_token_resp, mock_verify_resp, _ = mock_google_api
    with (
        patch('src.routes.auths.httpx.AsyncClient.post', AsyncMock(return_value=mock_token_resp)),
        patch('src.routes.auths.httpx.AsyncClient.get', AsyncMock(return_value=mock_verify_resp)),
    ):
        response = await test_client.post("/auth/google-verify", json={"code": "mock_code"})
    
    assert response.status_code == 200
    json_response = await response.json()
    assert "access_token" in json_response # JSON에 Access Token
    assert "refresh_token" in response.cookies # 쿠키에 Refresh Token

@pytest.mark.asyncio
async def test_refresh_token(test_client, mock_google_api):
    """
    refresh_token 쿠키로 새 access_token 받기
    """
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
    """
    보호된 라우트 접근 + 로그아웃 후 토큰 무효화
    """
    mock_token_resp, mock_verify_resp, google_user_info = mock_google_api
    with (
        patch('src.routes.auths.httpx.AsyncClient.post', AsyncMock(return_value=mock_token_resp)),
        patch('src.routes.auths.httpx.AsyncClient.get', AsyncMock(return_value=mock_verify_resp)),
    ):
        login_response = await test_client.post("/auth/google-verify", json={"code": "mock_code"})
    
    # 로그인
    access_token = (await login_response.json())["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 보호된 api 호출
    me_response = await test_client.get("/users/me", headers=headers)
    assert me_response.status_code == 200
    assert (await me_response.json())["email"] == google_user_info["email"]
    
    refresh_cookie = login_response.cookies.get("refresh_token")
    cookies = {"refresh_token": refresh_cookie}
    # 로그아웃
    logout_response = await test_client.post("/auth/logout", cookies=cookies)
    assert logout_response.status_code == 200
    # 로그아웃 후 refresh 토큰으로 갱신 시도 (실패해야 함)
    refresh_fail_response = await test_client.post("/auth/refresh", cookies=cookies)
    assert refresh_fail_response.status_code == 401

@pytest.mark.asyncio
async def test_delete_user(test_client, mock_google_api):
    """
    로그인 -> 회원탈퇴 -> 토큰으로 접근 시도 (실패해야 함)
    """
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
