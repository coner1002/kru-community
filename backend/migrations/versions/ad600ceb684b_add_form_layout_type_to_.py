"""Add FORM layout type to CategoryLayoutType enum

Revision ID: ad600ceb684b
Revises: 72c9f5d3e752
Create Date: 2025-10-23 20:36:34.311036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad600ceb684b'
down_revision = '72c9f5d3e752'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Detect database dialect
    bind = op.get_bind()
    dialect_name = bind.dialect.name

    if dialect_name == 'postgresql':
        # PostgreSQL에서는 enum type에 새 값 추가
        op.execute("ALTER TYPE categorylayouttype ADD VALUE IF NOT EXISTS 'form'")
    else:
        # SQLite는 문자열로 저장되므로 아무 작업도 필요 없음
        pass


def downgrade() -> None:
    # PostgreSQL에서는 enum 값 제거가 어렵기 때문에 downgrade는 스킵
    # SQLite는 변경사항이 없으므로 스킵
    pass