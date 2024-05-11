from dataclasses import InitVar, dataclass, field
from sqlite3 import connect
from uuid import UUID, uuid4

from physqgen import generator
from physqgen.generator.question import Question


@dataclass(slots=True)
class LoginInfo:
    """
    Login information for a Session.\n
    Attributes:\n
        first_name (str): student first name,\n
        last_name (str): student last name,\n
        email (str): student email address
    """
    first_name: str
    last_name: str
    email: str

@dataclass(slots=True)
class Session:
    """
    Student website session data. Tracks and updates student completion of questions. Is partially stored in session cookie, which is why its attributes use snake_case.\n
    Attributes:\n
        databasePath (str): path to the database, relative to the calling script,\n
        uuid (UUID): unique session id,\n
        login_info (LoginInfo): student login info,\n
        question (list): contains the question subclass objects that the student is answering,\n
        active_question (int): default 0, the index in the questions attribute of the question that the student is currently working on,\n
        active_question_data (dict): data to be used on the frontend, taken from the currently active question,\n
        all_questions_correct (bool): whether or not all questions have been completed
    """
    # TODO don't store the session itself, store the necessary data as a property and fetch as wanted, so will always be up to date
    databasePath: str
    uuid: str = field(default_factory=uuid4, init=False) # TODO: actually use this
    login_info: LoginInfo
    questions: list[Question]
    active_question: int = 0

    active_question_data: dict = field(init=False)
    all_questions_correct: bool = field(init=False, default=False)
    initial: InitVar[bool] = False

    def __post_init__(self, initial: bool) -> None:
        """Load in active question data wanted in cookies for website. initial should be set to True if this Session is not already stored in the database."""
        # store so is passed in cookie
        self.all_questions_correct = self.allQuestionsCorrect()
        self.active_question_data = self.currentQuestion.websiteDisplayData
        if initial:
            self.commitSessionToDatabase()
        else:
            self.updateSessionDataInDatabase()
        return
    
    @classmethod
    def recreateSession(cls, databasePath: str, data: dict):
        """Creates a Session from the data stored in the Flask session cookie."""
        obj = cls(
            databasePath,
            # TODO: store instead of resupplying
            LoginInfo(
                data["login_info"]["first_name"],
                data["login_info"]["last_name"],
                data["login_info"]["email"]
            ),
            questions=[
                # TODO: keep a list of question constructors and names instead of using a getattr
                getattr(generator, q["questionType"]).fromUUID(databasePath , q["questionType"], q["id"]) for q in data["questions"]
            ],
            # TODO: store instead of resupplying
            active_question=data["active_question"]
        )
        # set session uuid
        obj.uuid = UUID(data["uuid"])

        return obj

    def updateActiveQuestionData(self, increment: bool = False) -> None:
        """
        Updates the question data stored in the active_question_data attribute. Also commits any changes to the database.\n
        If increment is true, it will increment the currently active question and update accordingly.
        """
        self.updateSessionDataInDatabase()
        # update number of tries
        self.currentQuestion.numberTries += 1
        # if got correct, aka passed increment parameter, then update active question idnex
        if increment:
            self.active_question += 1
        # update data either way for cookie
        self.active_question_data = self.currentQuestion.websiteDisplayData
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
            UPDATE {self.currentQuestion.questionType}
            SET
                NUMBER_TRIES="{self.currentQuestion.numberTries}",
                CORRECT="{self.currentQuestion.correct}"
            WHERE
                QUESTION_UUID="{self.currentQuestion.id}"
            """
            cursor.execute(sql)
            
        # just in case
        connection.close()

        return
    
    @property
    def currentQuestion(self):
        """Returns the currently active Question subclass object."""
        return self.questions[self.active_question] 
    
    def allQuestionsCorrect(self) -> bool:
        """Whether or not the student has completed all questions in this Session."""
        return bool((self.active_question + int(self.currentQuestion.correct)) == len(self.questions))
