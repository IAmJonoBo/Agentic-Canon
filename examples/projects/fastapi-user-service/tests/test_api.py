"""Test FastAPI application endpoints."""

import pytest
from acme_service.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """Create a test client."""
    return TestClient(app)


def test_root_endpoint(client: TestClient) -> None:
    """Test root endpoint returns health status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "FastAPI User Service"
    assert "timestamp" in data


def test_health_endpoint(client: TestClient) -> None:
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_ready_endpoint(client: TestClient) -> None:
    """Test readiness check endpoint."""
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_create_user(client: TestClient) -> None:
    """Test creating a new user."""
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "securepassword123",
        "role": "user",
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data
    assert "hashed_password" not in data


def test_create_duplicate_user(client: TestClient) -> None:
    """Test creating a user with duplicate email fails."""
    user_data = {
        "email": "duplicate@example.com",
        "full_name": "Test User",
        "password": "securepassword123",
    }
    # Create first user
    response1 = client.post("/users", json=user_data)
    assert response1.status_code == 201

    # Try to create duplicate
    response2 = client.post("/users", json=user_data)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]


def test_list_users(client: TestClient) -> None:
    """Test listing all users."""
    # Create a user first
    user_data = {
        "email": "listtest@example.com",
        "full_name": "List Test User",
        "password": "securepassword123",
    }
    client.post("/users", json=user_data)

    # List users
    response = client.get("/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0


def test_get_user(client: TestClient) -> None:
    """Test getting a user by ID."""
    # Create a user first
    user_data = {
        "email": "gettest@example.com",
        "full_name": "Get Test User",
        "password": "securepassword123",
    }
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]

    # Get the user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == user_data["email"]


def test_get_nonexistent_user(client: TestClient) -> None:
    """Test getting a non-existent user returns 404."""
    response = client.get("/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_update_user(client: TestClient) -> None:
    """Test updating a user."""
    # Create a user first
    user_data = {
        "email": "updatetest@example.com",
        "full_name": "Update Test User",
        "password": "securepassword123",
    }
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]

    # Update the user
    update_data = {"full_name": "Updated Name"}
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == update_data["full_name"]
    assert data["email"] == user_data["email"]  # Email unchanged


def test_delete_user(client: TestClient) -> None:
    """Test deleting a user."""
    # Create a user first
    user_data = {
        "email": "deletetest@example.com",
        "full_name": "Delete Test User",
        "password": "securepassword123",
    }
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]

    # Delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # Verify user is deleted
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
