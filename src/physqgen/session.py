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
    """
    activeQuestion stores the index of the current question. Incremeneted when a question is gotten correct.
    """
    uuid: str = field(default_factory=uuid4, init=False)
    login_info: LoginInfo
    questions: list[Question]
    active_question = int = 0

    active_question_data: dict = field(init=False)

    def __post_init__(self) -> None:
        """Load in active question data. Will be first question."""
        self.reloadActiveQuestionData()
        return

    # def checkIfQuestionCorrect(self, submission: str) -> Enum:
    #     """TODO"""
    #     # TODO: verification
    #     # TODO: checking, increment if correct, return whether to send new site (enum reload or keep)
    
    def reloadActiveQuestionData(self) -> None:
        """Updates the question data stored in the active_question_data attribute to the current active_question. Also commits data to database."""
        self.active_question_data = self.questions[self.active_question].getWebsiteDisplayData()
        self.commitSessionToDatabase()
        return

    def test(self) -> None:
        return f"TEST TEXT RETURN {self.uuid}"
        
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
