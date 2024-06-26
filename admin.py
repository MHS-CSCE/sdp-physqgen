"""
Last Modified: May 14, 2024
"""

from os.path import join

from qtpy.QtWidgets import QApplication

from physqgen.admin import AdminView
from physqgen.generator.config import registerConfig


def runAdminApp() -> None:
    registerConfig(join(".", "configs"))
    # import config after creating it
    from physqgen.generator.config.session import appConfig

    adminapp = QApplication()

    view = AdminView(appConfig)
    view.show()

    adminapp.exec()

if __name__ == "__main__":
    runAdminApp()
