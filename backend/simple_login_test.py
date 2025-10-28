#!/usr/bin/env python3
import requests
import json

# Test 1: admin login
print("Test 1: Admin Login")
response = requests.post(
    "http://localhost:8000/api/auth/email/login",
    json={"email": "admin@russian.town", "password": "admin123"}
)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("PASS - Admin login successful")
else:
    print(f"FAIL - {response.text}")

print()

# Test 2: user login
print("Test 2: User Login")
response = requests.post(
    "http://localhost:8000/api/auth/email/login",
    json={"email": "user1@test.com", "password": "user1234"}
)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("PASS - User login successful")
else:
    print(f"FAIL - {response.text}")
