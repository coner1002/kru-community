from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import httpx
import secrets

from app.db.database import get_db
from app.core.security import (
    create_access_token, create_refresh_token,
    verify_password, get_password_hash,
    verify_token, generate_verification_token,
    generate_jti
)
from app.core.config import settings
from app.models import User, Session as UserSession, EmailVerification, OAuthProvider
from app.schemas.auth import (
    UserRegister, UserLogin, TokenResponse,
    PasswordReset, PasswordResetRequest, OAuthCallback
)
from app.services.email import send_verification_email, send_password_reset_email
from app.utils.validators import validate_email, validate_password
from app.utils.transliteration import transliterate_nickname

router = APIRouter()

@router.post("/email/register", response_model=TokenResponse)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    # 이메일 중복 확인
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다"
        )

    # 사용자명 중복 확인
    if user_data.username and db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 사용자명입니다"
        )

    # 비밀번호 검증
    if not validate_password(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비밀번호는 8자 이상이어야 하며, 대소문자와 숫자를 포함해야 합니다"
        )

    # 닉네임 음역
    nickname_ko, nickname_ru = transliterate_nickname(user_data.nickname)

    # 사용자 생성
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        username=user_data.username,
        nickname=user_data.nickname,
        nickname_ko=nickname_ko,
        nickname_ru=nickname_ru,
        password_hash=hashed_password,
        preferred_lang=user_data.preferred_lang,
        oauth_provider=OAuthProvider.EMAIL,
        user_type='REAL'  # 실제 가입회원으로 설정
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # 이메일 인증 토큰 생성
    verification = EmailVerification(
        user_id=user.id,
        email=user.email,
        token=generate_verification_token(),
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    db.add(verification)
    db.commit()

    # 인증 이메일 발송
    await send_verification_email(user.email, verification.token)

    # 토큰 생성
    access_jti = generate_jti()
    refresh_jti = generate_jti()
    access_token = create_access_token({"sub": str(user.id), "jti": access_jti})
    refresh_token = create_refresh_token({"sub": str(user.id), "jti": refresh_jti})

    # 세션 저장
    session = UserSession(
        user_id=user.id,
        access_token_jti=access_jti,
        refresh_token_jti=refresh_jti,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(session)
    db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/email/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    # 사용자 조회
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비활성화된 계정입니다"
        )

    # 로그인 시간 업데이트
    user.last_login_at = datetime.utcnow()
    db.commit()

    # 토큰 생성
    access_jti = generate_jti()
    refresh_jti = generate_jti()
    access_token = create_access_token({"sub": str(user.id), "jti": access_jti})
    refresh_token = create_refresh_token({"sub": str(user.id), "jti": refresh_jti})

    # 세션 저장
    session = UserSession(
        user_id=user.id,
        access_token_jti=access_jti,
        refresh_token_jti=refresh_jti,
        user_agent=request.headers.get("User-Agent"),
        ip_address=request.client.host,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(session)
    db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.get("/oauth/{provider}")
async def oauth_login(provider: str):
    """소셜 로그인 URL 리다이렉트"""
    if provider == "google":
        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={settings.GOOGLE_CLIENT_ID}&"
            f"response_type=code&"
            f"scope=openid%20email%20profile&"
            f"redirect_uri={settings.CORS_ORIGINS[0]}/api/auth/oauth/google/callback"
        )
    elif provider == "kakao":
        auth_url = (
            f"https://kauth.kakao.com/oauth/authorize?"
            f"client_id={settings.KAKAO_CLIENT_ID}&"
            f"redirect_uri={settings.CORS_ORIGINS[0]}/api/auth/oauth/kakao/callback&"
            f"response_type=code"
        )
    elif provider == "naver":
        auth_url = (
            f"https://nid.naver.com/oauth2.0/authorize?"
            f"response_type=code&"
            f"client_id={settings.NAVER_CLIENT_ID}&"
            f"redirect_uri={settings.CORS_ORIGINS[0]}/api/auth/oauth/naver/callback&"
            f"state={secrets.token_urlsafe(16)}"
        )
    elif provider == "facebook":
        auth_url = (
            f"https://www.facebook.com/v18.0/dialog/oauth?"
            f"client_id={settings.FACEBOOK_APP_ID}&"
            f"redirect_uri={settings.CORS_ORIGINS[0]}/api/auth/oauth/facebook/callback&"
            f"scope=email&"
            f"response_type=code"
        )
    elif provider == "vk":
        auth_url = (
            f"https://oauth.vk.com/authorize?"
            f"client_id={settings.VK_APP_ID}&"
            f"display=page&"
            f"redirect_uri={settings.CORS_ORIGINS[0]}/api/auth/oauth/vk/callback&"
            f"scope=email&"
            f"response_type=code&"
            f"v={settings.VK_API_VERSION}"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="지원하지 않는 OAuth 프로바이더입니다"
        )

    return RedirectResponse(url=auth_url)

@router.post("/oauth/{provider}/callback", response_model=TokenResponse)
async def oauth_callback(
    provider: str,
    callback_data: OAuthCallback,
    request: Request,
    db: Session = Depends(get_db)
):
    """소셜 로그인 콜백 처리"""
    user_info = None

    if provider == "google":
        user_info = await _handle_google_callback(callback_data.code)
    elif provider == "kakao":
        user_info = await _handle_kakao_callback(callback_data.code)
    elif provider == "naver":
        user_info = await _handle_naver_callback(callback_data.code)
    elif provider == "facebook":
        user_info = await _handle_facebook_callback(callback_data.code)
    elif provider == "vk":
        user_info = await _handle_vk_callback(callback_data.code)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="지원하지 않는 OAuth 프로바이더입니다"
        )

    # 기존 사용자 확인
    user = db.query(User).filter(
        User.oauth_provider == provider,
        User.oauth_uid == str(user_info["id"])
    ).first()

    if not user:
        # 이메일로 기존 계정 확인
        if user_info.get("email"):
            user = db.query(User).filter(User.email == user_info["email"]).first()

        if not user:
            # 닉네임 음역
            nickname = user_info.get("name", f"User{user_info['id'][:8]}")
            nickname_ko, nickname_ru = transliterate_nickname(nickname)

            # 새 사용자 생성
            user = User(
                email=user_info.get("email", f"{provider}_{user_info['id']}@kru.community"),
                nickname=nickname,
                nickname_ko=nickname_ko,
                nickname_ru=nickname_ru,
                oauth_provider=provider,
                oauth_uid=str(user_info["id"]),
                profile_image=user_info.get("picture"),
                is_verified=True,
                email_verified_at=datetime.utcnow(),
                user_type='REAL'  # 실제 가입회원으로 설정
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # OAuth 정보 업데이트
            user.oauth_provider = provider
            user.oauth_uid = str(user_info["id"])
            db.commit()

    # 로그인 처리
    user.last_login_at = datetime.utcnow()
    db.commit()

    # 토큰 생성
    access_jti = generate_jti()
    refresh_jti = generate_jti()
    access_token = create_access_token({"sub": str(user.id), "jti": access_jti})
    refresh_token = create_refresh_token({"sub": str(user.id), "jti": refresh_jti})

    # 세션 저장
    session = UserSession(
        user_id=user.id,
        access_token_jti=access_jti,
        refresh_token_jti=refresh_jti,
        user_agent=request.headers.get("User-Agent"),
        ip_address=request.client.host,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(session)
    db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

async def _handle_vk_callback(code: str) -> dict:
    """VK OAuth 콜백 처리"""
    async with httpx.AsyncClient() as client:
        # 액세스 토큰 획득
        token_response = await client.get(
            "https://oauth.vk.com/access_token",
            params={
                "client_id": settings.VK_APP_ID,
                "client_secret": settings.VK_APP_SECRET,
                "redirect_uri": f"{settings.CORS_ORIGINS[0]}/api/auth/oauth/vk/callback",
                "code": code
            }
        )
        token_data = token_response.json()

        if "error" in token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="VK 인증에 실패했습니다"
            )

        # 사용자 정보 획득
        user_response = await client.get(
            "https://api.vk.com/method/users.get",
            params={
                "user_ids": token_data["user_id"],
                "fields": "photo_200,city,country",
                "access_token": token_data["access_token"],
                "v": settings.VK_API_VERSION
            }
        )
        user_data = user_response.json()

        if "response" not in user_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="VK 사용자 정보를 가져올 수 없습니다"
            )

        vk_user = user_data["response"][0]
        return {
            "id": str(vk_user["id"]),
            "email": token_data.get("email"),
            "name": f"{vk_user.get('first_name', '')} {vk_user.get('last_name', '')}".strip(),
            "picture": vk_user.get("photo_200")
        }

