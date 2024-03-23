from dataclasses import dataclass, field
from uuid import uuid4
from physqgen.generator.question import Question
from physqgen.database import getDatabaseConnection

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
    number_tries: int = 0
    correct: bool = False

    def commitSessionToDatabase(self) -> None:
        """Constructs SQL command to commit session data to Database. Overwrites any row with the same uuid."""
        # TODO: look into how primary key uuid acts, if will auto-overwrite
        with getDatabaseConnection() as connection:
            cursor = connection.cursor()
            for question in self.questions:
                # TODO
                # we want to not overwrite existing data, adding together number of tries and only overwriting correct
                # but first, the session would need to be able to be restarted upon visiting site again

                sql = f"""
                INSERT INTO ? (
                    QUESTION_UUID,
                    FIRST_NAME,
                    LAST_NAME,
                    EMAIL_A,
                    NUMBER_TRIES,
                    CORRECT,
                    ANSWER
                    {", ?"*len(question.variables)})
                    VALUES(?, ?, ?, ?, ?, ?, ?{", ?"*len(question.variables)})
                """

                insertValues = [
                    question.questionName(), # question table name
                    # enum value column names, to ensure order
                    *[var.name for var in question.variables],

                    # column values
                    question.id, # QUESTION_UUID
                    self.login_info.first_name,
                    self.login_info.last_name,
                    self.login_info.email_a,
                    self.number_tries,
                    self.correct,
                    question.answer,
                    *question.variableValues()
                ]

                cursor.execute(sql, insertValues)
