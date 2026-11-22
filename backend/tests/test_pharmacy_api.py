import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base
from app.api.dependencies import get_db


# Create an isolated in-memory SQLite database
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


@pytest.fixture
def client():

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

    Base.metadata.drop_all(bind=test_engine)


# TEST 1: Successful pharmacy registration
def test_register_pharmacy_success(client):

    response = client.post(
        "/api/v1/pharmacies/",
        json={
            "name": "Test Pharmacy",
            "licensing_authority": "Test Authority",
            "registration_number": "TEST-001",
            "contact_email": "test@example.com",
            "contact_phone": "9876543210"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Pharmacy"
    assert data["registration_number"] == "TEST-001"
    assert data["is_active"] is True
    assert data["id"] is not None


# TEST 2: Invalid email
def test_invalid_email_returns_422(client):

    response = client.post(
        "/api/v1/pharmacies/",
        json={
            "name": "Test Pharmacy",
            "licensing_authority": "Test Authority",
            "registration_number": "TEST-002",
            "contact_email": "invalid-email",
            "contact_phone": "9876543210"
        }
    )

    assert response.status_code == 422


# TEST 3: Duplicate pharmacy registration
def test_duplicate_pharmacy_returns_409(client):

    pharmacy_data = {
        "name": "Test Pharmacy",
        "licensing_authority": "Test Authority",
        "registration_number": "TEST-003",
        "contact_email": "test@example.com",
        "contact_phone": "9876543210"
    }

    first_response = client.post(
        "/api/v1/pharmacies/",
        json=pharmacy_data
    )

    second_response = client.post(
        "/api/v1/pharmacies/",
        json=pharmacy_data
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


# TEST 4: Retrieve an existing pharmacy
def test_get_pharmacy_success(client):

    create_response = client.post(
        "/api/v1/pharmacies/",
        json={
            "name": "Apollo Pharmacy",
            "licensing_authority": "Test Authority",
            "registration_number": "GET-001",
            "contact_email": "apollo@example.com",
            "contact_phone": "9876543210"
        }
    )

    pharmacy_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/pharmacies/{pharmacy_id}"
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Apollo Pharmacy"


# TEST 5: Retrieve nonexistent pharmacy
def test_get_nonexistent_pharmacy(client):

    response = client.get("/api/v1/pharmacies/99999")

    assert response.status_code == 404


# TEST 6: Pagination
def test_get_all_pharmacies_with_pagination(client):

    for i in range(3):

        client.post(
            "/api/v1/pharmacies/",
            json={
                "name": f"Test Pharmacy {i}",
                "licensing_authority": "Test Authority",
                "registration_number": f"PAGE-{i}",
                "contact_email": f"test{i}@example.com",
                "contact_phone": "9876543210"
            }
        )

    response = client.get(
        "/api/v1/pharmacies/?limit=2&offset=1"
    )

    assert response.status_code == 200
    assert len(response.json()) == 2