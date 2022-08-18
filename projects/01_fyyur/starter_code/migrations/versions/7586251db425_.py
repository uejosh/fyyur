"""empty message

Revision ID: 7586251db425
Revises: 2bcb8f3731ac
Create Date: 2022-08-15 03:26:25.586947

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7586251db425'
down_revision = '2bcb8f3731ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.alter_column('artist', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artist', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artist', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artist', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artist', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('artist', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artist', 'website',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('artist', 'seeking_venue',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('artist', 'seeking_description',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.add_column('show', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('venue', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.alter_column('venue', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venue', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venue', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venue', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venue', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venue', 'website',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('venue', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('venue', 'seeking_description',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('venue', 'genres',
               existing_type=postgresql.BYTEA(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'genres',
               existing_type=postgresql.BYTEA(),
               nullable=False)
    op.alter_column('venue', 'seeking_description',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('venue', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('venue', 'website',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('venue', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venue', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venue', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venue', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venue', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.drop_column('venue', 'created_at')
    op.drop_column('show', 'created_at')
    op.alter_column('artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artist', 'seeking_description',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('artist', 'seeking_venue',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('artist', 'website',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('artist', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artist', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('artist', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artist', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artist', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artist', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.drop_column('artist', 'created_at')
    # ### end Alembic commands ###