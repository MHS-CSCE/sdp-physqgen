from physqgen.admin import DATABASEPATH
from physqgen.database import executeOnDatabase


def getStudentData() -> dict[str, list[tuple[int, bool]]]:
    """
    Collects wanted data from database.\n
    Returns a dict with student names as keys (FirstName LastName (email) strings) and a list of the data associated with them from the database.\n
    The nested tuple contains, in this order: numberTries, correct.
    """

    sql = '''
        SELECT
            SESSION_UUID,
            NUMBER_TRIES,
            CORRECT
        FROM
            QUESTIONS
    '''
    results = executeOnDatabase(DATABASEPATH, sql)

    studentQuestionInfo: dict = dict()
    for row in results:
        sql = '''
            SELECT
                FIRST_NAME,
                LAST_NAME,
                EMAIL
            FROM
                SESSIONS
            WHERE
                SESSION_UUID=?
        '''
        replacements = (row[0],)
        # should only get one result, index 0
        sessionResults = executeOnDatabase(DATABASEPATH, sql, replacements)[0]
        fullname = f"{sessionResults[0]} {sessionResults[1]} ({sessionResults[2]})"
        # add the key for the student if it is not already there
        try:
            # if it is there, append to the list
            studentQuestionInfo[fullname].append(
                (
                    row[1],
                    row[2]
                )
            )
        except KeyError:
            studentQuestionInfo[fullname] = [
                (
                    row[1],
                    row[2]
                )
            ]

    return studentQuestionInfo
