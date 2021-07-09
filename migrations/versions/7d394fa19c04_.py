"""empty message

Revision ID: 7d394fa19c04
Revises: 8a68126ba4c7
Create Date: 2021-07-07 16:59:38.482125

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7d394fa19c04'
down_revision = '990f6cf35a92'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('permission',
                    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('name', sa.String(length=80), nullable=True),
                    sa.Column('description', sa.String(length=255), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id'),
                    sa.UniqueConstraint('name')
    )
    op.create_table('roles_permissions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('permission_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
        sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id')
    )

def downgrade():
    op.drop_table('roles_permissions')
    op.drop_table('permission')
