from dataclasses import dataclass, field
from uuid import UUID, uuid4

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
        """Fetches the login info stored in the database for the given sessionUUID and returns an instance of cls populated with it. Will raise an IndexError if the database has been cleared since the session was created."""
        sql = '''
            SELECT 
                FIRST_NAME,
                LAST_NAME,
                EMAIL
            FROM SESSIONS WHERE SESSION_UUID=?
        '''
        replacements = (str(sessionUUID),)
        # index 0 is the first (and only) row that met the criteria
        # will error if the database has been cleared since the session was created
        # let it error to prevent other issues
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
    uuid: UUID = field(default_factory=uuid4)

    @property
    def frontendData(self) -> dict:
        """Returns a dict containing all relevant information for the website and for reconstructing the Session from the database."""
        return {
            "sessionUUID": str(self.uuid),
            "loginInfo": {
                "firstName": self.loginInfo.firstName,
                "lastName": self.loginInfo.lastName,
                "email": self.loginInfo.email
            },
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
        replacements = (sessionUUID,)
        results = executeOnDatabase(databasePath, sql, replacements)
        if len(results) == 0:
            # could happen if the database has been cleared since creation
            # should error on other things first, but check just in case
            # because this should never run, don't include it in docstring
            raise RuntimeError("Session has been cleared. Cannot load data.")

        questions = []
        for uuid in results:
            # return value is a tuple containing only the uuid
            uuid = uuid[0]
            questions.append(Question.fromDatabase(databasePath, uuid))

        return questions
    
    @classmethod
    def fromDatabase(cls, databasePath: str, sessionUUID: str):
        """Recreates an existing Session object. Will raise an IndexError if session data has been cleared."""
        return cls(
            databasePath=databasePath,
            uuid=sessionUUID,
            loginInfo=LoginInfo.fromDatabase(databasePath, sessionUUID),
            questions=Session.getAllQuestions(databasePath, sessionUUID),
        )
    
    def setNewActiveQuestion(self) -> bool:
        """Tries to find a Question in questions that is has not been completed to make the new activeQuestion. Returns whether or not this was successful."""
        for question in self.questions:
            if not question.correct:
                question.active = True
                return True
        else:
            return False
    
    def addToDatabase(self) -> None:
        """Add this Session's data to the database, including contained Questions and Variables. Only works if is not already in database."""
        # commit self
        sql = '''
            INSERT INTO SESSIONS (
                SESSION_UUID,
                FIRST_NAME,
                LAST_NAME,
                EMAIL
            ) VALUES (
                ?,
                ?,
                ?,
                ?
            )
        '''
        replacements = (
            str(self.uuid),
            self.loginInfo.firstName,
            self.loginInfo.lastName,
            self.loginInfo.email
        )
        executeOnDatabase(self.databasePath, sql, replacements)

        # commit questions. they will commit their own variables
        for question in self.questions:
            question.addToDatabase(self.databasePath, self.uuid)

        return

    def update(self, submission: float) -> None:
        """
        Update Session and activeQuestion based on contents of submission.\n
        Adds one to activeQuestion's numberTries.\n
        Checks submission and updates activeQuestion as needed.\n
        Updates database with new info before returning.
        """
        self.activeQuestion.numberTries += 1

        self.activeQuestion.correct = self.activeQuestion.checkSubmission(submission)

        if self.activeQuestion.correct:
            self.activeQuestion.active = False
        
            # set new active question if possible
            # if not possible, ignore, as that means all questions are complete
            self.setNewActiveQuestion()

        self.updateDatabase()
        return
    
    def updateDatabase(self) -> None:
        """Updates Session data, including Questions, stored in database."""
        for question in self.questions:
            question.updateDatabase(self.databasePath)

        return
