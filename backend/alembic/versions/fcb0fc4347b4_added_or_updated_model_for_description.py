"""Added or updated Model for description

Revision ID: fcb0fc4347b4
Revises: 34abcf096124
Create Date: 2024-02-17 14:55:00.375729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcb0fc4347b4'
down_revision: Union[str, None] = '34abcf096124'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('models', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('models', 'description')
    # ### end Alembic commands ###
