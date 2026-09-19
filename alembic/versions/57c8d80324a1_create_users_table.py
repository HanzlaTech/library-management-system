"""create users table

Revision ID: 57c8d80324a1
Revises: f8fd566c7a1b
Create Date: 2026-08-29 18:14:06.006962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57c8d80324a1'
down_revision: Union[str, Sequence[str], None] = 'f8fd566c7a1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # op.create_table(
    #     "users",
    #     sa.Column("Email", sa.String(255), nullable=False),
    #     sa.Column("Password", sa.String(255), nullable=True),
    #     sa.Column("User_id", sa.Integer(), primary_key=True, autoincrement=True),
    #     sa.Column("Role", sa.Enum("User", "Admin"), nullable=True),
    #     sa.Column("Email_Verified", sa.Boolean(), nullable=True),
    #     sa.Column("URL", sa.String(267), nullable=True),
    #     sa.UniqueConstraint("Email", name="unique_username"),
    #     sa.UniqueConstraint("Email", name="Username"),
    #     sa.UniqueConstraint("Email", name="Username_2"),
    # )

  op.create_table(
     "users",
     sa.Column("Email",sa.String(100),nullable=False,unique=True),
     sa.Column("Password",sa.String(100),nullable=False),
     sa.Column("User_id",sa.Integer(),nullable=False,autoincrement=True,unique=True,primary_key=True),
     sa.Column("Email_Verified",sa.Boolean(),nullable=False),
     sa.Column("URL",sa.String(255),nullable=False),
     mysql_charset="utf8mb4",
     mysql_collate="utf8mb4_0900_as_cs"
  )
def downgrade():
    op.drop_table("users")


