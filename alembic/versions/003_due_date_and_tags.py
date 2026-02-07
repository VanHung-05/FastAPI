"""due_date and tags

Revision ID: 003
Revises: 002
Create Date: 2025-02-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("todos", sa.Column("due_date", sa.Date(), nullable=True))
    op.add_column("todos", sa.Column("tags", postgresql.ARRAY(sa.Text()), nullable=True))


def downgrade() -> None:
    op.drop_column("todos", "tags")
    op.drop_column("todos", "due_date")
