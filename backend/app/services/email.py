import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

async def send_verification_email(email: str, token: str):
    """이메일 인증 메일 발송"""
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_USER
        msg['To'] = email
        msg['Subject'] = "KRU Community 이메일 인증"

        body = f"""
        안녕하세요!

        KRU Community에 가입해 주셔서 감사합니다.
        아래 링크를 클릭하여 이메일 인증을 완료해 주세요.

        인증 링크: {settings.CORS_ORIGINS[0]}/verify-email?token={token}

        감사합니다.
        KRU Community 팀
        """

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(settings.SMTP_USER, email, text)
        server.quit()

        logger.info(f"인증 이메일 발송 완료: {email}")

    except Exception as e:
        logger.error(f"이메일 발송 실패: {e}")

async def send_password_reset_email(email: str, token: str):
    """비밀번호 재설정 메일 발송"""
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_USER
        msg['To'] = email
        msg['Subject'] = "KRU Community 비밀번호 재설정"

        body = f"""
        안녕하세요!

        비밀번호 재설정을 요청하셨습니다.
        아래 링크를 클릭하여 새 비밀번호를 설정해 주세요.

        재설정 링크: {settings.CORS_ORIGINS[0]}/reset-password?token={token}

        감사합니다.
        KRU Community 팀
        """

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(settings.SMTP_USER, email, text)
        server.quit()

        logger.info(f"비밀번호 재설정 이메일 발송 완료: {email}")

    except Exception as e:
        logger.error(f"이메일 발송 실패: {e}")