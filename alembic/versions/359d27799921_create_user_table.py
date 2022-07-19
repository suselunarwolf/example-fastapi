"""create user table

Revision ID: 359d27799921
Revises: 4b4e46443465
Create Date: 2022-07-15 04:11:35.333914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '359d27799921'
down_revision = '4b4e46443465'
branch_labels = None
depends_on = None


def upgrade() :
    op.create_table('users',
                sa.Column('id',sa.Integer(),nullable = False),
                sa.Column('email',sa.String(),nullable = False),
                sa.Column('password',sa.String(),nullable = False),
                sa.Column('created_at',sa.TIMESTAMP(timezone = True),
                      server_default=sa.text('now()'),nullable = False),
                 sa.PrimaryKeyConstraint('id'),
                 sa.UniqueConstraint('email'))
    pass


def downgrade() :
    op.drop_table('users')
    pass
