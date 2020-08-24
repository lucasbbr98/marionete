import os
import subprocess


def install_venv(destination_path):

    original = os.getcwd()  # Original directory
    success = False
    try:
        os.chdir(destination_path)  # Execute cmd in project ROOT_DIR
        if not os.path.exists('venv'):
            code = subprocess.check_call(['virtualenv', 'venv'])
            if code != 0:
                success = False
            activate_this = os.path.join('venv', 'Scripts', 'activate_this.py')
            with open(activate_this) as file_:
                exec(file_.read(), dict(__file__=activate_this))
            code = subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
            if code == 0:
                success = True
    except Exception:
        success = False
    finally:
        os.chdir(original)

    return success


if __name__ == '__main__':
    path = r'C:\Projects\DevOps\Projects\llo'
    install_venv(path)