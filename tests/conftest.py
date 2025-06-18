import os
# Ensure test mode flag is set before importing the application (skip DB creation on import)
os.environ["TEST_MODE"] = "1"
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db
from app.db.models import User
from app.auth.utils import get_password_hash
from app.auth.token import create_access_token, SECRET_KEY, verify_token

# Ensure we're running in test mode
if os.environ.get("TEST_MODE") != "1" and not os.environ.get("PYTEST_CURRENT_TEST"):
    import warnings
    warnings.warn(
        "Tests are running without TEST_MODE=1 environment variable. "
        "This could potentially connect to production databases. "
        "Set TEST_MODE=1 to suppress this warning."
    )

# Test-specific configuration
TEST_JWT_SECRET_KEY = "test_secret_key_not_for_production"

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# PostgreSQL database configuration for integration tests
# This matches the configuration used in CI
PG_DATABASE_URL = os.environ.get(
    "PG_TEST_DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/test_db"
)

# Flag to determine if PostgreSQL tests should be run
# Only run if explicitly enabled or in CI environment
RUN_PG_TESTS = os.environ.get("RUN_PG_TESTS", "0") == "1" or os.environ.get("CI") == "true"

# Create PostgreSQL engine if tests are enabled
if RUN_PG_TESTS:
    try:
        pg_engine = create_engine(PG_DATABASE_URL)
        PgTestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pg_engine)
    except Exception as e:
        import warnings
        warnings.warn(f"PostgreSQL tests are enabled but connection failed: {e}")
        RUN_PG_TESTS = False

# Test user credentials
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}

@pytest.fixture(scope="function")
def db():
    """
    Create a fresh SQLite database for each test.
    """
    # Create the database tables
    Base.metadata.create_all(bind=engine)

    # Create a new session for the test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop the tables after the test is complete
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def pg_db():
    """
    Create a fresh PostgreSQL database for each test.
    This fixture is skipped if PostgreSQL tests are disabled.
    """
    if not RUN_PG_TESTS:
        pytest.skip("PostgreSQL tests are disabled")

    # Create the database tables
    Base.metadata.create_all(bind=pg_engine)

    # Create a new session for the test
    db = PgTestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop the tables after the test is complete
        Base.metadata.drop_all(bind=pg_engine)

@pytest.fixture(scope="function")
def client(db):
    """
    Create a test client using the test database.
    """
    # Override the get_db dependency to use our test database
    def override_get_db():
        try:
            yield db
        finally:
            pass

    # Override token verification to use test secret key
    from app.auth.token import verify_token

    # Store original function to restore later
    original_verify_token = verify_token

    # Patch the verify_token function in the auth module
    import app.auth.token as auth_token_module
    auth_token_module.verify_token = test_verify_token

    # Override the get_db dependency to use our test database
    app.dependency_overrides[get_db] = override_get_db

    # Create a test client in-process
    with TestClient(app) as client:
        yield client

    # Restore original verify_token function and clear overrides
    auth_token_module.verify_token = original_verify_token
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db):
    """
    Create a test user in the database.
    """
    # Create a user with a hashed password
    hashed_password = get_password_hash(TEST_USER["password"])
    user = User(
        username=TEST_USER["username"],
        email=TEST_USER["email"],
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Override token functions to use test secret key
def test_create_access_token(data: dict):
    """Test version of create_access_token that uses the test secret key"""
    from datetime import datetime, timedelta
    from jose import jwt
    from app.auth.token import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, TEST_JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def test_verify_token(token: str):
    """Test version of verify_token that uses the test secret key"""
    from jose import JWTError, jwt
    from app.auth.token import ALGORITHM

    try:
        payload = jwt.decode(token, TEST_JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

@pytest.fixture(scope="function")
def token(test_user):
    """
    Create a JWT token for the test user.
    """
    # Create an access token for the test user using the test secret key
    access_token = test_create_access_token(data={"sub": test_user.username})
    return access_token
