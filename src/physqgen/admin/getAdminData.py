from physqgen.database import getDatabaseConnection, assignCursorRowFactoryQuestionType
from copy import deepcopy

def addStudentData(dict: dict, parsedRow: tuple) -> None:
    """
    Modifies passed dict to add data from passed row to a student key. Tuple added contains number of tries, and whether they got it correct.
    """
    fullname = f"{parsedRow[1]} {parsedRow[2]} ({parsedRow[3]})"

    if fullname not in dict:
        dict[fullname] = list()

    dict[fullname].append((parsedRow[4], parsedRow[5]))

    return


def getRelevantQuestionData() -> dict[str, list[tuple]]:
    """
    Collects wanted data from question objects stored in database.\n
    Returns a dict with student names as keys (FirstName LastName strings) and a list of the data associated with them from the database.\n
    dict[str, list[tuple]]
    """

    studentQuestionInfo: dict = dict()


    with getDatabaseConnection() as conn:
        cursor = conn.cursor()

        cursor.execute(
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


        tableList = deepcopy(cursor.fetchall())

        for table in tableList:
            assignCursorRowFactoryQuestionType(cursor, table, studentInfo=True)

            cursor.execute("""SELECT FROM ?""", table)

            for data in cursor.fetchall():
                # mutates the dict directly
                addStudentData(studentQuestionInfo, data)
    
    return studentQuestionInfo
