"""courses table

Revision ID: e68b56556a6a
Revises: 
Create Date: 2020-04-03 19:35:14.904643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e68b56556a6a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Classroom', sa.String(length=32), nullable=True),
    sa.Column('Course_code', sa.String(length=32), nullable=True),
    sa.Column('Course_title', sa.String(length=128), nullable=True),
    sa.Column('Credits', sa.Integer(), nullable=True),
    sa.Column('Instructor', sa.String(length=128), nullable=True),
    sa.Column('Format', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_course_Classroom'), 'course', ['Classroom'], unique=False)
    op.create_index(op.f('ix_course_Course_code'), 'course', ['Course_code'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_course_Course_code'), table_name='course')
    op.drop_index(op.f('ix_course_Classroom'), table_name='course')
    op.drop_table('course')
    # ### end Alembic commands ###