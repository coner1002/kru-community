from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import random
import string
import secrets
import logging
from app.db.database import get_db
from app.models.user import User, EmailVerification, SMSVerification
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# ============================================================
# 이메일 인증 관련
# ============================================================

class EmailVerificationRequest(BaseModel):
    email: EmailStr

class EmailVerificationConfirm(BaseModel):
    email: EmailStr
    code: str

def generate_verification_token():
    """이메일 인증 토큰 생성 (32자리)"""
    return secrets.token_urlsafe(32)

def generate_verification_code():
    """6자리 인증번호 생성"""
    return ''.join(random.choices(string.digits, k=6))

def send_verification_email(email: str, code: str):
    """
    이메일 인증번호 발송
    나중에 SendGrid API로 교체 예정
    """
    try:
        # TODO: SendGrid 연동
        logger.info(f"[이메일 인증] {email} -> 인증번호: {code}")
        print(f"\n{'='*50}")
        print(f"📧 이메일 인증번호 발송")
        print(f"수신: {email}")
        print(f"인증번호: {code}")
        print(f"유효시간: 5분")
        print(f"{'='*50}\n")
        return True
    except Exception as e:
        logger.error(f"이메일 발송 실패: {e}")
        return False

@router.post("/email/send")
async def send_email_verification(
    request: EmailVerificationRequest,
    db: Session = Depends(get_db)
):
    """이메일 인증번호 발송"""
    # 이미 가입된 이메일인지 확인
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다")

    # 기존 인증 요청 삭제 (5분 이내 재발송 방지는 프론트에서 처리)
    db.query(EmailVerification).filter(
        EmailVerification.email == request.email,
        EmailVerification.verified_at.is_(None)
    ).delete()

    # 인증번호 생성 및 저장
    code = generate_verification_code()
    token = generate_verification_token()
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    verification = EmailVerification(
        user_id=0,  # 회원가입 전
        token=token,
        email=request.email,
        expires_at=expires_at
    )
    db.add(verification)
    db.commit()

    # 이메일 발송
    success = send_verification_email(request.email, code)
    if not success:
        raise HTTPException(status_code=500, detail="이메일 발송에 실패했습니다")

    # 개발 환경: 인증번호를 응답에 포함 (프로덕션에서는 제거)
    return {
        "success": True,
        "message": "인증번호가 발송되었습니다",
        "dev_code": code,  # TODO: 프로덕션에서 제거
        "token": token,
        "expires_at": expires_at.isoformat()
    }

@router.post("/email/verify")
async def verify_email_code(
    request: EmailVerificationConfirm,
    db: Session = Depends(get_db)
):
    """이메일 인증번호 확인"""
    verification = db.query(EmailVerification).filter(
        EmailVerification.email == request.email,
        EmailVerification.verified_at.is_(None)
    ).order_by(EmailVerification.created_at.desc()).first()

    if not verification:
        raise HTTPException(status_code=404, detail="인증 요청을 찾을 수 없습니다")

    # 만료 확인
    if datetime.utcnow() > verification.expires_at:
        raise HTTPException(status_code=400, detail="인증번호가 만료되었습니다")

    # TODO: 실제 인증번호 확인 (현재는 개발용으로 항상 통과)
    # if verification.code != request.code:
    #     raise HTTPException(status_code=400, detail="인증번호가 일치하지 않습니다")

    # 인증 완료 처리
    verification.verified_at = datetime.utcnow()
    db.commit()

    return {
        "success": True,
        "message": "이메일 인증이 완료되었습니다",
        "token": verification.token
    }

# ============================================================
# SMS 인증 관련
# ============================================================

class SMSVerificationRequest(BaseModel):
    phone: str

class SMSVerificationConfirm(BaseModel):
    phone: str
    code: str

def send_sms_verification(phone: str, code: str):
    """
    SMS 인증번호 발송
    나중에 알리고/NHN Cloud API로 교체 예정
    """
    try:
        # TODO: SMS API 연동 (알리고 또는 NHN Cloud)
        logger.info(f"[SMS 인증] {phone} -> 인증번호: {code}")
        print(f"\n{'='*50}")
        print(f"📱 SMS 인증번호 발송")
        print(f"수신: {phone}")
        print(f"인증번호: {code}")
        print(f"유효시간: 3분")
        print(f"{'='*50}\n")
        return True
    except Exception as e:
        logger.error(f"SMS 발송 실패: {e}")
        return False

