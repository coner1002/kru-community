"""Check admin login and test dashboard access"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_admin_login():
    # Test with admin123 password (which worked earlier)
    login_data = {
        "email": "admin@russian.town",
        "password": "admin123"
    }

    print("=== Testing Admin Login ===")
    print(f"Email: {login_data['email']}")
    print(f"Password: {login_data['password']}")

    response = requests.post(
        f"{BASE_URL}/api/auth/email/login",
        json=login_data
    )

    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print("\nLOGIN SUCCESS!")
        print(f"Token (first 50 chars): {data.get('access_token', '')[:50]}...")
        print(f"User role: {data.get('user', {}).get('role')}")
        print(f"User email: {data.get('user', {}).get('email')}")

        # Test dashboard access
        print("\n=== Testing Dashboard Access ===")
        token = data.get('access_token')

        dashboard_response = requests.get(
            f"{BASE_URL}/api/admin/dashboard",
            headers={"Authorization": f"Bearer {token}"}
        )

        print(f"Dashboard Status: {dashboard_response.status_code}")

        if dashboard_response.status_code == 200:
            dashboard_data = dashboard_response.json()
            print("\nDASHBOARD ACCESS SUCCESS!")
            print(json.dumps(dashboard_data, indent=2, ensure_ascii=False))
        else:
            print(f"Dashboard access failed: {dashboard_response.text}")

        return True
    else:
        print(f"\nLOGIN FAILED: {response.text}")
        return False

if __name__ == "__main__":
    test_admin_login()
