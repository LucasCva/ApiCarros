"""primeira migração Carros

Revision ID: f8f3bd248801
Revises: 
Create Date: 2023-12-19 13:38:50.122713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f8f3bd248801'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('carros',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('nome', sa.String(length=30), nullable=True),
                    sa.Column('ano', sa.Integer(), nullable=True),
                    sa.Column('modelo', sa.String(length=30), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('carros')
