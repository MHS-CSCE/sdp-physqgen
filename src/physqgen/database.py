from sqlite3 import connect
from typing import Iterator


def executeOnDatabase(databasePath: str, sql: str, replacements: Iterator = ()) -> list:
    """Executes the given sql with the given replacements on the database and returns the results of cursor.fetchall(). This can be used for committing, updating, or fetching."""
    with connect(databasePath) as connection:
        cursor = connection.cursor()
        cursor.execute(sql, replacements)
        results = cursor.fetchall()
    # shouldn't be necessary because of context manager but is
    connection.close()
    return results

def createSessionTable(databasePath: str) -> None:
    """Creates the table for storing persistent Session data."""
    sql = '''CREATE TABLE SESSIONS(
        SESSION_UUID CHAR NOT NULL PRIMARY KEY,
        FIRST_NAME CHAR NOT NULL,
        LAST_NAME CHAR NOT NULL,
        EMAIL CHAR NOT NULL
    )'''
    executeOnDatabase(databasePath, sql)
    return

def createQuestionTable(databasePath: str) -> None:
    """Creates the table for storing persistent data about a question subclass  object."""
    sql = '''CREATE TABLE QUESTIONS(
    QUESTION_UUID CHAR NOT NULL PRIMARY KEY,
    SESSION_UUID CHAR NOT NULL,
    QUESTION_TYPE CHAR NOT NULL,
    ANSWER_VARIABLE_NAME CHAR NOT NULL,
    CORRECT_LEEWAY FLOAT NOT NULL,
    TEXT CHAR NOT NULL,
    IMAGE_FILENAME CHAR NOT NULL,

    NUMBER_TRIES INT NOT NULL,
    CORRECT BOOL NOT NULL,
    ACTIVE BOOL NOT NULL
    )'''
    executeOnDatabase(databasePath, sql)
    return

def createVariableTable(databasePath: str) -> None:
    """Creates the table used to store all variable data"""
    sql = '''CREATE TABLE VARIABLES(
        VARIABLE_UUID CHAR NOT NULL PRIMARY KEY,
        QUESTION_UUID CHAR NOT NULL,
        VARIABLE_NAME CHAR NOT NULL,
        VALUE FLOAT NOT NULL,
        UNITS CHAR NOT NULL,
        DISPLAY_NAME CHAR NOT NULL,
        DECIMAL_PLACES INT NOT NULL
    )'''
    executeOnDatabase(databasePath, sql)
    return

def createDatabase(databasePath: str) -> None:
    """Creates the database from blank, with no contained data. Should only be used if the database file does not currently exist."""
    createSessionTable(databasePath)
    createQuestionTable(databasePath)
    createVariableTable(databasePath)
    return
