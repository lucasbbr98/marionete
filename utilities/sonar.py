import io
import os
from subprocess import Popen, PIPE
from utilities.files import copy_file_from_to
from configs import ROOT_DIR
import requests


def setup_sonar_report(destination_path, key):
    try:
        ok = create_sonar_project(key)
        if not ok:
            return False

        copy_sonar_template(destination_path)
        rewrite_sonar_key(destination_path, key)
        create_sonar_project(key)
        run_sonar_analysis(destination_path)

        return True
    except Exception:
        return False


def create_sonar_project(key):
    try:
        response = requests.post('http://localhost:9000/api/projects/create',
                          data={'name': key, 'project': key, 'visibility': 'public'})

        if response.ok or response.status_code == 400:
            return True

        return False
    except Exception:
        return False


def copy_sonar_template(destination_path):
    src = os.path.join(ROOT_DIR, 'static/files/sonar-project.properties')
    dest = os.path.join(destination_path, 'sonar-project.properties')
    copy_file_from_to(src, dest)


def rewrite_sonar_key(destination_path, key):
    # Read in the file
    sonar_config = os.path.join(destination_path, 'sonar-project.properties')
    with open(sonar_config, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('my_project_key', key)

    # Write the file out again
    with open(sonar_config, 'w') as file:
        file.write(filedata)


def run_sonar_analysis(destination_path):
    original = os.getcwd()              # Original directory
    try:
        os.chdir(destination_path)      # Execute cmd in project ROOT_DIR
        result = Popen(['sonar-scanner'], stdout=PIPE, shell=True, env=os.environ.copy())
        for line in io.TextIOWrapper(result.stdout, encoding="utf-8"):
            print(line)
        os.chdir(original)              # Get back to our original directory
    except Exception:
        pass
    finally:
        os.chdir(original)