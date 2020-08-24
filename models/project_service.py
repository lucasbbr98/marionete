import os
import sys
from subprocess import Popen, PIPE, call, CREATE_NEW_PROCESS_GROUP
import io
from configs import UPLOAD_FOLDER, PROJECTS_ROOT_DIR
from utilities.files import create_folder, unzip_file_to
from utilities.sonar import setup_sonar_report
from utilities.venv import install_venv

# https://www.reddit.com/r/learnpython/comments/3o9qym/open_a_cmd_shell_in_windows_and_issue_commands_to/


class ProjectService:

    @classmethod
    def create(cls, name, zip_file):
        try:
            root_path = UPLOAD_FOLDER
            app_path = create_folder(root_path, name)
            if app_path is None:
                raise FileNotFoundError(f"Não encontrei o caminho: {root_path}/{name}")

            ok = unzip_file_to(zip_file, app_path)
            if not ok:
                raise SystemError("Não consegui deszipar os arquivos enviados")

            setup_sonar_report(app_path, name)
            ok = install_venv(app_path)
            if not ok:
                raise EnvironmentError("Não consegui instalar o venv nesse projeto")

            # TODO: waitress-serve

            # TODO: checar o ping

            # TODO: update db com o pid
            return True

        except Exception:
            return False

    @classmethod
    def stop(cls, name):
        pass

    @classmethod
    def start(cls, name):
        original = os.getcwd()  # Original directory
        success = False
        try:
            destination_path = os.path.join(PROJECTS_ROOT_DIR, name)
            venv_path = os.path.join(destination_path, 'venv', 'Scripts', 'python')
            wsgi_path = os.path.join(destination_path, 'wsgi.py')
            os.chdir(destination_path)  # Execute cmd in project ROOT_DIR

            activate_this = os.path.join(destination_path, 'venv', 'Scripts', 'activate_this.py')
            with open(activate_this) as file_:
                exec(file_.read(), dict(__file__=activate_this))

            result = Popen([venv_path, wsgi_path], shell=True, stdout=PIPE)
            for line in io.TextIOWrapper(result.stdout, encoding="utf-8"):
                print(line)

            os.chdir(original)  # Get back to our original directory
            success = True
        except Exception as e:
            print(e)
        finally:
            os.chdir(original)
        return success


    def ping(cls, name):
        pass

if __name__ == '__main__':
    ps = ProjectService()
    ok = ps.start('llo')
    print(ok)