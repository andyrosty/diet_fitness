"""
Password utility module for the Diet Fitness application.

This module provides functions for securely hashing and verifying passwords
using the bcrypt hashing algorithm. These utilities are used in the authentication
system to protect user credentials.
"""
from passlib.context import CryptContext

# Create a password context using bcrypt for secure password hashing
# bcrypt is a password-hashing function designed to be slow and resist brute-force attacks
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    Verify a password against its hash.

    Args:
        plain_password (str): The plaintext password to verify
        hashed_password (str): The hashed password to compare against

    Returns:
        bool: True if the password matches the hash, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Generate a secure hash for a password.

    Args:
        password (str): The plaintext password to hash

    Returns:
        str: The securely hashed password
    """
    return pwd_context.hash(password)
