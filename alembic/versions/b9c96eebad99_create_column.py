"""create column

Revision ID: b9c96eebad99
Revises: 6f27d037c36a
Create Date: 2026-08-19 16:55:27.693540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9c96eebad99'
down_revision: Union[str, Sequence[str], None] = '6f27d037c36a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
