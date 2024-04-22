from physqgen.database import createQuestionDatabaseTable, createVariableTable
from physqgen.generator import KinematicsQuestion

from .constants import DATABASEPATH


def createDataBaseFromBlank() -> None:
    """Expects the database file not to exist."""
    # Existing Questions
    createQuestionDatabaseTable(DATABASEPATH, "KinematicsQuestion", (var for var in KinematicsQuestion.POSSIBLE_VARIABLES))
    createVariableTable(DATABASEPATH)
    return
