"""테스트 로그인 스크립트"""
import requests
import json

# 백엔드 URL
BASE_URL = "http://localhost:8000"

# 관리자 계정으로 로그인 시도
def test_login():
    login_data = {
        "email": "admin@russian.town",
        "password": "admin1234"  # 일반적인 테스트 비밀번호
    }

    print("로그인 시도 중...")
    print(f"이메일: {login_data['email']}")

    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/email/login",
            json=login_data
        )

        print(f"\n상태 코드: {response.status_code}")
        print(f"응답 헤더: {dict(response.headers)}")

        if response.status_code == 200:
            data = response.json()
            print("\n✅ 로그인 성공!")
            print(f"Access Token (앞 50자): {data.get('access_token', '')[:50]}...")
            print(f"User Role: {data.get('user', {}).get('role')}")
            print(f"User Email: {data.get('user', {}).get('email')}")

            # 토큰으로 대시보드 접근 테스트
            test_dashboard(data.get('access_token'))
        else:
            print(f"\n❌ 로그인 실패")
            print(f"응답: {response.text}")

            # 다른 비밀번호로 시도
            print("\n다른 비밀번호로 시도 중...")
            for pwd in ["test1234", "password", "admin123", "12345678"]:
                login_data["password"] = pwd
                response = requests.post(f"{BASE_URL}/api/auth/email/login", json=login_data)
                if response.status_code == 200:
                    print(f"✅ 비밀번호 '{pwd}'로 로그인 성공!")
                    data = response.json()
                    test_dashboard(data.get('access_token'))
                    return

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def test_dashboard(token):
    """대시보드 접근 테스트"""
    print("\n대시보드 접근 테스트 중...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/admin/dashboard",
            headers={"Authorization": f"Bearer {token}"}
        )

        print(f"상태 코드: {response.status_code}")

        if response.status_code == 200:
            print("✅ 대시보드 접근 성공!")
            data = response.json()
            print(f"데이터: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 대시보드 접근 실패")
            print(f"응답: {response.text}")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    test_login()
