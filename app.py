from flask import Flask
from flask_wtf import CSRFProtect
from configs import UPLOAD_FOLDER, MAX_CONTENT_LENGTH, SECRET_KEY
from web.api import api
from web.routes import web

# General configs
app = Flask(__name__,  static_folder='static')
csrf = CSRFProtect()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = SECRET_KEY
csrf.init_app(app) # Compliant

# Blueprints
app.register_blueprint(api)
app.register_blueprint(web)

