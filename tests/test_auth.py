"""
Authentication endpoints test script.

This script tests the authentication flow of the Diet Fitness application by:
1. Creating a test user account (signup)
2. Authenticating the user to obtain a JWT token (login)
3. Testing a protected endpoint using the obtained token

This helps verify that the authentication system is working correctly
and that protected endpoints properly enforce authentication.
"""
import requests
import json

# Base URL for the API
# Change this if testing against a different host or port
BASE_URL = "http://localhost:8000"

# Test user data for registration
# These credentials will be used to create a new user account
test_user = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}

# Test login data for authentication
# These credentials will be used to obtain a JWT token
login_data = {
    "username": "testuser",
    "password": "password123"
}

def test_signup():
    """Test user signup endpoint"""
    response = requests.post(f"{BASE_URL}/auth/signup", json=test_user)
    print("Signup Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200

def test_login():
    """Test user login endpoint"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": login_data["username"], "password": login_data["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print("Login Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    return response.json().get("access_token") if response.status_code == 200 else None

def test_protected_endpoint(token):
    """Test a protected endpoint with the JWT token"""
    if not token:
        print("No token available, skipping protected endpoint test")
        return False

    response = requests.get(
        f"{BASE_URL}/api/my-plans",
        headers={"Authorization": f"Bearer {token}"}
    )
    print("Protected Endpoint Response:", response.status_code)
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(response.text)
    return response.status_code == 200

if __name__ == "__main__":
    print("Testing user signup...")
    signup_success = test_signup()

    print("\nTesting user login...")
    token = test_login()

    print("\nTesting protected endpoint...")
    test_protected_endpoint(token)