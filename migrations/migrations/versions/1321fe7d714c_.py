"""empty message

Revision ID: 1321fe7d714c
Revises: b14b0baee182
Create Date: 2023-10-24 17:34:59.163040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1321fe7d714c'
down_revision = 'b14b0baee182'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('charge_record', schema=None) as batch_op:
        batch_op.drop_index('price')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('charge_record', schema=None) as batch_op:
        batch_op.create_index('price', ['price'], unique=False)

    # ### end Alembic commands ###
