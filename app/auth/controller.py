from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.auth.schemas import UserCreate, Token, UserResponse
from app.auth.utils import get_password_hash, verify_password
from app.auth.token import create_access_token

# Authentication controller for handling user registration and login
# Provides endpoints for user signup and authentication

router = APIRouter(tags=["Authentication"])

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    User registration endpoint.

    Creates a new user account with the provided username, email, and password.
    Performs validation to ensure username and email are not already in use.

    Args:
        user: User creation data containing username, email, and password
        db: Database session dependency

    Returns:
        The newly created user object (without password)

    Raises:
        HTTPException: If username or email is already registered
    """
    # Check if username exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Check if email exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user with hashed password for security
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    User login endpoint.

    Authenticates a user with username and password, and issues a JWT access token.
    Uses OAuth2 password flow for authentication.

    Args:
        form_data: OAuth2 form containing username and password
        db: Database session dependency

    Returns:
        A token object containing the JWT access token and token type

    Raises:
        HTTPException: If authentication fails due to invalid credentials
    """
    # Find user by username
    user = db.query(User).filter(User.username == form_data.username).first()

    # Verify user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token with username as subject
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
