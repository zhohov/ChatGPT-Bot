"""Initial

Revision ID: caaa7e6b1410
Revises: 
Create Date: 2023-04-08 15:33:47.657467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'caaa7e6b1410'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.TEXT(), nullable=True),
    sa.Column('register_date', sa.DATE(), nullable=True),
    sa.Column('requests', sa.Integer(), nullable=True),
    sa.Column('subscription', sa.Integer(), nullable=True),
    sa.Column('subscription_end_date', sa.Integer(), nullable=True),
    sa.Column('custom_key', sa.Integer(), nullable=True),
    sa.Column('user_openai_key', sa.TEXT(), nullable=True),
    sa.Column('user_openai_max_tokens', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
