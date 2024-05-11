from os import remove

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QAction, QFrame, QGridLayout, QLabel, QMainWindow,
                            QToolBar, QVBoxLayout, QWidget)

from physqgen.admin import DATABASEPATH
from physqgen.admin.get_admin_data import getRelevantQuestionData
from physqgen.database import createDatabase
from physqgen.generator import Config


class AdminView(QMainWindow):
    """
    Quick and dirty window that contains a view of the data currently stored in the database. Has a reload button to refresh data.\n
    Inherits attributes from QMainWindow.
    """
    def __init__(self, config: Config) -> None:
        """Initialize widgets with data."""
        super().__init__()

        self.setWindowTitle("Physqgen Administration App")

        self.widgets = {}
        
        central = QWidget()
        central.setLayout(QGridLayout())

        self.setCentralWidget(central)

        self.widgets["central"] = central
        
        toolbar = QToolBar("toolbar")
        toolbar.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        toolbar.setMovable(False)

        # TODO: button to open dropdown to select active config?
        
        self.widgets["toolbar"] = toolbar

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        reloadButton = QAction("Reload", self)
        reloadButton.triggered.connect(self.reload)

        toolbar.addAction(reloadButton)

        emptyDatabaseButton = QAction("Clear All Data", self)
        emptyDatabaseButton.triggered.connect(self.clearDatabase)

        toolbar.addAction(emptyDatabaseButton)

        # toplevel layout is hbox.
        # left container is for student names and emails
        toplevelStudentInfoContainer = QFrame()
        studentTopLevelLayout = QVBoxLayout()
        toplevelStudentInfoContainer.setLayout(studentTopLevelLayout)
        
        central.layout().addWidget(QLabel("Student"), 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        
        # create the question columns on creation. will need a reload to update.
        # determine via number of questions in active config
        self.takeAtLocation = 0
        for index, question in enumerate(config.questionConfigs):
            # counter for where to start removing items
            self.takeAtLocation += 1

            questionType = question.questionType
            central = self.widgets["central"]

            central.layout().addWidget(QLabel(questionType), 0, (2 * index) + 1, alignment=Qt.AlignmentFlag.AlignTop)
            # add number of tries and completed headers
            central.layout().addWidget(QLabel("Submissions"), 1, (2 * index) + 1, alignment=Qt.AlignmentFlag.AlignTop)
            central.layout().addWidget(QLabel("Completed"), 1, (2 * index) + 2, alignment=Qt.AlignmentFlag.AlignTop)

        self.reload()

        return

    def reload(self) -> None:
        """Reloads the visible data."""
        # clear layouts
        # 0 is student label, every group of three after is from a question in config. takeAt (0) + len(questions) * 3 + 1 (so am taking next one)
        while (layoutItem := self.widgets["central"].layout().takeAt(self.takeAtLocation * 3 + 1)) != None:
            layoutItem.widget().deleteLater()

        # fetch all data
        dynamicData = getRelevantQuestionData()

        for index, data in enumerate(dynamicData.items()):
            name = data[0]
            data = data[1]
            gridLayout: QGridLayout = self.widgets["central"].layout()

            gridLayout.addWidget(QLabel(name), index + 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)

            for columnIndex, questionData in enumerate(data):
                # 0 is number of tries
                # 1 is correct
                gridLayout.addWidget(QLabel(str(questionData[0])), index + 2, columnIndex * 2 + 1, alignment=Qt.AlignmentFlag.AlignLeft)
                gridLayout.addWidget(QLabel(str(questionData[1])), index + 2, columnIndex * 2 + 2, alignment=Qt.AlignmentFlag.AlignLeft)
        
        return
    
    def clearDatabase(self) -> None:
        """Deletes any existing database and generates a new blank one."""
        # works, but only if some extra arbitrary closes are added in. They shouldn't be required because of the context managers, but they are.
        remove(DATABASEPATH)
        createDatabase()
        # reload view to show changes
        self.reload()
        return
