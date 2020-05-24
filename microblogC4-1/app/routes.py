from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.models import Course, Enrolls, Student, Instructs, Instructor
from app import models
import json
import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

from flask import request
#from werkzeug import secure_filename

from werkzeug.utils import secure_filename

app.config["FILE_UPLOADS"] = "/Users/Astrid/project1/microblogC4/app/static/files/uploads"


def getExcel(path):
    return json.load(open("/Users/Astrid/project1/test2.json", "r"))

@app.route('/')
def index():
    #Course = {'cTitle': 'Some'}

    Courses = Course.query.all()
    return render_template('index.html', title='Home',  myDat=Courses)


@app.route('/show_courses/')
def show_courses():
    Courses = models.Course.query.all()
    return render_template('show_courses.html', title='Course Schedule',  myDat=Courses) 

@app.route('/upload_spreasheet/')
def upload_spreasheet():
    return Courses


def allowed_table(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() == "XLSX":
        return True
    else:
        return False


@app.route('/upload')
def upload_file2():
   return render_template('upload.html')
	
#@app.route('/uploader', methods = ['GET', 'POST'])
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      if request.files:
        f = request.files['file']
        if f.filename == "":
            print("No filename")
            return redirect(request.url)
        if allowed_table(f.filename):
            ffilename = secure_filename(f.filename)
            f.save(os.path.join(app.config["FILE_UPLOADS"], ffilename))
            print("table saved")
            pddf=pd.read_excel(app.config["FILE_UPLOADS"]+'/'+ffilename)
            dictdf = pddf.to_dict('records')
            baseName = os.path.splitext(os.path.basename(ffilename))[0]
            json.dump(dictdf, open(app.config["FILE_UPLOADS"]+'/'+ baseName +".json", "w"), sort_keys=True, default=str)
            print("dumped to a json file")
            update(baseName)
            #return redirect(request.url)
            Courses = models.Course.query.all()
            return render_template('show_courses.html', title='the new one',  myDat=Courses) 
        else:
            print("pls upload a correct file")
            return redirect(request.url)
   return render_template('upload.html')


def update(baseName):
    oldDF = models.Course.query.all()
    newDF = json.load(open(app.config["FILE_UPLOADS"]+'/'+ baseName +".json", "r"))
    for oldRecord in oldDF:
        for newRecord in newDF:
            if oldRecord.session_ID == newRecord['SessionID'] and oldRecord != newRecord:
                db.session.delete(oldRecord)
                alternate = Course(Course_title=newRecord['CourseTitle'],Classroom=newRecord['Classroom'],Course_code=newRecord['CourseCode'],Credits=newRecord['Cr'],
                Format=newRecord['CourseFormat'], session_ID=newRecord['SessionID'])
                db.session.add(alternate)
                db.session.commit()
                





#function update: loop over the list of dict from json file, for each row use the course Code to search for the matching courseid, update the row with json file, do a test by direct to show course


