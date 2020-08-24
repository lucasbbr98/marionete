import os
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
from flask import Blueprint, request, redirect, flash
from werkzeug.utils import secure_filename
from utilities.validators import allowed_file
from app import app


app_create = Blueprint('app_create', __name__)


@app_create.route('/', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'name' not in request.form.keys() or 'file' not in request.files or request.files['file'].filename == '':
                flash('No file part')
                return redirect(request.url)

            name = secure_filename(request.form['name'])
            name.replace('.zip', '')
            if not name or name == '':
                flash('Invalid name')
                return redirect(request.url)

            file = request.files['file']
            if file and allowed_file(file.filename):
                b = BytesIO(file.read())
                with ZipFile(b, 'r') as zip:
                    app_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
                    Path(app_path).mkdir(parents=True, exist_ok=True)
                    zip.extractall(app_path)
                return 'Ok'

    except Exception as e:
        print(e)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=text placeholder="Nome app" name="name">
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''