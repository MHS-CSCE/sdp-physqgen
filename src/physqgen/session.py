from dataclasses import InitVar, dataclass, field
from sqlite3 import connect
from uuid import UUID, uuid4

from physqgen import generator
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
    databasePath: str
    uuid: str = field(default_factory=uuid4, init=False)
    login_info: LoginInfo
    questions: list[Question]
    active_question: int = 0
    questions_correct: int = 0

    active_question_data: dict = field(init=False)
    initial: InitVar[bool] = False

    def __post_init__(self, initial: bool) -> None:
        """Load in active question data wanted in cookies for website."""
        # add one to index if current question is correct. this happens when submitting the final question
        self.questions_correct = self.active_question + int(bool(self.questions[self.active_question].correct))
        self.active_question_data = self.questions[self.active_question].websiteDisplayData
        if initial:
            self.commitSessionToDatabase()
        else:
            self.updateSessionDataInDatabase()
        return
    
    @classmethod
    def recreateSession(cls, databasePath: str, data: dict):
        """Creates a Session from the data stored in the Flask session cookie"""
        obj = cls(
            databasePath,
            LoginInfo(
                data["login_info"]["first_name"],
                data["login_info"]["last_name"],
                data["login_info"]["email_a"]
            ),
            questions=[
                getattr(generator, q["questionType"]).fromUUID(databasePath , q["questionType"], q["id"]) for q in data["questions"]
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
        self.updateSessionDataInDatabase()
        return
        
    def commitSessionToDatabase(self, rollback: bool = False) -> None:
        """
        Creates rows in the appropriate database tables for the questions and variables for this Session.\n
        If rollback is True, will rollback the commit. For testing purposes.
        """
        with connect(self.databasePath) as connection:
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
                    IMAGE_PATH,
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
                    "{question.imageName}",
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
        with connect(self.databasePath) as connection:
            activeQuestion = self.questions[self.active_question]

            cursor = connection.cursor()
            # TODO: prevent sql injection

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
