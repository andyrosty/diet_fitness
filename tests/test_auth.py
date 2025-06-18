"""
Authentication endpoints test script.

This script tests the authentication flow of the Diet Fitness application by:
1. Creating a test user account (signup)
2. Authenticating the user to obtain a JWT token (login)
3. Testing a protected endpoint using the obtained token

This helps verify that the authentication system is working correctly
and that protected endpoints properly enforce authentication.
"""
import pytest
import json

# Test user data for registration
test_user_data = {
    "username": "testuser2",
    "email": "test2@example.com",
    "password": "password123"
}

# Test login data for authentication
login_data = {
    "username": "testuser",
    "password": "password123"
}

def test_signup(client):
    """Test user signup endpoint"""
    response = client.post("/auth/signup", json=test_user_data)
    assert response.status_code == 200
    assert response.json()["username"] == test_user_data["username"]
    assert response.json()["email"] == test_user_data["email"]

def test_login(client, test_user):
    """Test user login endpoint"""
    response = client.post(
        "/auth/login",
        data={"username": login_data["username"], "password": login_data["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_protected_endpoint(client, token):
    """Test a protected endpoint with the JWT token"""
    response = client.get(
        "/api/my-plans",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_delete_user(client, token):
    """Test user deletion endpoint"""
    response = client.delete(
        "/auth/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

    # Verify user is deleted by trying to access protected endpoint again
    verify_response = client.get(
        "/api/my-plans",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert verify_response.status_code == 401
