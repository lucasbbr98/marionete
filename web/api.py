from flask import Blueprint, request, redirect, flash
from werkzeug.utils import secure_filename
from utilities.validators import allowed_file
from api.create import create_new_app


api = Blueprint('api', __name__)


@api.route('/', methods=['POST'])
def upload_file():
    try:
        if 'name' not in request.form.keys() or 'file' not in request.files or request.files['file'].filename == '':
            flash('No file part')
            return redirect(request.url)

        name = secure_filename(request.form['name'])
        name.replace('.zip', '')
        if not name or name == '':
            flash('Invalid project name')
            return redirect(request.url)

        file = request.files['file']
        if not file or not allowed_file(file.filename):
            flash('Invalid filename')
            return redirect(request.url)

        ok = create_new_app(name, file)
        if not ok:
            flash('Houve um erro ao tentar criar o seu app')
            return redirect(request.url)

        return 'Ok'

    except Exception as e:
        return f'FATAL ERROR: {e}'