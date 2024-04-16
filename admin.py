from json import load
from os.path import join

from qtpy.QtWidgets import QApplication

from physqgen.admin import AdminView
from physqgen.app.application import create_app
from physqgen.generator.config import Config

if __name__ == "__main__":
    adminapp = QApplication()
    app = create_app()

    # get config on run
    with open(join(".", "configs", "active_config.json")) as file:
        with open(join(".", "configs", load(file)["activeConfigName"])) as configFile:
            app.questionConfig = Config.fromFile(load(configFile))

    view = AdminView(app)
    view.show()

    adminapp.exec()
