"""add public_id on Photo

Revision ID: e63a481db856
Revises: 63c8ab54f85a
Create Date: 2024-05-03 00:42:03.318345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e63a481db856'
down_revision: Union[str, None] = '63c8ab54f85a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photos', sa.Column('cloudinary_public_id', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('photos', 'cloudinary_public_id')
    # ### end Alembic commands ###
