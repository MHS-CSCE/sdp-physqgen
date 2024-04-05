from json import load
from os.path import join

from qtpy.QtWidgets import QApplication

from physqgen.admin import AdminView
from physqgen.app.application import create_app

if __name__ == "__main__":
    adminapp = QApplication()
    app = create_app()

    # get config on run
    with open(join(".", "configs", "active_config.json")) as file:
        app.questionConfig = join(".", "configs", load(file)["activeConfigName"])

    view = AdminView(app)
    view.show()

    adminapp.exec()
