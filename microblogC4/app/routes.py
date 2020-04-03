from flask import render_template, flash, redirect, url_for
from app import app
import json



@app.route('/')
@app.route('/index')
@app.route('/http://mydom/upload_spreasheet/')



def index():
    Course = {'cTitle': 'Some'}
    Courses = Course.query.all()
    return render_template('index.html', title='Home',  myDat=Courses)

def show_courses():
    Courses = Course.query.all()
    return render_template('index.html', title='Home',  myDat=Courses)

def upload_spreasheet():
    return Courses

def getExcel(path):
    return json.load(open("/Users/Astrid/project1/test.json", "r"))
