"""Added vehicle details and heigh in the db3

Revision ID: 560b6a48e928
Revises: e199c525de16
Create Date: 2024-03-04 21:10:09.470465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '560b6a48e928'
down_revision: Union[str, None] = 'e199c525de16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_vehicle_heights_id', table_name='vehicle_heights')
    op.drop_table('vehicle_heights')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehicle_heights',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('vehicle_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('height', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicle_details.id'], name='vehicle_heights_vehicle_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='vehicle_heights_pkey')
    )
    op.create_index('ix_vehicle_heights_id', 'vehicle_heights', ['id'], unique=False)
    # ### end Alembic commands ###
