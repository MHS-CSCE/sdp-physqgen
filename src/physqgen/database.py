from sqlite3 import connect, Connection
from physqgen.generator import KinematicsQuestion

def getDatabaseConnection() -> Connection:
    """Fetches database connection. Will create database if it does not exist."""
    # create sqlite3 db
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
            ANSWER FLOAT NOT NULL,
            {" FLOAT,".join([variable.upper() for variable in question_variables]) + " FLOAT"}
        )'''

        cursor.execute(sql)

def createDataBaseFromBlank() -> None:
    """Expects the database file not to exist."""
    # added
    # TODO: add attribute, regen database (maybe type()?)
    # TODO: get enum value names
    addQuestionToDatabase(KinematicsQuestion.questionGroupName(), [var.name for var in KinematicsQuestion.variables])


if __name__ =="__main__":
    createDataBaseFromBlank()
