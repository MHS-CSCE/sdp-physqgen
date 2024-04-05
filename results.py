from qtpy.QtWidgets import QApplication

from physqgen.admin.qtapp import AdminView

if __name__ == "__main__":
    app = QApplication()
    view = AdminView()
    view.show()

    exit(app.exec())
