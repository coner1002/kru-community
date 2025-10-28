"""
프로젝트 정리 스크립트
불필요한 임시 파일들을 backup 폴더로 이동
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

# 프로젝트 루트 디렉토리
ROOT_DIR = Path(__file__).parent

# 백업 폴더 생성 (날짜별)
backup_date = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = ROOT_DIR / "backup" / backup_date
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# 보관할 중요 파일 목록 (이동하지 않음)
KEEP_FILES = {
    # 설정 파일
    ".env",
    ".gitignore",
    "CLAUDE.md",
    "AUTH_GUIDE.md",
    "DEPLOYMENT.md",
    "README.md",

    # 유지할 배치 파일 (메인 실행 파일만)
    "QUICK_START.bat",
    "START_BACKEND.bat",

    # 현재 실행 중인 스크립트
    "cleanup_project.py",
}

# 보관할 디렉토리 (이동하지 않음)
KEEP_DIRS = {
    "backend",
    "frontend",
    "scripts",
    "data",
    "deploy",
    ".git",
    ".vscode",
    ".claude",
    ".history-memo",
    "backups",
    "backup",
}

def should_move_to_backup(file_path: Path) -> bool:
    """파일을 백업으로 이동해야 하는지 판단"""

    # 디렉토리는 건너뜀
    if file_path.is_dir():
        return False

    # 보관할 파일은 건너뜀
    if file_path.name in KEEP_FILES:
        return False

    filename = file_path.name.lower()

    # 임시 수정 스크립트들 (fix_, update_, add_, cleanup_ 등)
    temp_script_patterns = [
        "fix_", "update_", "add_", "cleanup_", "apply_",
        "unify_", "rebuild_", "replace_", "convert_",
        "make_", "copy_", "simple_", "final_",
        "insert_", "create_test", "test_"
    ]

    if filename.endswith(".py"):
        for pattern in temp_script_patterns:
            if filename.startswith(pattern):
                return True

    # 중복/불필요한 배치 파일
    if filename.endswith(".bat"):
        unnecessary_bat = [
            "start_backend_fixed",
            "check_backend",
            "install_packages",
            "diagnose",
            "setup_all"
        ]
        for pattern in unnecessary_bat:
            if pattern in filename:
                return True

    return False

def move_files_to_backup():
    """불필요한 파일들을 백업 폴더로 이동"""

    moved_files = []
    kept_files = []

    print(f"백업 폴더: {BACKUP_DIR}")
    print("\n" + "="*60)
    print("파일 정리 시작...")
    print("="*60 + "\n")

    # 루트 디렉토리의 파일들만 검사
    for item in ROOT_DIR.iterdir():
        # 디렉토리 건너뛰기
        if item.is_dir():
            if item.name not in KEEP_DIRS:
                print(f"⚠️  디렉토리 발견 (수동 확인 필요): {item.name}")
            continue

        # 백업으로 이동해야 하는 파일
        if should_move_to_backup(item):
            try:
                # 백업 폴더 내 카테고리별 분류
                if item.suffix == ".py":
                    category_dir = BACKUP_DIR / "python_scripts"
                elif item.suffix == ".bat":
                    category_dir = BACKUP_DIR / "batch_files"
                else:
                    category_dir = BACKUP_DIR / "other_files"

                category_dir.mkdir(exist_ok=True)

                # 파일 이동
                dest = category_dir / item.name
                shutil.move(str(item), str(dest))
                moved_files.append(item.name)
                print(f"✅ 이동: {item.name} → backup/{backup_date}/{category_dir.name}/")
            except Exception as e:
                print(f"❌ 이동 실패: {item.name} - {e}")
        else:
            kept_files.append(item.name)

    # 결과 요약
    print("\n" + "="*60)
    print("정리 완료!")
    print("="*60)
    print(f"\n📦 백업으로 이동한 파일: {len(moved_files)}개")
    print(f"✅ 프로젝트에 유지된 파일: {len(kept_files)}개")

    if moved_files:
        print(f"\n백업 위치: {BACKUP_DIR}")
        print("\n이동된 파일 카테고리:")
        print(f"  - Python 스크립트: backup/{backup_date}/python_scripts/")
        print(f"  - Batch 파일: backup/{backup_date}/batch_files/")

    # 백업된 파일 목록 저장
    manifest_file = BACKUP_DIR / "BACKUP_MANIFEST.txt"
    with open(manifest_file, "w", encoding="utf-8") as f:
        f.write(f"백업 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"백업된 파일 개수: {len(moved_files)}\n\n")
        f.write("="*60 + "\n")
        f.write("백업된 파일 목록:\n")
        f.write("="*60 + "\n\n")
        for filename in sorted(moved_files):
            f.write(f"  - {filename}\n")

    print(f"\n📄 백업 목록: {manifest_file}")

    return moved_files, kept_files

def create_readme():
    """정리 후 프로젝트 구조 README 생성"""
    readme_content = """# KRU Community 프로젝트 구조

## 📁 주요 디렉토리

- `backend/` - FastAPI 백엔드 서버
- `frontend/` - Next.js 프론트엔드 (또는 정적 HTML)
- `scripts/` - 유틸리티 스크립트
- `data/` - 데이터 파일
- `deploy/` - 배포 관련 파일
- `backup/` - 정리된 임시 파일들의 백업

## 🚀 실행 방법

### 백엔드 + 정적 프론트엔드 (권장)
```bash
QUICK_START.bat
```

### 백엔드만 실행
```bash
START_BACKEND.bat
```

## 📚 문서

- `AUTH_GUIDE.md` - 인증 시스템 가이드
- `DEPLOYMENT.md` - 배포 가이드
- `CLAUDE.md` - Claude AI 프롬프트

## 🗂️ 백업 정보

임시 수정 스크립트와 중복 배치 파일들은 `backup/` 폴더에 날짜별로 보관됩니다.
필요시 언제든 복구할 수 있습니다.

---
마지막 정리: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    readme_path = ROOT_DIR / "PROJECT_STRUCTURE.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"\n📖 프로젝트 구조 문서 생성: {readme_path}")

if __name__ == "__main__":
    import sys
    import io
    # UTF-8 출력 설정
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("🧹 프로젝트 정리 시작...\n")

    # 사용자 확인
    print("다음 파일들이 백업 폴더로 이동됩니다:")
    print("  - fix_*.py, update_*.py, add_*.py 등 임시 수정 스크립트")
    print("  - 중복/불필요한 배치 파일")
    print(f"\n백업 위치: backup/{backup_date}/")
    print("\n계속하시겠습니까? (y/n): ", end="")

    response = input().strip().lower()
    if response != 'y':
        print("\n취소되었습니다.")
        exit(0)

    print()
    moved, kept = move_files_to_backup()
    create_readme()

    print("\n✨ 프로젝트 정리가 완료되었습니다!")
    print("\n주요 실행 파일:")
    print("  - QUICK_START.bat (백엔드 + 정적 HTML)")
    print("  - START_BACKEND.bat (백엔드만)")