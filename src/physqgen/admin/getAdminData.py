from sqlite3 import connect

from physqgen.admin.constants import DATABASEPATH


def addStudentData(dict: dict, parsedRow: tuple) -> None:
    """
    Modifies passed dict to add data from passed row to a student key. Tuple added contains number of tries, and whether they got it correct.
    """
    fullname = f"{parsedRow[0]} {parsedRow[1]} ({parsedRow[2]})"

    if fullname not in dict:
        dict[fullname] = list()

    dict[fullname].append((parsedRow[3], parsedRow[4]))

    return


def getRelevantQuestionData() -> dict[str, list[tuple]]:
    """
    Collects wanted data from question objects stored in database.\n
    Returns a dict with student names as keys (FirstName LastName strings) and a list of the data associated with them from the database.\n
    First return is the dict of student names and associated questionData: dict[str, list[tuple]]\n
    Second return is the set of tables pulled from (question types).
    """

    studentQuestionInfo: dict = dict()

    with connect(DATABASEPATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            # TODO: remove this once database reformat is fixed
            # taken from https://www.sqlitetutorial.net/sqlite-show-tables/
            """
            SELECT 
                name
            FROM 
                sqlite_schema
            WHERE 
                type ='table' AND 
                name NOT LIKE 'sqlite_%';
            """
        )

        tableList = cursor.fetchall()
        for index, stringTuple in enumerate(tableList):
            tableList[index] = stringTuple[0]

        for table in tableList:
            # don't try and fetch from variables table
            if table != "VARIABLES":
                # table is a tuple with a single string
                # extracted when inputting

                # table names cannot be parametrized, so have to use a formatted string
                # table names are from database anyways, so shouldn't be any real risk of sql injection

                # assignCursorRowFactoryQuestionType(cursor, table)
                cursor.execute(
                    f"""
                    SELECT
                        FIRST_NAME,
                        LAST_NAME,
                        EMAIL,
                        NUMBER_TRIES,
                        CORRECT
                    FROM
                        {table}
                    """
                )

                for data in cursor.fetchall():
                    # mutates the dict directly
                    addStudentData(studentQuestionInfo, data)
    # shouldn't be necessary, but is.
    conn.close()
    
    return studentQuestionInfo
