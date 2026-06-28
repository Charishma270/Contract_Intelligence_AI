import uuid

from backend.services.auth_service import create_user
from backend.services.tracking import init_db


def test_create_user_registers_with_hashing():
    init_db()

    email = f"signup-test-{uuid.uuid4().hex}@example.com"
    user = create_user(name="Test User", email=email, password="password123")

    assert user.email == email
    assert user.name == "Test User"
    assert user.hashed_password
    assert user.hashed_password != "password123"
