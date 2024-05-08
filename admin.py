"""
Last Modified: May 8, 2024
"""

from qtpy.QtWidgets import QApplication

# registers the config on import
from physqgen.admin import AdminView, appConfig


def runAdminApp() -> None:
    adminapp = QApplication()

    view = AdminView(appConfig)
    view.show()

    adminapp.exec()

if __name__ == "__main__":
    runAdminApp()