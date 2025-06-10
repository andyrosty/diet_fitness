from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.auth.token import verify_token

# Authentication dependencies for securing API endpoints
# These dependencies are used to protect routes that require authentication

# OAuth2 password bearer scheme that will extract and validate JWT tokens
# The tokenUrl parameter specifies the endpoint where clients can obtain tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependency to get the current authenticated user from a JWT token.

    This function is used as a dependency in protected routes to:
    1. Extract the JWT token from the Authorization header
    2. Verify the token's validity and extract the username
    3. Retrieve the corresponding user from the database

    Args:
        token: JWT token extracted from the Authorization header by oauth2_scheme
        db: Database session for querying the user

    Returns:
        User: The authenticated user object if token is valid

    Raises:
        HTTPException: If token is invalid or user doesn't exist
    """
    # Verify token and extract username
    username = verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Retrieve user from database
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
