"""init

Revision ID: 4b37b4fb5ec3
Revises: 
Create Date: 2021-05-13 22:23:41.110195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b37b4fb5ec3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ended_process',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mp4', sa.String(length=50), nullable=True),
    sa.Column('webm', sa.String(length=50), nullable=True),
    sa.Column('json', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('runned_process',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('frameCount', sa.Integer(), nullable=True),
    sa.Column('currentFrame', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('started_process',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('started_process')
    op.drop_table('runned_process')
    op.drop_table('ended_process')
    # ### end Alembic commands ###