"""
Authentication schemas module for the Diet Fitness application.

This module defines Pydantic models used for data validation and serialization
in the authentication system. These models handle user registration, login,
token responses, and user data representation.
"""
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """
    Schema for user registration requests.

    Contains the data required to create a new user account.
    """
    username: str  # Unique username for identification
    email: EmailStr  # Valid email address for the user
    password: str  # User's password (will be hashed before storage)

class UserLogin(BaseModel):
    """
    Schema for user login requests.

    Contains the credentials needed for authentication.
    """
    username: str  # Username for login
    password: str  # Password for verification

class Token(BaseModel):
    """
    Schema for authentication token responses.

    Returned after successful authentication.
    """
    access_token: str  # JWT token for API access
    token_type: str  # Token type (typically "bearer")

class UserResponse(BaseModel):
    """
    Schema for user data responses.

    Used when returning user information (excludes sensitive data like passwords).
    """
    id: int  # User's unique identifier
    username: str  # User's username
    email: EmailStr  # User's email address

    class Config:
        """Configuration for Pydantic model."""
        orm_mode = True  # Allows the model to read data from ORM objects
