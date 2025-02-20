"""Added a refresh_token_id column in Users table

Revision ID: 3ca2eb28739d
Revises: 60319fdf5652
Create Date: 2025-01-21 14:43:15.916545

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from source.database_service.database_config import Base

# revision identifiers, used by Alembic.
revision: str = "3ca2eb28739d"
down_revision: Union[str, None] = "60319fdf5652"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
