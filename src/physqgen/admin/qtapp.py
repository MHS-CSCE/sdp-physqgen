from json import load
from os.path import join

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QAction, QFrame, QGridLayout, QLabel, QMainWindow,
                            QToolBar, QVBoxLayout, QWidget)

from physqgen.admin.getAdminData import getRelevantQuestionData
from physqgen.app.application import app


# TODO: construct the MainWindow with data from getRelevantQuestionData
class AdminView(QMainWindow):
    """
    Quick and dirty window that contains a view of the data currently stored in the database. Has a reload button to refresh data.\n
    Inherits attributes from QMainWindow.
    """
    def __init__(self) -> None:
        """Initialize widgets with data."""
        super().__init__()

        self.setWindowTitle("Question Completion")

        self.widgets = {}
        
        central = QWidget()
        central.setLayout(QGridLayout())

        self.setCentralWidget(central)

        self.widgets["central"] = central
        
        toolbar = QToolBar("reloadToolbar")
        toolbar.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        toolbar.setMovable(False)

        self.widgets["toolbar"] = toolbar

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        reloadButton = QAction("Reload", self)
        reloadButton.triggered.connect(self.reload)

        toolbar.addAction(reloadButton)

        # toplevel layout is hbox.
        # left container is for student names and emails
        toplevelStudentInfoContainer = QFrame()
        studentTopLevelLayout = QVBoxLayout()
        toplevelStudentInfoContainer.setLayout(studentTopLevelLayout)
        
        central.layout().addWidget(QLabel("Student"), 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        
        # create the question columns on creation. will need a reload to update.
        # determine via number of questions in active config
        with open(app.questionConfig) as configFile:
            # use generateQuestions to interpret it, generating question from it
            configData = load(configFile)
        
        for index, questionConfig in enumerate(configData["questions"]):
            central.layout().addWidget(QLabel(questionConfig["question"]), 0, 2 * index + 1, alignment=Qt.AlignmentFlag.AlignTop)

        self.reload()

        return

    def reload(self) -> None:
        """Reloads the visible data."""
        # clear layouts
        while (layoutItem := self.widgets["central"].layout().takeAt(3)) != None:
            layoutItem.widget().deleteLater()

        # fetch all data
        dynamicData = getRelevantQuestionData()

        for index, data in enumerate(dynamicData.items()):
            name = data[0]
            data = data[1]
            gridLayout: QGridLayout = self.widgets["central"].layout()

            gridLayout.addWidget(QLabel(name), index + 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)

            for columnIndex, questionData in enumerate(data):
                gridLayout.addWidget(QLabel(str(questionData[0])), index + 1, columnIndex + 1, alignment=Qt.AlignmentFlag.AlignLeft)
                gridLayout.addWidget(QLabel(str(questionData[1])), index + 1, columnIndex + 2, alignment=Qt.AlignmentFlag.AlignLeft)
        
        return