async def _handle_google_callback(code: str) -> dict:
    """Google OAuth 콜백 처리"""
    async with httpx.AsyncClient() as client:
        # 액세스 토큰 획득
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": f"{settings.CORS_ORIGINS[0]}/api/auth/oauth/google/callback",
                "grant_type": "authorization_code"
            }
        )
        token_data = token_response.json()

        # 사용자 정보 획득
        user_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {token_data['access_token']}"}
        )
        return user_response.json()

async def _handle_kakao_callback(code: str) -> dict:
    """Kakao OAuth 콜백 처리"""
    async with httpx.AsyncClient() as client:
        # 액세스 토큰 획득
        token_response = await client.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": settings.KAKAO_CLIENT_ID,
                "client_secret": settings.KAKAO_CLIENT_SECRET,
                "redirect_uri": f"{settings.CORS_ORIGINS[0]}/api/auth/oauth/kakao/callback",
                "code": code
            }
        )
        token_data = token_response.json()

        # 사용자 정보 획득
        user_response = await client.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {token_data['access_token']}"}
        )
        kakao_user = user_response.json()
        return {
            "id": str(kakao_user["id"]),
            "email": kakao_user.get("kakao_account", {}).get("email"),
            "name": kakao_user.get("properties", {}).get("nickname"),
            "picture": kakao_user.get("properties", {}).get("profile_image")
        }

