from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ContactRequest(BaseModel):
    type: str  # 'ad' or 'suggest'
    name: str
    email: EmailStr
    company: Optional[str] = None
    phone: Optional[str] = None
    requestType: Optional[str] = None
    suggestType: Optional[str] = None
    title: str
    content: str

# 메일 전송 설정
ADMIN_EMAIL = "coner1002@naver.com"
SMTP_SERVER = "smtp.gmail.com"  # Gmail SMTP
SMTP_PORT = 587
SMTP_USERNAME = "coner1002@gmail.com"
SMTP_PASSWORD = "oxjqzyehkoyvseiv"  # Gmail 앱 비밀번호

def send_email(contact: ContactRequest):
    """메일 전송 함수"""
    try:
        # 메일 내용 작성
        type_label = "광고/협력 요청" if contact.type == "ad" else "운영자 건의"

        # 요청 유형 매핑
        request_type_map = {
            'banner': '배너 광고',
            'content': '콘텐츠 협찬',
            'partnership': '비즈니스 제휴',
            'event': '이벤트 협력',
            'improvement': '서비스 개선',
            'feature': '기능 추가',
            'bug': '버그 신고',
            'complaint': '불편 사항',
            'question': '질문',
            'other': '기타'
        }

        request_type = contact.requestType or contact.suggestType or 'other'
        request_type_label = request_type_map.get(request_type, '기타')

        # HTML 메일 본문
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #0039A6; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .info-row {{ margin-bottom: 15px; padding: 10px; background-color: #f8f9fa; border-left: 4px solid #0039A6; }}
                .label {{ font-weight: bold; color: #0039A6; }}
                .value {{ margin-left: 10px; }}
                .message-box {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🔔 Russki.Center 새로운 연락 알림</h2>
            </div>
            <div class="content">
                <div class="info-row">
                    <span class="label">📋 유형:</span>
                    <span class="value">{type_label}</span>
                </div>
                <div class="info-row">
                    <span class="label">👤 이름:</span>
                    <span class="value">{contact.name}</span>
                </div>
                {f'<div class="info-row"><span class="label">🏢 회사명:</span><span class="value">{contact.company}</span></div>' if contact.company else ''}
                <div class="info-row">
                    <span class="label">📧 이메일:</span>
                    <span class="value">{contact.email}</span>
                </div>
                {f'<div class="info-row"><span class="label">📞 연락처:</span><span class="value">{contact.phone}</span></div>' if contact.phone else ''}
                <div class="info-row">
                    <span class="label">📂 요청 유형:</span>
                    <span class="value">{request_type_label}</span>
                </div>
                <div class="info-row">
                    <span class="label">📌 제목:</span>
                    <span class="value"><strong>{contact.title}</strong></span>
                </div>
                <div class="message-box">
                    <div class="label">📝 상세 내용:</div>
                    <div style="margin-top: 10px; white-space: pre-wrap;">{contact.content}</div>
                </div>
                <div class="info-row">
                    <span class="label">🕐 접수 일시:</span>
                    <span class="value">{datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}</span>
                </div>
            </div>
            <div class="footer">
                <p>이 메일은 Russki.Center 운영자 연락 시스템에서 자동으로 발송되었습니다.</p>
                <p>관리자 페이지에서 더 자세한 내용을 확인하실 수 있습니다.</p>
            </div>
        </body>
        </html>
        """

        # 메일 메시지 생성
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"[Russki.Center] {type_label} - {contact.title}"
        msg['From'] = SMTP_USERNAME or "noreply@russki.center"
        msg['To'] = ADMIN_EMAIL
        msg['Reply-To'] = contact.email

        # HTML 본문 추가
        html_part = MIMEText(html_body, 'html', 'utf-8')
        msg.attach(html_part)

        # SMTP 서버가 설정되어 있지 않으면 로그만 남김
        if not SMTP_USERNAME or not SMTP_PASSWORD:
            logger.warning("SMTP 설정이 없습니다. 메일 전송을 시뮬레이션합니다.")
            logger.info(f"[메일 전송 시뮬레이션] To: {ADMIN_EMAIL}, Subject: {msg['Subject']}")
            return True

        # 메일 전송
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"메일 전송 성공: {ADMIN_EMAIL}")
        return True

    except Exception as e:
        logger.error(f"메일 전송 실패: {str(e)}")
        return False

@router.post("/send")
async def send_contact_email(contact: ContactRequest):
    """
    운영자 연락 메일 전송 API
    """
    try:
        # 메일 전송
        success = send_email(contact)

        if success:
            return {
                "success": True,
                "message": "문의가 접수되었습니다. 빠른 시일 내에 답변드리겠습니다."
            }
        else:
            # 메일 전송 실패해도 localStorage에는 저장되므로 부분 성공 처리
            return {
                "success": True,
                "message": "문의가 접수되었습니다.",
                "warning": "메일 알림 전송에 일부 문제가 있었습니다."
            }

    except Exception as e:
        logger.error(f"Contact API 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="문의 접수 중 오류가 발생했습니다.")
