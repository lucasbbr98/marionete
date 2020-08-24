from configs import UPLOAD_FOLDER
from utilities.files import create_folder, unzip_file_to
from utilities.sonar import setup_sonar_report
from utilities.venv import install_venv


def create_new_app(name, zip_file):
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



        #TODO: waitress-serve
        return True

    except Exception:
        return False
