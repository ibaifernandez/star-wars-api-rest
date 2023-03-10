"""empty message

Revision ID: 53c05fdabc36
Revises: 8d1b402c9596
Create Date: 2023-02-25 02:17:16.187722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53c05fdabc36'
down_revision = '8d1b402c9596'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehicles',
    sa.Column('vehicle_id', sa.Integer(), nullable=False),
    sa.Column('vehicle_name', sa.String(length=120), nullable=False),
    sa.Column('vehicle_url', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('vehicle_id'),
    sa.UniqueConstraint('vehicle_url')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vehicles')
    # ### end Alembic commands ###
