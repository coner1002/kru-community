"""Add user role tiers and category permissions

Revision ID: 72c9f5d3e752
Revises: 8709aa2249be
Create Date: 2025-10-23 17:22:01.053929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72c9f5d3e752'
down_revision = '8709aa2249be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Detect database dialect
    bind = op.get_bind()
    dialect_name = bind.dialect.name

    # Check if columns already exist
    from sqlalchemy import inspect
    inspector = inspect(bind)
    existing_columns = [col['name'] for col in inspector.get_columns('categories')]

    columns_to_add = []
    if 'read_permission' not in existing_columns:
        columns_to_add.append('read_permission')
    if 'write_permission' not in existing_columns:
        columns_to_add.append('write_permission')
    if 'comment_permission' not in existing_columns:
        columns_to_add.append('comment_permission')

    if not columns_to_add:
        print("Permission columns already exist, skipping...")
        return

    if dialect_name == 'postgresql':
        # PostgreSQL-specific migration
        if 'read_permission' in columns_to_add:
            op.add_column('categories', sa.Column('read_permission', sa.Enum('ALL', 'USER', 'PREMIUM', 'STAFF', 'ADMIN', name='permissionlevel'), nullable=True))
        if 'write_permission' in columns_to_add:
            op.add_column('categories', sa.Column('write_permission', sa.Enum('ALL', 'USER', 'PREMIUM', 'STAFF', 'ADMIN', name='permissionlevel'), nullable=True))
        if 'comment_permission' in columns_to_add:
            op.add_column('categories', sa.Column('comment_permission', sa.Enum('ALL', 'USER', 'PREMIUM', 'STAFF', 'ADMIN', name='permissionlevel'), nullable=True))

        # Set default values for existing categories
        op.execute("UPDATE categories SET read_permission = 'ALL' WHERE read_permission IS NULL")
        op.execute("UPDATE categories SET write_permission = 'USER' WHERE write_permission IS NULL")
        op.execute("UPDATE categories SET comment_permission = 'USER' WHERE comment_permission IS NULL")

        # Make columns not nullable after setting defaults
        if 'read_permission' in columns_to_add:
            op.alter_column('categories', 'read_permission', nullable=False)
        if 'write_permission' in columns_to_add:
            op.alter_column('categories', 'write_permission', nullable=False)
        if 'comment_permission' in columns_to_add:
            op.alter_column('categories', 'comment_permission', nullable=False)

        # Update UserRole enum to include new roles (staff and premium)
        op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'staff'")
        op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'premium'")

    else:
        # SQLite-specific migration (uses string type for enums)
        if 'read_permission' in columns_to_add:
            op.add_column('categories', sa.Column('read_permission', sa.String(20), nullable=False, server_default='ALL'))
        if 'write_permission' in columns_to_add:
            op.add_column('categories', sa.Column('write_permission', sa.String(20), nullable=False, server_default='USER'))
        if 'comment_permission' in columns_to_add:
            op.add_column('categories', sa.Column('comment_permission', sa.String(20), nullable=False, server_default='USER'))

        # Note: SQLite doesn't enforce enum values at database level
        # Validation will be done at application level via SQLAlchemy


def downgrade() -> None:
    # Remove permission columns from categories
    op.drop_column('categories', 'comment_permission')
    op.drop_column('categories', 'write_permission')
    op.drop_column('categories', 'read_permission')

    # Drop the permission level enum
    op.execute("DROP TYPE IF EXISTS permissionlevel")

    # Note: PostgreSQL doesn't support removing enum values easily
    # Manual intervention may be required to remove staff and premium from userrole enum