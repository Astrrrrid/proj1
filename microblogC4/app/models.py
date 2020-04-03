from datetime import datetime
from app import db


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Classroom = db.Column(db.String(32), index=True, unique=False)
    Course_code = db.Column(db.String(32), index=True, unique=True)
    Course_title = db.Column(db.String(128))
    Credits = db.Column(db.Integer)
    Instructor = db.Column(db.String(128))
    Format = db.Column(db.String(32))

    

    def __repr__(self):
        return '<Course {}>'.format(self.Course_title)


