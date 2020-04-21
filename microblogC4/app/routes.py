from flask import render_template, flash, redirect, url_for
from app import app
from app.models import Course
from app import models
import json
import os


from flask import request
#from werkzeug import secure_filename

from werkzeug.utils import secure_filename

app.config["FILE_UPLOADS"] = "/project1/microblogC4/app/static/files/uploads"


def getExcel(path):
    return json.load(open("/Users/Astrid/project1/test.json", "r"))

@app.route('/')
def index():
    #Course = {'cTitle': 'Some'}

    Courses = Course.query.all()
    return render_template('index.html', title='Home',  myDat=Courses)


@app.route('/show_courses/')
def show_courses():
    Courses = models.Course.query.all()
    return render_template('show_courses.html', title='Course Schedule',  myDat=Courses) #return hello""

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
            return redirect(request.url)
            #return "kk I gotchu yall"
        else:
            print("pls upload a correct file")
            return redirect(request.url)
   return render_template('upload.html')
