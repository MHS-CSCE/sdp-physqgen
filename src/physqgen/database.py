from sqlite3 import connect, Connection, Cursor, Row
from physqgen.generator import KinematicsQuestion

def getDatabaseConnection() -> Connection:
    """Fetches database connection. Will create database if it does not exist."""
    # sqlite3 db
    return connect('.\\data\\data.db')

def addQuestionToDatabase(question_type_name: str, question_variables: list[str]) -> None:
    """Creates a table for a question type."""
    # get cursor object
    with getDatabaseConnection() as connection:
        cursor = connection.cursor()

        # creating table for question type
        # don't care about sql injection, is internal use.
        sql = f'''CREATE TABLE {question_type_name.upper()}(
            QUESTION_UUID CHAR NOT NULL PRIMARY KEY,
            FIRST_NAME CHAR NOT NULL,
            LAST_NAME CHAR NOT NULL,
            EMAIL_A CHAR NOT NULL,
            NUMBER_TRIES INT NOT NULL,
            CORRECT BOOL NOT NULL,
            SOLVE_VARIABLE CHAR NOT NULL,
            TEXT CHAR NOT NULL,
            CORRECT_RANGE FLOAT NOT NULL,
            {" FLOAT,".join([variable.upper() for variable in question_variables]) + " FLOAT"}
        )'''

        cursor.execute(sql)

def assignCursorRowFactoryQuestionType(cursor: Cursor, questionType: str, studentInfo: bool = False) -> None:
    """Sets row_factory the correct row factory function based on questionType. Will set the alternate rowfactory that includes all info if studentInfo is True."""
    cursor.row_factory = questionRowFactory
    cursor.questionType = questionType.upper()
    return

def questionAndStudentInfoRowFactory(cursor, rowData: Row):
    """Uses questionRowFactory, but also returns the student data."""
    question = questionRowFactory(cursor, rowData)

    # rowData[1-5] are user data
    # 1 -> firstName
    # 2 -> lastname
    # 3 -> email
    # 4 -> tries
    # 5 -> correct

    return *rowData[2:6], question

def questionRowFactory(cursor: Cursor, rowData: Row):
    """
    Converts a database row to the coresponding question object.\n
    Will raise a ValueError if cursor's questionType is not set, use assignCursorRowFactoryQuestionType on the cursor.\n
    Needs to be updated when adding new question types.
    """
    questionType = cursor.questionType

    if questionType == "KINEMATICS":
        id = rowData[0]
        solveVar = rowData[6]
        text = rowData[7]
        correctRange = rowData[8]
        variableValues = (var for var in rowData[9:])

        return KinematicsQuestion.fromDatabase(
            solveVariable=solveVar,
            text=text,
            variableValues=variableValues,
            correctRange=correctRange,
            id=id
        )
    else:
        raise ValueError(f"Cursor's questionType attribute has unsupported value '{questionType}'.")

def createDataBaseFromBlank() -> None:
    """Expects the database file not to exist."""
    # added
    # TODO: add attribute, regen database (maybe type()?)
    addQuestionToDatabase(KinematicsQuestion.questionName(), [var.name for var in KinematicsQuestion.variables])


if __name__ == "__main__":
    # if this is run directly, it will regenerate the database from blank.
    createDataBaseFromBlank()
