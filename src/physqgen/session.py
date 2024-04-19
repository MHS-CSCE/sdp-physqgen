from dataclasses import dataclass, field, InitVar
from sqlite3 import connect
from uuid import uuid4, UUID

from physqgen import generator
from physqgen.database import DATABASEPATH
from physqgen.generator.question import Question


@dataclass(slots=True)
class LoginInfo:
    first_name: str
    last_name: str
    email_a: str

@dataclass(slots=True)
class Session:
    """
    activeQuestion stores the index of the current question. Incremeneted when a question is gotten correct.
    """
    uuid: str = field(default_factory=uuid4, init=False)
    login_info: LoginInfo
    questions: list[Question]
    active_question: int = 0

    active_question_data: dict = field(init=False)
    initial: InitVar[bool] = False

    def __post_init__(self, initial: bool) -> None:
        """Load in active question data. Will be first question."""
        self.active_question_data = self.questions[self.active_question].websiteDisplayData
        if initial:
            self.commitSessionToDatabase()
        else:
            self.updateSessionDataInDatabase()
        return
    
    @classmethod
    def recreateSession(cls, data: dict):
        """Creates a Session from the data stored in the Flask session cookie"""
        obj = cls(
            LoginInfo(
                data["login_info"]["first_name"],
                data["login_info"]["last_name"],
                data["login_info"]["email_a"]
            ),
            questions=[
                getattr(generator, q["questionType"]).fromUUID(q["questionType"], q["id"]) for q in data["questions"]
            ],
            active_question=data["active_question"]
        )
        # set session uuid
        obj.uuid = UUID(data["uuid"])

        return obj

    def incrementActiveQuestionData(self) -> None:
        """Updates the question data stored in the active_question_data attribute to the current active_question. Also commits data to database."""
        self.updateSessionDataInDatabase()
        self.active_question += 1
        self.active_question_data = self.questions[self.active_question].websiteDisplayData
        # DEBUG
        print(f"Active question after incrementing: {self.questions[self.active_question]}")
        self.updateSessionDataInDatabase()
        return
        
    def commitSessionToDatabase(self, rollback: bool = False) -> None:
        """
        Creates rows in the appropriate database tables for the questions and variables for this Session.\n
        If rollback is True, will rollback the commit. For testing purposes.
        """
        with connect(DATABASEPATH) as connection:
            cursor = connection.cursor()
            for question in self.questions:

                # TODO: prevent sql injection. doesn't allow setting table names from input, can only outsource last bit
                sql = f"""
                INSERT INTO {question.questionType} (
                    QUESTION_UUID,
                    FIRST_NAME,
                    LAST_NAME,
                    EMAIL_A,
                    NUMBER_TRIES,
                    CORRECT,
                    SOLVE_VARIABLE,
                    TEXT,
                    CORRECT_RANGE,
                    {",".join(question.varNames).upper()}
                )
                VALUES (
                    "{question.id}",
                    "{self.login_info.first_name}",
                    "{self.login_info.last_name}",
                    "{self.login_info.email_a}",
                    {question.numberTries},
                    "{question.correct}",
                    "{question.solveVariable}",
                    "{question.text}",
                    {question.correctRange},
                    "{"\", \"".join((str(question.getValue(name, id=True)) for name in question.varNames))}"
                )
                """

                cursor.execute(sql)
            
                # commit variables to separate table
                for variable in question.variables:
                    variableSQL = f'''
                    INSERT INTO VARIABLES (
                        VARIABLE_UUID,
                        NAME,
                        VALUE,
                        DISPLAY_NAME,
                        UNITS
                    )
                    VALUES (
                        ?,
                        ?,
                        ?,
                        ?,
                        ?
                    )
                    '''

                    cursor.execute(
                        variableSQL,
                        [str(variable.varID), variable.name, variable.value, variable.displayName, variable.units]
                    )
                
                if rollback:
                    connection.rollback()
        # just in case
        connection.close()

        return
    
    def updateSessionDataInDatabase(self) -> None:
        """Updates rows in the appropriate database tables for the Session's active question."""
        with connect(DATABASEPATH) as connection:
            print(self.questions[self.active_question])
            activeQuestion = self.questions[self.active_question]

            cursor = connection.cursor()
            # TODO: prevent sql injection

            print(f"Question number tries: {activeQuestion.numberTries}")
            sql = f"""
            UPDATE {activeQuestion.questionType}
            SET
                NUMBER_TRIES="{activeQuestion.numberTries}",
                CORRECT="{activeQuestion.correct}"
            WHERE
                QUESTION_UUID="{activeQuestion.id}"
            """
            cursor.execute(sql)
            
        # just in case
        connection.close()

        return
