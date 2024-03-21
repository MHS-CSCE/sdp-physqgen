from dataclasses import dataclass
from physqgen.generator.question import Question
from physqgen.database import getDatabaseConnection

@dataclass(slots=True)
class Session:
    first_name: str
    last_name: str
    email_a: str
    question: Question
    number_tries: int = 0
    correct: bool = False

    def commitToDatabase(self) -> None:
        """Constructs SQL command to commit session data to Database. Overwrites any row with the same uuid."""
        with getDatabaseConnection() as connection:
            cursor = connection.cursor()
            # TODO: look into how primary key uuid acts, if will auto-overwrite

            sql = f"""
            INSERT INTO ? (?, ?, ?, ?, ?, ?, ?{", ?"*len(self.question.variables)})
                VALUES(?, ?, ?, ?, ?, ?, ?{", ?"*len(self.question.variables)})
            """

            insertValues = [
                self.question.questionName(), # question table name
                # column names, to ensure order
                "QUESTION_UUID",
                "FIRST_NAME",
                "LAST_NAME",
                "EMAIL_A",
                "NUMBER_TRIES",
                "CORRECT",
                "ANSWER",
                *[var.name for var in self.question.variables], # enum names

                # column values
                self.question.id, # QUESTION_UUID
                self.first_name,
                self.last_name,
                self.email_a,
                self.number_tries,
                self.correct,
                self.question.answer,
                *self.question.variableValues()
            ]

            cursor.execute(sql, insertValues)
