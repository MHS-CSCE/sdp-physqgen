from dataclasses import dataclass, field
from uuid import uuid4
from sqlite3 import connect

from physqgen.database import DATABASEPATH
from physqgen.generator.question import Question


@dataclass(slots=True)
class LoginInfo:
    first_name: str
    last_name: str
    email_a: str

@dataclass(slots=True)
class Session:
    uuid: str = field(default_factory=uuid4, init=False)
    login_info: LoginInfo
    questions: list[Question]

    def commitSessionToDatabase(self, rollback=False) -> None:
        """
        Constructs SQL command to commit session data to Database.\n
        Overwrites any row with the same uuid. Therefore, can be called multiple times, whenever data is recieved from client.\n
        If rollback is True, will rollback the commit. For testing purposes.
        """
        with connect(DATABASEPATH) as connection:
            cursor = connection.cursor()
            for question in self.questions:
                # we want to not overwrite existing data, adding together number of tries and only overwriting correct

                # prevent sql injection. it stopped working. TODO: fix.

                sql = f"""
                INSERT INTO {question.questionName()} (
                    QUESTION_UUID,
                    FIRST_NAME,
                    LAST_NAME,
                    EMAIL_A,
                    NUMBER_TRIES,
                    CORRECT,
                    SOLVE_VARIABLE,
                    TEXT,
                    CORRECT_RANGE,
                    {",".join([var.name for var in question.variables])}
                )
                VALUES(
                    "{question.id}",
                    "{self.login_info.first_name}",
                    "{self.login_info.last_name}",
                    "{self.login_info.email_a}",
                    {question.numberTries},
                    "{question.correct}",
                    "{question.solveVariable}",
                    "{question.text}",
                    {question.correctRange},
                    {",".join((str(val) for val in question.variableValues()))}
                )
                """

                cursor.execute(sql)
            
            if rollback:
                cursor.connection.rollback()

        return
