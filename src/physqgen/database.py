from sqlite3 import connect
from typing import Iterable

def createQuestionDatabaseTable(databasePath: str, question_type_name: str, question_variables: Iterable[str]) -> None:
    """Creates a table for a question type."""
    # get cursor object
    with connect(databasePath) as connection:
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
            IMAGE_PATH CHAR NOT NULL,
            CORRECT_RANGE FLOAT NOT NULL,
            {" CHAR,".join([variable.upper() for variable in question_variables]) + " CHAR"}
        )'''

        cursor.execute(sql)
    # shouldn't be necessary, but is.
    connection.close()
    return

def createVariableTable(databasePath: str) -> None:
    """Creates the table used to store all variable data"""

    with connect(databasePath) as conn:
        cursor = conn.cursor()

        sql = '''CREATE TABLE VARIABLES(
            VARIABLE_UUID CHAR NOT NULL PRIMARY KEY,
            NAME CHAR NOT NULL,
            VALUE FLOAT NOT NULL,
            UNITS CHAR NOT NULL,
            DISPLAY_NAME CHAR NOT NULL,
            DECIMAL_PLACES NOT NULL
        )'''

        cursor.execute(sql)
    # just in case
    conn.close()
    return

