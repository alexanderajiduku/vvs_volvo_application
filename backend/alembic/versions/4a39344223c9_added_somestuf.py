"""Added somestuf

Revision ID: 4a39344223c9
Revises: 1d64019ac2a2
Create Date: 2024-02-17 23:46:28.581793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a39344223c9'
down_revision: Union[str, None] = '1d64019ac2a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('models_user_id_fkey', 'models', type_='foreignkey')
    op.drop_column('models', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('models', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('models_user_id_fkey', 'models', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
