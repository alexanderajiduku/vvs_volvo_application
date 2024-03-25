"""Remove content_type column from images table

Revision ID: bf33485f91ff
Revises: 560b6a48e928
Create Date: 2024-03-25 10:51:35.435051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf33485f91ff'
down_revision: Union[str, None] = '560b6a48e928'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
