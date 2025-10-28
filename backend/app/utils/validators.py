import re
from typing import Optional

def validate_email(email: str) -> bool:
    """이메일 유효성 검사"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    """비밀번호 유효성 검사"""
    if len(password) < 8:
        return False

    # 대소문자, 숫자 포함 여부 확인
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    return has_upper and has_lower and has_digit

def validate_username(username: str) -> bool:
    """사용자명 유효성 검사"""
    if not username or len(username) < 3 or len(username) > 30:
        return False

    # 영문, 숫자, 언더스코어만 허용
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, username) is not None

def validate_nickname(nickname: str) -> bool:
    """닉네임 유효성 검사"""
    if not nickname or len(nickname) < 2 or len(nickname) > 50:
        return False

    # 특수문자 제한 (기본적인 문자와 공백만 허용)
    pattern = r'^[a-zA-Z0-9가-힣а-яё\s]+$'
    return re.match(pattern, nickname) is not None