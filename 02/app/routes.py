from flask import render_template
from app import app
import json 

@app.route('/')
@app.route('/index')
def index():
    course = {'cTitle': 'Miguel'}
    myDat = json.load(open("/Users/Astrid/project1/test.json", "r"))
    
    return render_template('index.html', title='Home', course=course, myDat=myDat)