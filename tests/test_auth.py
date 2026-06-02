import uuid

import pytest
from fastapi.testclient import TestClient
from main import app

PASSWORD = "Password123"

@pytest.fixture
def client():
    return TestClient(app)


def register_user(client: TestClient, username: str):
    response = client.post(
        "/register",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": PASSWORD,
            "password_confirm": PASSWORD,
        },
    )
    assert response.status_code == 200
    return response.json()


def login_user(client: TestClient, username: str):
    response = client.post(
        "/login",
        json={"username": username, "password": PASSWORD},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response


def test_register_and_login_sets_tokens(client: TestClient):
    username = f"user_{uuid.uuid4().hex[:8]}"
    register_user(client, username)

    login_response = login_user(client, username)
    assert login_response.cookies.get("my_access_token") is not None
    assert login_response.cookies.get("my_refresh_token") is not None


def test_refresh_and_logout_flow(client: TestClient):
    username = f"user_{uuid.uuid4().hex[:8]}"
    register_user(client, username)
    login_user(client, username)

    refresh_response = client.post("/refresh")
    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()
    assert client.cookies.get("my_access_token") is not None
    assert client.cookies.get("my_refresh_token") is not None

    logout_response = client.post("/logout")
    assert logout_response.status_code == 200
    assert client.cookies.get("my_access_token") is None
    assert client.cookies.get("my_refresh_token") is None