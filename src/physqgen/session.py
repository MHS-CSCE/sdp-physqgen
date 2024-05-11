from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Literal

from physqgen.database import executeOnDatabase
from physqgen.generator.question import Question


@dataclass(slots=True)
class LoginInfo:
    """
    Login information for a Session.\n
    Attributes:\n
        firstName (str): student first name,\n
        lastName (str): student last name,\n
        email (str): student email address
    """
    firstName: str
    lastName: str
    email: str

    @classmethod
    def fromDatabase(cls, databasePath: str, sessionUUID: str | UUID):
        """Fetches the login info stored in the database for the given sessionUUID and returns an instance of cls populated with it."""
        sql = '''SELECT (
            FIRST_NAME,
            LAST_NAME,
            EMAIL
        ) FROM SESSIONS WHERE SESSION_UUID=?'''
        replacements = tuple(str(sessionUUID))
        # TODO: check that returned valid result
        # index 0 is the first (and only) row that met the criteria
        results = executeOnDatabase(databasePath, sql, replacements)[0]

        return cls(
            firstName=results[0],
            lastName=results[1],
            email=results[2]
        )

@dataclass(slots=True)
class Session:
    """
    Student website session data. Tracks and updates student completion of questions. The property frontendData is used to retrieve data to be stored in session cookie.\n
    Attributes:\n
        databasePath (str): path to the database, relative to the calling script,\n
        loginInfo (LoginInfo): student login info,\n
        questions (list[Questions]): contains the question subclass objects that the student is answering,\n
        uuid (UUID): unique session id
    """
    databasePath: str
    loginInfo: LoginInfo
    questions: list[Question]
    uuid: str = field(default_factory=uuid4)

    def __post_init__(self, initial: bool) -> None:
        """Load in active question data wanted in cookies for website. initial should be set to True if this Session is not already stored in the database."""
        # TODO: fix the initial session creation steps, maybe do a placeholder commit first and then just update everything
        if initial:
            self.commitSessionToDatabase()
        else:
            self.updateSessionDataInDatabase()
        return
    
    @property
    def frontendData(self) -> dict:
        """Returns a dict containing all relevant information for the website and for reconstructing the Session from the database."""
        return {
            "sessionUUID": self.uuid,
            "questionsCompleted": (numCorrect := self.questionsCorrect), # question number is derived from this by adding one, is only used for display
            "sessionComplete": bool(numCorrect == len(self.questions)),
            "activeQuestion": qData.questionFrontendData if (qData := self.activeQuestion) is not None else None
        }
    
    @property
    def questionsCorrect(self) -> int:
        """The number of questions that have been completed."""
        complete = 0
        for question in self.questions:
            if question.correct:
                complete += 1
        
        return complete
    
    @property
    def activeQuestion(self) -> Question | None:
        """Returns the currently active Question subclass instance, or None if no question is active."""
        for question in self.questions:
            if question.active:
                return question
    
    @staticmethod
    def getAllQuestions(databasePath: str, sessionUUID: str) -> list[Question]:
        """Constructs a list of all the Question subclass instances in the database which corespond to the passed sessionUUID."""
        sql = '''SELECT QUESTION_UUID FROM QUESTIONS WHERE SESSION_UUID=?'''
        replacements = tuple(sessionUUID)
        results = executeOnDatabase(databasePath, sql, replacements)
        # TODO: check result validity

        questions = []
        for (uuid) in results:
            questions.append(Question.fromDatabase(databasePath, uuid))

        return questions
    
    @classmethod
    def fromDatabase(cls, databasePath: str, sessionUUID: str):
        """Recreates an existing Session object."""
        return cls(
            databasePath=databasePath,
            uuid=sessionUUID,
            loginInfo=LoginInfo.fromDatabase(databasePath, sessionUUID),
            questions=Session.getAllQuestions(sessionUUID),
        )

    def updateActiveQuestionData(self, increment: bool = False) -> None:
        """
        Updates the question data stored in the active_question_data attribute. Also commits any changes to the database.\n
        If increment is true, it will increment the currently active question and update accordingly.
        """
        self.updateSessionDataInDatabase()
        # update number of tries
        self.activeQuestion.numberTries += 1
        # if got correct, aka passed increment parameter, then update active question idnex
        if increment:
            self.active_question += 1
        # update data either way for cookie
        self.active_question_data = self.activeQuestion.websiteDisplayData
        self.updateSessionDataInDatabase()
        return
        
    def commitSessionToDatabase(self) -> None:
        """Creates rows in the appropriate database tables for the questions and variables for this Session."""
        # TODO: update docstring with any weird behaviours after database is reformatted, like any possible errors
        with connect(self.databasePath) as connection:
            cursor = connection.cursor()
            for question in self.questions:

                # TODO: prevent sql injection. doesn't allow setting table names from input, can only outsource last bit
                sql = f"""
                INSERT INTO {question.questionType} (
                    QUESTION_UUID,
                    FIRST_NAME,
                    LAST_NAME,
                    EMAIL,
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
                    "{self.login_info.email}",
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
                        UNITS,
                        DISPLAY_NAME,
                        DECIMAL_PLACES
                    )
                    VALUES (
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?
                    )
                    '''

                    cursor.execute(
                        variableSQL,
                        [str(variable.varID), variable.name, variable.value, variable.units, variable.displayName, variable.decimalPlaces]
                    )
        
        # just in case
        connection.close()

        return
    
    def updateSessionDataInDatabase(self) -> None:
        """Updates rows in the appropriate database tables for the Session's active question."""
        with connect(self.databasePath) as connection:
            cursor = connection.cursor()
            # TODO: prevent sql injection

            sql = f"""
            UPDATE {self.activeQuestion.questionType}
            SET
                NUMBER_TRIES="{self.activeQuestion.numberTries}",
                CORRECT="{self.activeQuestion.correct}"
            WHERE
                QUESTION_UUID="{self.activeQuestion.id}"
            """
            cursor.execute(sql)
            
        # just in case
        connection.close()

        return