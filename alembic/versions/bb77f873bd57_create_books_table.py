"""create books table

Revision ID: bb77f873bd57
Revises: 57c8d80324a1
Create Date: 2026-08-29 23:31:35.490490

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb77f873bd57'
down_revision: Union[str, Sequence[str], None] = '57c8d80324a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # op.create_table(
    #     "books",
    #     sa.Column("Book_id", sa.Integer(), primary_key=True, nullable=False),
    #     sa.Column("Book_isbn", sa.Integer(), nullable=False),
    #     sa.Column("Book_name", sa.String(30), nullable=False),
    #     sa.Column("Author_name", sa.String(30), nullable=False),
    #     sa.UniqueConstraint("Book_id", name="Book_id"),
    #     mysql_charset="utf8mb4",
    #     mysql_collate="utf8mb4_0900_ai_ci",
    # )
    op.create_table(
        "books",
        sa.Column("Book_id",sa.Integer(),nullable=False,primary_key=True),
        sa.Column("Book_isbn",sa.Integer(),nullable=False),
        sa.Column("Book_name",sa.String(100),nullable=False),
        sa.Column("Author_name",sa.String(100),nullable=False),
        sa.UniqueConstraint(
            "Book_id"
        ),
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_0900_as_cs"
        
    )

def downgrade():
   op.drop_table("books")