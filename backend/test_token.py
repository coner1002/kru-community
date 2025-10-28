"""토큰 생성 및 검증 테스트"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.core.security import create_access_token, verify_token
from app.core.config import settings
from jose import jwt

# 테스트 토큰 생성
print("=== 토큰 생성 테스트 ===")
print(f"SECRET_KEY: {settings.SECRET_KEY[:30]}...")
print(f"ALGORITHM: {settings.ALGORITHM}\n")

# 토큰 생성
token_data = {"sub": "1", "jti": "test123"}
token = create_access_token(token_data)

print(f"생성된 토큰 (앞 80자): {token[:80]}...")
print(f"전체 길이: {len(token)}\n")

# 토큰 검증
try:
    payload = verify_token(token, "access")
    print("✅ 토큰 검증 성공!")
    print(f"Payload: {payload}\n")
except Exception as e:
    print(f"❌ 토큰 검증 실패: {e}\n")

# 직접 디코드 테스트
try:
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print("✅ 직접 디코드 성공!")
    print(f"Decoded: {decoded}\n")
except Exception as e:
    print(f"❌ 직접 디코드 실패: {e}\n")

# 잘못된 SECRET_KEY로 테스트
print("=== 잘못된 SECRET_KEY 테스트 ===")
wrong_key = "wrong-secret-key"
try:
    jwt.decode(token, wrong_key, algorithms=[settings.ALGORITHM])
    print("⚠️  잘못된 키로 디코드됨 (이상함)")
except Exception as e:
    print(f"✅ 예상대로 실패: {e}")
