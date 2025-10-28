#!/usr/bin/env python3
"""
FTP 업로드 스크립트
프론트엔드 파일을 프로덕션 서버에 업로드합니다.
"""

import ftplib
import os
import sys
from pathlib import Path

def upload_file(ftp, local_path, remote_path):
    """단일 파일 업로드"""
    try:
        with open(local_path, 'rb') as file:
            ftp.storbinary(f'STOR {remote_path}', file)
        print(f"✓ 업로드 완료: {remote_path}")
        return True
    except Exception as e:
        print(f"✗ 업로드 실패: {remote_path} - {e}")
        return False

def upload_directory(ftp, local_dir, remote_dir):
    """디렉토리 재귀 업로드"""
    try:
        # 원격 디렉토리 생성 시도
        try:
            ftp.mkd(remote_dir)
        except ftplib.error_perm:
            pass  # 디렉토리가 이미 존재할 수 있음

        ftp.cwd(remote_dir)

        for item in os.listdir(local_dir):
            local_path = os.path.join(local_dir, item)

            if os.path.isfile(local_path):
                upload_file(ftp, local_path, item)
            elif os.path.isdir(local_path):
                # 재귀적으로 하위 디렉토리 업로드
                current_dir = ftp.pwd()
                upload_directory(ftp, local_path, item)
                ftp.cwd(current_dir)

    except Exception as e:
        print(f"디렉토리 업로드 오류: {e}")

def main():
    # FTP 연결 정보 (환경변수에서 가져오거나 기본값 사용)
    FTP_HOST = os.getenv("FTP_HOST", "playground.io.kr")
    FTP_USER = os.getenv("FTP_USER", "")
    FTP_PASS = os.getenv("FTP_PASS", "")

    if not FTP_USER or not FTP_PASS:
        print("오류: FTP 사용자명과 비밀번호가 설정되지 않았습니다.")
        print("환경변수 FTP_USER와 FTP_PASS를 설정하거나")
        print("다음 명령어로 실행하세요:")
        print("set FTP_USER=your_username && set FTP_PASS=your_password && python ftp_upload.py")
        return

    # 로컬 프론트엔드 디렉토리
    local_frontend_dir = Path(__file__).parent.parent / "frontend" / "public"

    if not local_frontend_dir.exists():
        print(f"오류: 프론트엔드 디렉토리를 찾을 수 없습니다: {local_frontend_dir}")
        return

    try:
        # FTP 연결
        print(f"FTP 서버에 연결 중: {FTP_HOST}")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)

        print("연결 성공!")
        print(f"현재 디렉토리: {ftp.pwd()}")

        # public_html 또는 www 디렉토리로 이동 (서버 설정에 따라 다름)
        try:
            ftp.cwd('/public_html')
        except:
            try:
                ftp.cwd('/www')
            except:
                try:
                    ftp.cwd('/htdocs')
                except:
                    print("웹 루트 디렉토리를 찾을 수 없습니다. 현재 디렉토리에 업로드합니다.")

        print(f"업로드 대상 디렉토리: {ftp.pwd()}")

        # 주요 파일들 업로드
        files_to_upload = [
            "index.html",
            "config.js",
            "style.css",  # 만약 별도 CSS 파일이 있다면
        ]

        uploaded_count = 0

        for filename in files_to_upload:
            local_file = local_frontend_dir / filename
            if local_file.exists():
                if upload_file(ftp, str(local_file), filename):
                    uploaded_count += 1
            else:
                print(f"파일을 찾을 수 없습니다: {filename}")

        # assets 디렉토리가 있다면 업로드
        assets_dir = local_frontend_dir / "assets"
        if assets_dir.exists():
            print("assets 디렉토리 업로드 중...")
            upload_directory(ftp, str(assets_dir), "assets")

        print(f"\n업로드 완료! {uploaded_count}개 파일이 업로드되었습니다.")

        # 연결 종료
        ftp.quit()

    except ftplib.error_perm as e:
        print(f"FTP 권한 오류: {e}")
        print("FTP 사용자명, 비밀번호 또는 서버 주소를 확인해주세요.")
    except Exception as e:
        print(f"업로드 오류: {e}")

if __name__ == "__main__":
    main()