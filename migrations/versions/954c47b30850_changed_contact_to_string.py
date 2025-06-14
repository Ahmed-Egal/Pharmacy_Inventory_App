"""Changed contact to string

Revision ID: 954c47b30850
Revises: ce301cdf548b
Create Date: 2025-05-22 13:57:51.262940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '954c47b30850'
down_revision = 'ce301cdf548b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('suppliers', schema=None) as batch_op:
        batch_op.alter_column('contact',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=30),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('suppliers', schema=None) as batch_op:
        batch_op.alter_column('contact',
               existing_type=sa.String(length=30),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
