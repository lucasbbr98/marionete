import os
from subprocess import Popen, PIPE
from io import TextIOWrapper


def run_cmd(cmd, root_dir=''):
    original = os.getcwd()  # Original directory
    success = False
    try:
        if root_dir and root_dir != '':
            os.chdir(root_dir)  # Execute cmd in project new ROOT_DIR

        result = Popen([cmd], stdout=PIPE, shell=True, env=os.environ.copy())
        for line in TextIOWrapper(result.stdout, encoding="utf-8"):
            print(line)
        os.chdir(original)  # Get back to our original directory
        success = True
    except Exception:
        pass
    finally:
        os.chdir(original)
    return success