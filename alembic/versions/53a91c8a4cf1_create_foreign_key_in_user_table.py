"""create foreign key in user table

Revision ID: 53a91c8a4cf1
Revises: 359d27799921
Create Date: 2022-07-15 04:35:59.843374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53a91c8a4cf1'
down_revision = '359d27799921'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_user_fk',source_table="posts",referent_table="users",
        local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade():
    op.drop_column('posts','owner_id')
    op.drop_constraint('post_user_fk',table_name='posts')
    pass
