"""Remove content_type column from images table

Revision ID: 7b8d2decf6dc
Revises: 47a8c15562d6
Create Date: 2024-03-25 10:53:50.225530

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b8d2decf6dc'
down_revision: Union[str, None] = '47a8c15562d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
