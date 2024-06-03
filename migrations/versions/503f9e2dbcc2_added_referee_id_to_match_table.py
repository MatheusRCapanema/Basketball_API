"""Added referee_id to match table

Revision ID: 503f9e2dbcc2
Revises: 4ec4240ae355
Create Date: 2024-06-02 21:17:27.220489

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '503f9e2dbcc2'
down_revision = '4ec4240ae355'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('location', schema=None) as batch_op:
        batch_op.alter_column('stadium_name',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('city',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('capacity',
               existing_type=mysql.INTEGER(),
               nullable=True)

    with op.batch_alter_table('match', schema=None) as batch_op:
        batch_op.add_column(sa.Column('referee_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['referee_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('match', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('referee_id')

    with op.batch_alter_table('location', schema=None) as batch_op:
        batch_op.alter_column('capacity',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('city',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('stadium_name',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###
