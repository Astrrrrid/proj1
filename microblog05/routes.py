from flask import Flask, render_template, request, jsonify, redirect, make_response
from app import app
from werkzeug import secure_filename
import


app.config["FORM_UPLOADS"] = "/mnt/c/wsl/projects/pythonise/tutorials/flask_series/app/app/static/img/uploads" #tbd
app.config["ALLOWED_EXTENSIONS"] = ["XLSX"]


def allowed_file(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False




@app.route("/")
def index():

    return render_template("app/static/index.html")

app = Flask(__name__)
app.config["FILE_UPLOADS"] = "somepath/somepath"


@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'


		
if __name__ == '__main__':
   app.run(debug = True)