@router.post("/sms/send")
async def send_sms_verification_code(
    request: SMSVerificationRequest,
    db: Session = Depends(get_db)
):
    """SMS 인증번호 발송"""
    # 전화번호 형식 검증 (간단한 검증)
    phone = request.phone.replace("-", "").replace(" ", "")
    if not phone.startswith("010") or len(phone) != 11:
        raise HTTPException(status_code=400, detail="올바른 전화번호 형식이 아닙니다")

    # 이미 가입된 전화번호인지 확인
    existing_user = db.query(User).filter(User.phone == phone).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 가입된 전화번호입니다")

    # 최근 1분 이내 발송 내역 확인 (스팸 방지)
    recent_verification = db.query(SMSVerification).filter(
        SMSVerification.phone == phone,
        SMSVerification.created_at > datetime.utcnow() - timedelta(minutes=1)
    ).first()
    if recent_verification:
        raise HTTPException(status_code=429, detail="1분 후에 다시 시도해주세요")

    # 기존 미인증 요청 삭제
    db.query(SMSVerification).filter(
        SMSVerification.phone == phone,
        SMSVerification.verified_at.is_(None)
    ).delete()

    # 인증번호 생성 및 저장
    code = generate_verification_code()
    expires_at = datetime.utcnow() + timedelta(minutes=3)

    verification = SMSVerification(
        phone=phone,
        code=code,
        expires_at=expires_at,
        attempt_count=0
    )
    db.add(verification)
    db.commit()

    # SMS 발송
    success = send_sms_verification(phone, code)
    if not success:
        raise HTTPException(status_code=500, detail="SMS 발송에 실패했습니다")

    # 개발 환경: 인증번호를 응답에 포함 (프로덕션에서는 제거)
    return {
        "success": True,
        "message": "인증번호가 발송되었습니다",
        "dev_code": code,  # TODO: 프로덕션에서 제거
        "expires_at": expires_at.isoformat()
    }

@router.post("/sms/verify")
async def verify_sms_code(
    request: SMSVerificationConfirm,
    db: Session = Depends(get_db)
):
    """SMS 인증번호 확인"""
    phone = request.phone.replace("-", "").replace(" ", "")

    verification = db.query(SMSVerification).filter(
        SMSVerification.phone == phone,
        SMSVerification.verified_at.is_(None)
    ).order_by(SMSVerification.created_at.desc()).first()

    if not verification:
        raise HTTPException(status_code=404, detail="인증 요청을 찾을 수 없습니다")

    # 만료 확인
    if datetime.utcnow() > verification.expires_at:
        raise HTTPException(status_code=400, detail="인증번호가 만료되었습니다")

    # 시도 횟수 확인 (5회 초과 시 차단)
    if verification.attempt_count >= 5:
        raise HTTPException(status_code=400, detail="인증 시도 횟수를 초과했습니다")

    # 인증번호 확인
    if verification.code != request.code:
        verification.attempt_count += 1
        db.commit()
        remaining = 5 - verification.attempt_count
        raise HTTPException(
            status_code=400,
            detail=f"인증번호가 일치하지 않습니다 (남은 시도: {remaining}회)"
        )

    # 인증 완료 처리
    verification.verified_at = datetime.utcnow()
    db.commit()

    return {
        "success": True,
        "message": "전화번호 인증이 완료되었습니다"
    }

# ============================================================
# 인증 상태 확인
# ============================================================

@router.get("/status")
async def check_verification_status(
    email: str = None,
    phone: str = None,
    db: Session = Depends(get_db)
):
    """이메일/전화번호 인증 상태 확인"""
    result = {
        "email_verified": False,
        "phone_verified": False
    }

    if email:
        verification = db.query(EmailVerification).filter(
            EmailVerification.email == email,
            EmailVerification.verified_at.isnot(None)
        ).first()
        result["email_verified"] = verification is not None

    if phone:
        phone = phone.replace("-", "").replace(" ", "")
        verification = db.query(SMSVerification).filter(
            SMSVerification.phone == phone,
            SMSVerification.verified_at.isnot(None)
        ).first()
        result["phone_verified"] = verification is not None

    return result
