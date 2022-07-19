"""adding column on post table

Revision ID: 208733217c3d
Revises: 53a91c8a4cf1
Create Date: 2022-07-15 04:50:39.949512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '208733217c3d'
down_revision = '53a91c8a4cf1'
branch_labels = None
depends_on = None


def upgrade() :
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,
               server_default='True'),)
    op.add_column('posts',sa.Column('created_at',
           sa.TIMESTAMP(timezone = True),nullable=False,server_default=sa.text('now()')),)
    pass


def downgrade() :
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
