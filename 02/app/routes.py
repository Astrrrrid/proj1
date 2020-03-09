from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    course = {'cTitle': 'Miguel'}
    info = [
        {
            'cName': {'cTitle': ''},
            'instructor': '',
            'cID': 100,
            'dayOfWeek': ''
        },
        {
            'name': {'cTitle': ''},
            'instructor': '',
            'cID': 101,
            'dayOfWeek': ''
        }
    ]
    return render_template('index.html', title='Home', student=student, info=info)