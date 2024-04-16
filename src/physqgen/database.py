from sqlite3 import connect
from os.path import join
from collections.abc import Iterable

from physqgen.generator import KinematicsQuestion

# the path to the sqlite3 database
DATABASEPATH = join('.', 'data', 'data.db')

def addQuestionToDatabase(question_type_name: str, question_variables: Iterable[str]) -> None:
    """Creates a table for a question type."""
    # get cursor object
    with connect(DATABASEPATH) as connection:
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
    # shouldn't be necessary, but is.
    connection.close()
    return

def createDataBaseFromBlank() -> None:
    """Expects the database file not to exist."""
    # Existing Questions
    addQuestionToDatabase("KinematicsQuestion", (var for var in KinematicsQuestion.POSSIBLE_VARIABLES))
    return
