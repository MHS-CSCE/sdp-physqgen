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

    # TODO: move to physqgen.database, encapsulation
    def commitSessionToDatabase(self, rollback=False) -> None:
        """
        Constructs SQL command to commit session data to Database.\n
        Overwrites any row with the same uuid. Therefore, can be called multiple times, whenever data is recieved from client.\n
        If rollback is True, will rollback the commit. For testing purposes.
        """
        # TODO: look into how primary key uuid acts, if will auto-overwrite
        with getDatabaseConnection() as connection:
            cursor = connection.cursor()
            for question in self.questions:
                # TODO
                # we want to not overwrite existing data, adding together number of tries and only overwriting correct
                # but first, the session would need to be able to be restarted upon visiting site again

                # commented out code is the proper way, that prevents sql injection. it stopped working. TODO: fix.
                # sql = f"""
                # INSERT INTO ? (
                #     QUESTION_UUID,
                #     FIRST_NAME,
                #     LAST_NAME,
                #     EMAIL_A,
                #     NUMBER_TRIES,
                #     CORRECT,
                #     ANSWER
                #     {", ?"*len(question.variables)})
                #     VALUES(?, ?, ?, ?, ?, ?, ?{", ?"*len(question.variables)})
                # """

                # insertValues = [
                #     question.questionName(), # question table name
                #     # enum value column names, to ensure order
                #     *[var.name for var in question.variables],

                #     # column values
                #     question.id, # QUESTION_UUID
                #     self.login_info.first_name,
                #     self.login_info.last_name,
                #     self.login_info.email_a,
                #     self.number_tries,
                    # question.solveVariable,
                    # question.text,
                    # question.correctRange,
                #     *question.variableValues()
                # ]

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
                    {self.number_tries},
                    "{question.solveVariable}",
                    "{question.text}",
                    {question.correctRange},
                    {question.answer},
                    {",".join((str(val) for val in question.variableValues()))}
                )
                """

                cursor.execute(sql)
            
            if rollback:
                cursor.connection.rollback()
