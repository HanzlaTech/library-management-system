"""create record table

Revision ID: c366d69495b6
Revises: bb77f873bd57
Create Date: 2026-08-29 23:31:45.385835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c366d69495b6'
down_revision: Union[str, Sequence[str], None] = 'bb77f873bd57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # op.create_table(
    #     "record",
    #     sa.Column("User_id", sa.Integer(), nullable=True),
    #     sa.Column("Book_id", sa.Integer(), nullable=True),
    #     sa.Column("Status", sa.String(20), nullable=True),
    #     sa.Index("User_id", "User_id"),
    #     sa.ForeignKeyConstraint(
    #         ["User_id"],
    #         ["users.User_id"],
    #         name="record_ibfk_1",
    #     ),
    #     mysql_charset="utf8mb4",
    #     mysql_collate="utf8mb4_0900_ai_ci",
    # )
    op.create_table(
        "record",
        sa.Column("User_id",sa.Integer(),nullable=False),
        sa.Column("Book_id",sa.Integer(),nullable=False),
        sa.Column("Status",sa.String(100),nullable=False),
        sa.ForeignKeyConstraint(
            ["User_id"],
            ["users.User_id"]
        ),
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_0900_as_cs"
    )


def downgrade():
    op.drop_table("record")