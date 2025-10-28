#!/usr/bin/env python3
"""
로그인 API 테스트 스크립트
"""
import requests
import json

# 테스트 계정
test_users = [
    {"email": "user1@test.com", "password": "user1234"},
    {"email": "admin@russian.town", "password": "admin123"},
]

API_URL = "http://localhost:8000/api/auth/email/login"

print("=== 로그인 API 테스트 ===\n")

for user in test_users:
    print(f"테스트 계정: {user['email']}")

    try:
        response = requests.post(
            API_URL,
            json=user,
            headers={"Content-Type": "application/json"}
        )

        print(f"상태 코드: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ 로그인 성공!")
            print(f"토큰: {data.get('access_token', '')[:50]}...")
        else:
            print(f"❌ 로그인 실패")
            print(f"응답: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ 백엔드 서버에 연결할 수 없습니다 (http://localhost:8000)")
    except Exception as e:
        print(f"❌ 오류: {e}")

    print()
