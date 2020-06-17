from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.models import Course, Enrolls, Student, Instructs, Instructor, Conflicts, colNames
from app import models
import json
import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import requests, hashlib, time
from collections import defaultdict
import urllib

from flask import request
#from werkzeug import secure_filename

from werkzeug.utils import secure_filename

parse= urllib.parse

app.config["FILE_UPLOADS"] = "/Users/Astrid/project1/microblogC4/app/static/files/uploads"

tablesAndTheirPrimaries = {"Instructor": "TID", "Student": "SID", "Course": "session_ID"}


def getExcel(path):
    return json.load(open("/Users/Astrid/project1/test2.json", "r"))

@app.route('/')
@app.route('/index')
def index():
    #Course = {'cTitle': 'Some'}

    Courses = Course.query.all()
    return render_template('index.html', title='Home',  myDat=Courses)


@app.route('/show/')
def show_table():
    #Courses = models.Course.query.all()
    
        
    return render_template('show.html', title='Table list')

@app.route('/show/courses/')
def show_courses():
    Courses = models.Course.query.all()
    return render_template('show_courses.html', title='the new one',  myDat=Courses)

@app.route('/show/students/')
def show_students():
    Students = models.Student.query.all()
    return render_template('show_students.html', title='the new one',  myDat=Students)

@app.route('/show/instructors/')
def show_instructors():
    Instructors = models.Instructor.query.all()
    return render_template('show_instructors.html', title='the new one',  myDat=Instructors)



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

