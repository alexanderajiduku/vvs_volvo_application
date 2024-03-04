"""Added vehicle details and heigh in the db2

Revision ID: e199c525de16
Revises: 776f83b4f344
Create Date: 2024-03-04 21:01:48.404776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e199c525de16'
down_revision: Union[str, None] = '776f83b4f344'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehicle_heights',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vehicle_id', sa.Integer(), nullable=True),
    sa.Column('height', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicle_details.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vehicle_heights_id'), 'vehicle_heights', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_vehicle_heights_id'), table_name='vehicle_heights')
    op.drop_table('vehicle_heights')
    # ### end Alembic commands ###
