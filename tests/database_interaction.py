from physqgen.session import Session, LoginInfo
from physqgen.generator import generateQuestions
from io import StringIO

# test basic database interaction
if __name__ == "__main__":
    sess = Session(
        login_info=LoginInfo(
            "test_first_name",
            "test_last_name",
            "test@email.a"
        ),
        questions=generateQuestions(
            StringIO(
                """
                {
                    "questions": [
                        {
                            "correctRange": 0.1,
                            "question": "KinematicsQuestion",
                            "variableConfig": {
                                "displacement": [0, 0],
                                "time": [1, 2],
                                "acceleration": [0.5, 10]
                            },
                            "solveVariable": "initial_velocity",
                            "text": "Test KinematicsQuestion solve for initial_velocity."
                        }
                    ]
                }
                """
            )
        )
    )

    # test commiting session data
    sess.commitSessionToDatabase(rollback=True)