async def _handle_naver_callback(code: str) -> dict:
    """Naver OAuth 콜백 처리"""
    async with httpx.AsyncClient() as client:
        # 액세스 토큰 획득
        token_response = await client.post(
            "https://nid.naver.com/oauth2.0/token",
            data={
                "grant_type": "authorization_code",
                "client_id": settings.NAVER_CLIENT_ID,
                "client_secret": settings.NAVER_CLIENT_SECRET,
                "code": code,
                "state": "random_state"  # 실제로는 세션에서 가져와야 함
            }
        )
        token_data = token_response.json()

        if "error" in token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Naver 인증에 실패했습니다"
            )

        # 사용자 정보 획득
        user_response = await client.get(
            "https://openapi.naver.com/v1/nid/me",
            headers={"Authorization": f"Bearer {token_data['access_token']}"}
        )
        naver_user = user_response.json()

        if "response" not in naver_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Naver 사용자 정보를 가져올 수 없습니다"
            )

        user_data = naver_user["response"]
        return {
            "id": str(user_data["id"]),
            "email": user_data.get("email"),
            "name": user_data.get("name"),
            "picture": user_data.get("profile_image")
        }

async def _handle_facebook_callback(code: str) -> dict:
    """Facebook OAuth 콜백 처리"""
    async with httpx.AsyncClient() as client:
        # 액세스 토큰 획득
        token_response = await client.get(
            "https://graph.facebook.com/v18.0/oauth/access_token",
            params={
                "client_id": settings.FACEBOOK_APP_ID,
                "client_secret": settings.FACEBOOK_APP_SECRET,
                "redirect_uri": f"{settings.CORS_ORIGINS[0]}/api/auth/oauth/facebook/callback",
                "code": code
            }
        )
        token_data = token_response.json()

        if "error" in token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Facebook 인증에 실패했습니다"
            )

        # 사용자 정보 획득
        user_response = await client.get(
            "https://graph.facebook.com/me",
            params={
                "fields": "id,name,email,picture.type(large)",
                "access_token": token_data["access_token"]
            }
        )
        facebook_user = user_response.json()

        return {
            "id": str(facebook_user["id"]),
            "email": facebook_user.get("email"),
            "name": facebook_user.get("name"),
            "picture": facebook_user.get("picture", {}).get("data", {}).get("url")
        }