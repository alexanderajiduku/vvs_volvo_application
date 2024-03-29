"""Changing ultralytics model and schema

Revision ID: 0e84ff74bd7a
Revises: 02f9033577a8
Create Date: 2024-02-19 12:42:03.523016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0e84ff74bd7a'
down_revision: Union[str, None] = '02f9033577a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ultralyticsuploads', sa.Column('upload_timestamp', sa.DateTime(), nullable=True))
    op.alter_column('ultralyticsuploads', 'filename',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('ultralyticsuploads', 'content_type',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('ultralyticsuploads', 'file_path',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.create_index(op.f('ix_ultralyticsuploads_filename'), 'ultralyticsuploads', ['filename'], unique=False)
    op.drop_column('ultralyticsuploads', 'uploaded_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ultralyticsuploads', sa.Column('uploaded_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_ultralyticsuploads_filename'), table_name='ultralyticsuploads')
    op.alter_column('ultralyticsuploads', 'file_path',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('ultralyticsuploads', 'content_type',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('ultralyticsuploads', 'filename',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('ultralyticsuploads', 'upload_timestamp')
    # ### end Alembic commands ###
