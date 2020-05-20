from datetime import datetime
from app import db


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Classroom = db.Column(db.String(32), index=True, unique=False)
    Course_code = db.Column(db.String(32), index=True, unique=False)
    session_ID = db.Column(db.Integer, index = True, unique = True)# then migrate, add a new col in spreadsheet, check the existing code read the xl function, check update(match code+seesionID


    Course_title = db.Column(db.String(128))
    Credits = db.Column(db.Integer)
    Instructor = db.Column(db.String(128))
    Format = db.Column(db.String(32))

    

    def __repr__(self):
        return '<Course {}>'.format(self.Course_title)

class Student(db.Model):
    SID = db.Column(db.Integer, primary_key=True)
    Sname = db.Column(db.String(128))
    

class Instructor(db.Model):
    TID = db.Column(db.Integer, primary_key=True)
    Tname = db.Column(db.String(128))

