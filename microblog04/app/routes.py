from flask import render_template, flash, redirect, url_for
from app import app
#from app.models import Course
from app import models
import json

def getExcel(path):
    return json.load(open("/Users/Astrid/project1/test.json", "r"))

@app.route('/')
@app.route('/index')
def index():
    Course = {'cTitle': 'Some'}
    Courses = Course.query.all()
    return render_template('index.html', title='Home',  myDat=Courses)

@app.route('/show_courses/')
def show_courses():
    Courses = Course.query.all()
    return render_template('index.html', title='Home',  myDat=Courses)

@app.route('/upload_spreasheet/')
def upload_spreasheet():
    return Courses


