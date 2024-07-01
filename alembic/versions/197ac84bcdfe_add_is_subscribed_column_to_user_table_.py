"""Add is_subscribed column to user table with default value

Revision ID: 197ac84bcdfe
Revises: 
Create Date: 2024-06-23 16:00:22.750247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '197ac84bcdfe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('is_subscribed', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))



def downgrade() -> None:
    op.drop_column('user', 'is_subscribed')

