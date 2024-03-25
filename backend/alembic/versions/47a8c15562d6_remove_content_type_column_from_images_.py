"""Remove content_type column from images table

Revision ID: 47a8c15562d6
Revises: bf33485f91ff
Create Date: 2024-03-25 10:52:33.008938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47a8c15562d6'
down_revision: Union[str, None] = 'bf33485f91ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
