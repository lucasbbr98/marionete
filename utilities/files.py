import os
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
from shutil import copyfile
from configs import ROOT_DIR


def create_folder(root_path, new_folder_name):
    try:
        app_path = os.path.join(root_path, new_folder_name)
        Path(app_path).mkdir(parents=True, exist_ok=True)
        return app_path
    except Exception:
        return None


def unzip_file_to(file, destination_path):
    try:
        MUST_HAVE_FILES = ['main.py', 'wsgi.py', 'requirements.txt']
        b = BytesIO(file.read())
        zip_file = ZipFile(b, 'r')
        if not set(zip_file.namelist()).issubset(MUST_HAVE_FILES):
            raise FileNotFoundError(f'App zip must have: {", ".join(MUST_HAVE_FILES)}')

        with zip_file:
            zip_file.extractall(destination_path)

        venv_bat_path = os.path.join(ROOT_DIR, 'static/files/build_venv.bat')
        copy_file_from_to(venv_bat_path, os.path.join(destination_path, 'build_venv.bat'))
        return True
    except Exception:
        return False


def copy_file_from_to(src, dest):
    copyfile(src, dest)


