"""Remove content_type column from images table

Revision ID: 3da7ffb12a2e
Revises: 7b8d2decf6dc
Create Date: 2024-03-25 10:56:57.331107

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3da7ffb12a2e'
down_revision: Union[str, None] = '7b8d2decf6dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