def allowed_csv_table(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() == "CSV":
        return True
    else:
        return False


@app.route('/upload')
def upload_file2():
   return render_template('upload.html')
	
#@app.route('/uploader', methods = ['GET', 'POST'])
@app.route('/uploaderOld', methods=['GET', 'POST'])
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
            updateCourse(dictdf) # !!! this is the new function to update a course table

            baseName = os.path.splitext(os.path.basename(ffilename))[0]
            json.dump(dictdf, open(app.config["FILE_UPLOADS"]+'/'+ baseName +".json", "w"), sort_keys=True, default=str)
            print("dumped to a json file")
            #update(baseName)
            #return redirect(request.url)

            Courses = models.Course.query.all()
            return render_template('show_courses.html', title='the new one',  myDat=Courses) 
        else:
            print("pls upload a correct file")
            return redirect(request.url)
   return render_template('upload.html')

#function update: loop over the list of dict from json file, for each row use the course Code to search for the matching courseid, update the row with json file, do a test by direct to show course

def update(baseName):
    oldDF = models.Course.query.all()
    #oldIDs = models.Course.query.session_ID()
    newDF = json.load(open(app.config["FILE_UPLOADS"]+'/'+ baseName +".json", "r"))
    oldSessionIDs = []
    for oldRecord in oldDF:
        oldSessionIDs.append(oldRecord.session_ID)
    for oldRecord in oldDF:
        for newRecord in newDF:
            if oldRecord.session_ID == newRecord['SessionID'] and oldRecord != newRecord:
                db.session.delete(oldRecord)
                alternate = Course(Course_title=newRecord['CourseTitle'],Classroom=newRecord['Classroom'],Course_code=newRecord['CourseCode'],Credits=newRecord['Cr'],
                Format=newRecord['CourseFormat'], session_ID=newRecord['SessionID'])
                db.session.add(alternate)
                db.session.commit()
            elif not(newRecord['SessionID'] in oldSessionIDs): # in oldIDs

                new = Course(Course_title=newRecord['CourseTitle'],Classroom=newRecord['Classroom'],Course_code=newRecord['CourseCode'],Credits=newRecord['Cr'],
                Format=newRecord['CourseFormat'], session_ID=newRecord['SessionID'])
                db.session.add(new)
                db.session.commit()

@app.route('/uploader', methods=['GET', 'POST'])
def updateCSV1(primary="SessionID"):
    if request.method == 'POST':
      if request.files:
        f = request.files['file']
        if f.filename == "":
            print("No filename")
            return redirect(request.url)
        if allowed_csv_table(f.filename):
            ffilename = secure_filename(f.filename)
            f.save(os.path.join(app.config["FILE_UPLOADS"], ffilename))
            print("table saved")
            #pddf=pd.read_excel(app.config["FILE_UPLOADS"]+'/'+ffilename)

            mydf=pd.read_csv(app.config["FILE_UPLOADS"]+'/'+ffilename, delimiter=',')
            Dicts = mydf.to_dict('records')

            
            primary="session_ID"
            for k in tablesAndTheirPrimaries:
                if k in ffilename:
                    primary=tablesAndTheirPrimaries[k]
            
            updateCSV2(primary, Dicts) # !!! this is the new function to update a course table

           

            #Courses = models.Course.query.all()

            for v in tablesAndTheirPrimaries:
                if primary==v:
                    modifiedTable = getattr(models,get_key(tablesAndTheirPrimaries,v)).query.all()
            return render_template('show.html', title='the new one')
            '''if get_key(tablesAndTheirPrimaries,v)=="Course":
                    return show_courses()
                elif get_key(tablesAndTheirPrimaries,v)=="Student":
                    return show_students()
                elif get_key(tablesAndTheirPrimaries,v)=="Instructor":
                    return render_template('show_instructors.html', title='the new one',  myDat=modifiedTable)'''
            


        else:
            print("pls upload a correct file")
            return redirect(request.url)
    return render_template('upload.html')



def updateCSV2(primary, Dicts):
    
    for x in Dicts:
        match = x[primary]
        if primary=="session_ID":
            found = Course.query.filter_by(session_ID=match)
        elif primary=="SID":
            found = Student.query.filter_by(SID=match)
        elif primary=="TID":
            found = Instructor.query.filter_by(TID=match)
        if found.count()>0:
            obj=found[0]
            for k,v in x.items():
                setattr(obj, k, v)
            db.session.add(obj)
            db.session.commit()
        else:
            for k,v in tablesAndTheirPrimaries:
                if v==primary:
                    newOne=getattr(models,k)
            
            for k, v in x.items():
                setattr(newOne, k,v)
            db.session.add(newOne)
            db.session.commit()

def get_key(my_dict,val): 
    for key, value in my_dict.items(): 
         if val == value: 
             return key

"""def updateCourse(dictdf, primary="SessionID"):
    
    Dicts = dictdf
    
    for x in Dicts:
        match = x[primary]
        found = Course.query.filter_by(session_ID=match)
        if found.count()>0:
            aCourse=found[0]
            for k,v in x.items():
                setattr(aCourse, k, v)
            db.session.add(aCourse)
            db.session.commit()
        else:
            new = Course(Course_title=x['CourseTitle'],Classroom=x['Classroom'],Course_code=x['CourseCode'],Credits=x['Cr'],
            Format=x['CourseFormat'], session_ID=x['SessionID'])
            db.session.add(new)
            db.session.commit()"""
                


#def newFunction():
    #df = pd.read_csv('students.csv', delimiter=',')
    #LIST = [list(row) for row in df.values]
#for row in table:
    #T = getTable("Course")
    
#for key in row.keys():
     #if there is conflicts to update
     #pass
#else:
#   newrow = T(row)



@app.route('/downloadTable/<tname>')
def downloadTable(tname=None):
    
    thoseTables=["Course", "Enrolls", "Instructs", "Student", "Instructor", "Conflicts"]
    if any(name == tname for name in thoseTables):
        uniqueStr = hashlib.md5((str(time.time())+"anotherString").encode("utf8")).hexdigest()
        dbList = getattr(models, tname).query.all()

            
        listS = defaultdict(list)
            
        for row in dbList: 
            for col in colNames[tname]:
                listS[col].append(getattr(row, col))
       
        # app.static_path <-- this is local file folder
        # app.static_url <--download link prefix
         #jsfile = os.path.join(app.static_path, "hellow.js")

         
            #df2.to_csv('static/tmp/Students{}.csv'.format(uniqueStr),index=False)

        df2 = pd.DataFrame(listS)
        path=os.path.join(app.static_folder, tname+'{}.csv'.format(uniqueStr))
        df2.to_csv(path, index=False)
        fileUrl = parse.urljoin(app.static_url_path + '/', tname+'{}.csv'.format(uniqueStr))
        return render_template('download_page.html', title = 'links for csv', tableLink=fileUrl, tableName=tname)

    else:
        return "Sorry <html><head></head><body><p>no such table<p><body></html>"
    

@app.route('/downloadTable/')
def show_downloads():
    return render_template('download_table.html', title = 'links for tables') 

