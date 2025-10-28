import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "coner1002@gmail.com"
SMTP_PASSWORD = "oxjqzyehkoyvseiv"
ADMIN_EMAIL = "coner1002@naver.com"

try:
    print("SMTP 서버 연결 시도...")
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    print("TLS 시작...")

    print(f"로그인 시도: {SMTP_USERNAME}")
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    print("로그인 성공!")

    msg = MIMEMultipart()
    msg['Subject'] = "테스트 메일"
    msg['From'] = SMTP_USERNAME
    msg['To'] = ADMIN_EMAIL

    body = MIMEText("테스트 메일입니다.", 'plain', 'utf-8')
    msg.attach(body)

    server.send_message(msg)
    print(f"메일 전송 성공: {ADMIN_EMAIL}")

    server.quit()

except Exception as e:
    print(f"오류 발생: {e}")
