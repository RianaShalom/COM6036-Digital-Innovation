import jwt

from app.core.security import create_access_token
from app.core.config import settings
from datetime import datetime, timedelta, timezone


def register_user(client, email: str, password: str = "TestPassword123!"):
    # Registers a test user through the public API.
    response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    return response


def login_user(client, email: str, password: str = "TestPassword123!"):
    # Authenticates a test user through the public API.
    return client.post(
        "/api/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )


def test_register_user_returns_created_user(client):
    response = register_user(client, "api-register@example.com")

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "api-register@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data
    assert "password_hash" not in data


def test_duplicate_registration_returns_conflict(client):
    register_user(client, "duplicate@example.com")

    response = register_user(client, "duplicate@example.com")

    assert response.status_code == 409
    assert response.json()["detail"] == "A user with this email already exists."


def test_login_returns_access_token(client):
    register_user(client, "api-login@example.com")

    response = login_user(client, "api-login@example.com")

    assert response.status_code == 200

    data = response.json()

    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


def test_login_rejects_incorrect_password(client):
    register_user(client, "wrong-password@example.com")

    response = login_user(
        client,
        "wrong-password@example.com",
        "IncorrectPassword123!",
    )

    assert response.status_code == 401


def test_login_rejects_unknown_user(client):
    response = login_user(client, "does-not-exist@example.com")

    assert response.status_code == 401


def test_protected_endpoint_rejects_missing_token(client):
    response = client.get("/api/tasks")

    assert response.status_code == 401


def test_protected_endpoint_rejects_invalid_token(client):
    response = client.get(
        "/api/tasks",
        headers={
            "Authorization": "Bearer this-is-not-a-valid-jwt",
        },
    )

    assert response.status_code == 401


def test_expired_token_is_rejected(client):
    register_user(client, "expired-token@example.com")

    # Creates an already-expired token to verify JWT validation.
    expired_token = jwt.encode(
        {
            "sub": "00000000-0000-0000-0000-000000000000",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        settings.secret_key,
        algorithm="HS256",
    )

    response = client.get(
        "/api/tasks",
        headers={
            "Authorization": f"Bearer {expired_token}",
        },
    )

    assert response.status_code == 401

def test_authenticated_user_can_create_task(client):
    register_user(client, "create-task@example.com")
    login_response = login_user(client, "create-task@example.com")

    token = login_response.json()["access_token"]

    response = client.post(
        "/api/tasks",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "API integration test",
            "description": "Created through the HTTP API",
            "module": "COM6036",
            "deadline": (
                datetime.now(timezone.utc) + timedelta(days=7)
            ).isoformat(),
            "estimated_hours": 3,
            "difficulty": 3,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "API integration test"
    assert data["status"] == "pending"


def test_authenticated_user_can_complete_task(client):
    register_user(client, "complete-api@example.com")
    login_response = login_user(client, "complete-api@example.com")

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/api/tasks",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Complete through API",
            "description": "Completion test",
            "module": "COM6036",
            "deadline": (
                datetime.now(timezone.utc) + timedelta(days=5)
            ).isoformat(),
            "estimated_hours": 2,
            "difficulty": 2,
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    complete_response = client.post(
        f"/api/tasks/{task_id}/complete",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert complete_response.status_code == 200

    data = complete_response.json()

    assert data["status"] == "completed"
    assert data["completed_at"] is not None


def test_user_cannot_access_another_users_task(client):
    register_user(client, "owner@example.com")
    owner_login = login_user(client, "owner@example.com")
    owner_token = owner_login.json()["access_token"]

    create_response = client.post(
        "/api/tasks",
        headers={
            "Authorization": f"Bearer {owner_token}",
        },
        json={
            "title": "Private task",
            "description": "Belongs to another user",
            "module": "COM6036",
            "deadline": (
                datetime.now(timezone.utc) + timedelta(days=5)
            ).isoformat(),
            "estimated_hours": 2,
            "difficulty": 2,
        },
    )

    task_id = create_response.json()["id"]

    register_user(client, "other-user@example.com")
    other_login = login_user(client, "other-user@example.com")
    other_token = other_login.json()["access_token"]

    response = client.get(
        f"/api/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {other_token}",
        },
    )

    assert response.status_code == 404