def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'zip'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
