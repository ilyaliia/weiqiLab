import uuid

from fastapi.testclient import TestClient
from main import app

PASSWORD = "Password123"


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
    return response


def test_profile_requires_auth():
    client = TestClient(app)
    response = client.get("/users/me")
    assert response.status_code == 401


def test_get_current_user_profile():
    client = TestClient(app)
    username = f"user_{uuid.uuid4().hex[:8]}"
    register_user(client, username)
    login_user(client, username)

    response = client.get("/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username
    assert data["email"] == f"{username}@example.com"


def test_get_public_user_profile():
    client = TestClient(app)
    username = f"user_{uuid.uuid4().hex[:8]}"
    register_user(client, username)

    response = client.get(f"/users/{username}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username
    assert data["email"] == f"{username}@example.com"
