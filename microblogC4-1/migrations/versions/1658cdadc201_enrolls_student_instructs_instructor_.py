"""Enrolls Student Instructs Instructor Course

Revision ID: 1658cdadc201
Revises: 
Create Date: 2020-05-24 01:33:59.599065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1658cdadc201'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('Classroom', sa.String(length=32), nullable=True),
    sa.Column('Course_code', sa.String(length=32), nullable=True),
    sa.Column('session_ID', sa.String(length=32), nullable=False),
    sa.Column('Course_title', sa.String(length=128), nullable=True),
    sa.Column('Credits', sa.Integer(), nullable=True),
    sa.Column('Format', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('session_ID')
    )
    op.create_index(op.f('ix_course_Classroom'), 'course', ['Classroom'], unique=False)
    op.create_index(op.f('ix_course_Course_code'), 'course', ['Course_code'], unique=False)
    op.create_index(op.f('ix_course_session_ID'), 'course', ['session_ID'], unique=True)
    op.create_table('instructor',
    sa.Column('TID', sa.Integer(), nullable=False),
    sa.Column('Tname', sa.String(length=128), nullable=True),
    sa.Column('Temail', sa.String(length=300), nullable=True),
    sa.Column('Address', sa.Text(), nullable=True),
    sa.Column('Dpt', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('TID')
    )
    op.create_table('student',
    sa.Column('SID', sa.Integer(), nullable=False),
    sa.Column('Sname', sa.String(length=128), nullable=True),
    sa.Column('Semail', sa.String(length=300), nullable=True),
    sa.Column('Address', sa.Text(), nullable=True),
    sa.Column('Dpt', sa.String(length=32), nullable=True),
    sa.Column('GradDate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('SID')
    )
    op.create_table('Enrolls',
    sa.Column('SID', sa.Integer(), nullable=False),
    sa.Column('session_ID', sa.Integer(), nullable=False),
    sa.Column('Status', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['SID'], ['student.SID'], ),
    sa.ForeignKeyConstraint(['session_ID'], ['course.session_ID'], ),
    sa.PrimaryKeyConstraint('SID', 'session_ID')
    )
    op.create_table('Instructs',
    sa.Column('TID', sa.Integer(), nullable=False),
    sa.Column('session_ID', sa.Integer(), nullable=False),
    sa.Column('PrimaryTeach', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['TID'], ['instructor.TID'], ),
    sa.ForeignKeyConstraint(['session_ID'], ['course.session_ID'], ),
    sa.PrimaryKeyConstraint('TID', 'session_ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Instructs')
    op.drop_table('Enrolls')
    op.drop_table('student')
    op.drop_table('instructor')
    op.drop_index(op.f('ix_course_session_ID'), table_name='course')
    op.drop_index(op.f('ix_course_Course_code'), table_name='course')
    op.drop_index(op.f('ix_course_Classroom'), table_name='course')
    op.drop_table('course')
    # ### end Alembic commands ###
