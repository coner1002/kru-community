"""Test admin API endpoints"""
import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Login
login_response = requests.post(
    f"{BASE_URL}/api/auth/email/login",
    json={"email": "admin@russian.town", "password": "admin123"}
)

if login_response.status_code != 200:
    print("Login failed!")
    print(login_response.text)
    exit(1)

token = login_response.json()['access_token']
print(f"Token obtained: {token[:50]}...")

# 2. Test users endpoint
print("\n=== Testing /api/admin/users ===")
users_response = requests.get(
    f"{BASE_URL}/api/admin/users?limit=10",
    headers={"Authorization": f"Bearer {token}"}
)

print(f"Status: {users_response.status_code}")
if users_response.status_code == 200:
    users = users_response.json()
    print(f"Total users returned: {len(users)}")
    if len(users) > 0:
        print(f"First user: {users[0].get('email')} - {users[0].get('nickname_ko')}")
else:
    print(f"Error: {users_response.text}")
