from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os

# JWT Token handling module
# Provides functions for creating and verifying JWT tokens used in authentication

# Configuration for JWT tokens
SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Secret key for signing tokens, loaded from environment
ALGORITHM = "HS256"                       # Hashing algorithm used for token signing
ACCESS_TOKEN_EXPIRE_MINUTES = 30          # Token validity period in minutes

# OAuth2 scheme for token extraction (duplicated from dependencies.py for potential standalone use)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict):
    """
    Create a new JWT access token.

    Generates a signed JWT token containing the provided data and an expiration timestamp.

    Args:
        data: Dictionary containing claims to include in the token (typically includes 'sub' for subject)

    Returns:
        str: Encoded JWT token string
    """
    # Create a copy of the data to avoid modifying the original
    to_encode = data.copy()

    # Calculate token expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add expiration claim to token data
    to_encode.update({"exp": expire})

    # Encode and sign the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """
    Verify a JWT token and extract the username.

    Decodes and validates the token signature and expiration time.

    Args:
        token: JWT token string to verify

    Returns:
        str: Username extracted from the token's 'sub' claim if valid
        None: If token is invalid or expired
    """
    try:
        # Decode and verify the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract username from the 'sub' (subject) claim
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        # Return None if token is invalid or expired
        return None
