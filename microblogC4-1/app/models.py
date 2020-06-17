from datetime import datetime
from app import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


colNames = {"Student":["SID", "Sname", "Semail", "Address", "Dpt", "GradDate"], "Course":["Classroom","Course_code", "session_ID", "Course_title", "Credits", "Format"],
    "Instructor":["TID", "Tname", "Temail", "Address", "Dpt"],
    "Conflicts":["session_ID","Block", "TimeStart","Duration", "Mon","Tue","Wed", "Thu", "Fri", "Classroom","Instructor"],
    "Enrolls":["SID", "session_ID", "Status"],
    "Instructs":["TID", "session_ID", "PrimaryTeach"]} 


'''Enrolls = db.Table('Enrolls',
    db.Column('SID', db.Integer, db.ForeignKey('student.SID'), primary_key=True),
    db.Column('session_ID', db.String(32), db.ForeignKey('course.session_ID'), primary_key=True),
    db.Column('Status', db.String(32)) # -- student is on waitlist with a number, or auditing, or registrated with credits
)'''

'''Instructs = db.Table('Instructs',
    db.Column('TID', db.Integer, db.ForeignKey('instructor.TID'), primary_key=True),
    db.Column('session_ID', db.String(32), db.ForeignKey('course.session_ID'), primary_key=True),
    db.Column('PrimaryTeach', db.Boolean, nullable=True, default=False) # -- the host who is in charge of the course and leads all speakers 
)'''

class Instructs(db.Model):
    TID = db.Column(db.Integer, db.ForeignKey('instructor.TID'), primary_key=True)
    session_ID = db.Column(db.String(32), db.ForeignKey('course.session_ID'), primary_key=True)
    PrimaryTeach = db.Column(db.Boolean, nullable=True, default=False) # -- the host who is in charge of the course and leads all speakers
    course = relationship(Course, backref=backref("Instructs", cascade="all, delete-orphan"))
    instructor = relationship(Instructor, backref=backref("Instructs", cascade="all, delete-orphan"))

class Enrolls(db.Model):
    SID = db.Column(db.Integer, db.ForeignKey('student.SID'), primary_key=True)
    session_ID = db.Column(db.String(32), db.ForeignKey('course.session_ID'), primary_key=True)
    Status = db.Column(db.String(32)) # -- student is on waitlist with a number, or auditing, or registrated with credits
    course = relationship(Course, backref=backref("Enrolls", cascade="all, delete-orphan"))
    student = relationship(Student, backref=backref("Enrolls", cascade="all, delete-orphan"))


class Course(db.Model):
    #id = db.Column(db.Integer)

    Classroom = db.Column(db.String(32), index=True, unique=False)
    Course_code = db.Column(db.String(32), index=True, unique=False)
    session_ID = db.Column(db.String(32), index = True, unique = True, primary_key=True) # then migrate, add a new col in spreadsheet, check the existing code read the xl function, check update(match code+seesionID

    Course_title = db.Column(db.String(128))
    Credits = db.Column(db.Integer)
    #Instructor = db.Column(db.String(128))
    Format = db.Column(db.String(32))
    enrollment = db.relationship('Student', secondary=Enrolls, lazy = 'dynamic', backref=db.backref('courses'))
    instruction = db.relationship('Instructor', secondary=Instructs, lazy='dynamic', backref=db.backref('courses'))

    def __repr__(self):
        return '<Course {}>'.format(self.Course_title)


class Student(db.Model):
    SID = db.Column(db.Integer, primary_key=True)
    Sname = db.Column(db.String(128))
    Semail = db.Column(db.String(300))
    Address = db.Column(db.Text)
    Dpt = db.Column(db.String(32))
    GradDate = db.Column(db.DateTime)
    enrollment = db.relationship('Course', secondary=Enrolls, lazy = 'dynamic', backref=db.backref('students'))

class Instructor(db.Model):
    TID = db.Column(db.Integer, primary_key=True)
    Tname = db.Column(db.String(128))
    Temail = db.Column(db.String(300))#required=FALSE

    Address = db.Column(db.Text)
    Dpt = db.Column(db.String(32))
    instruction = db.relationship('Course', secondary=Instructs, lazy='dynamic', backref=db.backref('instructors'))

class Conflicts(db.Model):
    session_ID = db.Column(db.String(32),  db.ForeignKey('course.session_ID'), primary_key=True )
    Block = db.Column(db.Boolean, default=True)
    TimeStart = db.Column(db.Time )#, timezone=False)

    Duration = db.Column(db.Interval)#, second_precision=None, day_precision=None)

    #TimeEnd = db.Column(db.Time, timezone=False)

    Mon = db.Column(db.Boolean, default=False)
    Tue = db.Column(db.Boolean, default=False)
    Wed = db.Column(db.Boolean, default=False)
    Thu = db.Column(db.Boolean, default=False)
    Fri = db.Column(db.Boolean, default=False)
    Classroom = db.Column(db.String(32))
    Instructor = db.Column(db.String(48))




