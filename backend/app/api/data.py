"""
게시판 데이터 저장/로드 API
"""
import json
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any

router = APIRouter()

# 데이터 저장 파일 경로
DATA_DIR = Path(__file__).parent.parent.parent / "data"
DATA_FILE = DATA_DIR / "board_data.json"

# 데이터 디렉토리가 없으면 생성
DATA_DIR.mkdir(exist_ok=True)

@router.post("/save")
async def save_board_data(data: Dict[str, Any]):
    """게시판 데이터를 서버에 저장"""
    try:
        # JSON 파일로 저장
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return {"status": "success", "message": "데이터 저장 완료"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터 저장 실패: {str(e)}")

@router.get("/load")
async def load_board_data():
    """서버에서 게시판 데이터 로드"""
    try:
        if not DATA_FILE.exists():
            # 파일이 없으면 빈 데이터 반환
            return {
                "freeboard": [],
                "qna": [],
                "lifeinfo": [],
                "admininfo": [],
                "jobs": [],
                "marketplace": [],
                "partners": []
            }

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터 로드 실패: {str(e)}")

@router.get("/backup")
async def backup_data():
    """현재 데이터의 백업 파일 생성"""
    try:
        if not DATA_FILE.exists():
            raise HTTPException(status_code=404, detail="저장된 데이터가 없습니다")

        # 백업 파일명 (타임스탬프 포함)
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = DATA_DIR / f"board_data_backup_{timestamp}.json"

        # 백업 생성
        import shutil
        shutil.copy2(DATA_FILE, backup_file)

        return {
            "status": "success",
            "message": "백업 생성 완료",
            "backup_file": str(backup_file)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"백업 생성 실패: {str(e)}")