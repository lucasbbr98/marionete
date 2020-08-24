from flask import Blueprint


web = Blueprint('web', __name__)


@web.route('/', methods=['GET'])
def upload_file():
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