"""create otp table

Revision ID: 42196d154b41
Revises: c366d69495b6
Create Date: 2026-08-29 23:31:50.308082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42196d154b41'
down_revision: Union[str, Sequence[str], None] = 'c366d69495b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # op.create_table(
    #     "otp",
    #     sa.Column("OTP", sa.String(255), nullable=True),
    #     sa.Column("User_id", sa.Integer(), nullable=True),
    #     sa.Index("OTP", "User_id"),
    #     sa.ForeignKeyConstraint(
    #         ["User_id"],
    #         ["users.User_id"],
    #         name="otp_ibfk_1",
    #     ),
    #     mysql_charset="utf8mb4",
    #     mysql_collate="utf8mb4_0900_ai_ci",
    # )

  op.create_table(
     "otp",
     sa.Column("OTP",sa.Integer(),nullable=False),
     sa.Column("User_id",sa.Integer,nullable=False),
     sa.ForeignKeyConstraint(
        ["User_id"],
        ["users.User_id"]
     ),
     sa.UniqueConstraint("User_id"),
     mysql_charset="utf8mb4",
     mysql_collate="utf8mb4_0900_as_cs"


  )
def downgrade():
    op.drop_table("otp")