"""Added registration_date field to Participant

Revision ID: 0224f5c2ee49
Revises: 1df4d1111803
Create Date: 2024-10-30 13:03:14.073947

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0224f5c2ee49'
down_revision: Union[str, None] = '1df4d1111803'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participants', sa.Column('registration_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('participants', 'registration_date')
    # ### end Alembic commands ###
