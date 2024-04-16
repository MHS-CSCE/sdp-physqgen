from json import load
from os.path import join

from qtpy.QtWidgets import QApplication

from physqgen import AdminView, Config


def runAdminApp() -> None:
    adminapp = QApplication()

    # get config on run
    with open(join(".", "configs", "active_config.json")) as file:
        with open(join(".", "configs", load(file)["activeConfigName"])) as configFile:
            config = Config.fromFile(load(configFile))

    view = AdminView(config)
    view.show()

    adminapp.exec()

if __name__ == "__main__":
    runAdminApp()