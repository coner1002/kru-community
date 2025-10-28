"""Simple login test without Unicode issues"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_login():
    login_data = {
        "email": "admin@russian.town",
        "password": "admin1234"
    }

    print("Logging in...")
    print(f"Email: {login_data['email']}")

    response = requests.post(
        f"{BASE_URL}/api/auth/email/login",
        json=login_data
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        data = response.json()
        print("\nSUCCESS!")
        print(f"Token: {data.get('access_token', '')[:50]}...")
        return data.get('access_token')
    else:
        print("\nFailed. Trying other passwords...")
        for pwd in ["test1234", "password", "admin123", "12345678", "Test1234", "Admin1234"]:
            login_data["password"] = pwd
            response = requests.post(f"{BASE_URL}/api/auth/email/login", json=login_data)
            print(f"  {pwd}: {response.status_code}")
            if response.status_code == 200:
                print(f"  SUCCESS with password: {pwd}")
                return response.json().get('access_token')

if __name__ == "__main__":
    test_login()
