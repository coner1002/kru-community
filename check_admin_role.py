"""Check admin user role and user_type"""
import requests

BASE_URL = "http://localhost:8000"

# Login
login_response = requests.post(
    f"{BASE_URL}/api/auth/email/login",
    json={"email": "admin@russian.town", "password": "admin123"}
)

if login_response.status_code != 200:
    print("Login failed!")
    exit(1)

token = login_response.json()['access_token']

# Get /me info
me_response = requests.get(
    f"{BASE_URL}/api/users/me",
    headers={"Authorization": f"Bearer {token}"}
)

print("=== /api/users/me Response ===")
print(f"Status: {me_response.status_code}")

if me_response.status_code == 200:
    user_data = me_response.json()
    print(f"Email: {user_data.get('email')}")
    print(f"Role: {user_data.get('role')}")
    print(f"User Type: {user_data.get('user_type')}")
    print(f"Is Admin: {user_data.get('is_active')}")
    print(f"\nFull data:")
    import json
    print(json.dumps(user_data, indent=2, ensure_ascii=False))
else:
    print(f"Error: {me_response.text}")
