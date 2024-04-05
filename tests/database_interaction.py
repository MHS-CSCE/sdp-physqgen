from physqgen.session import Session, LoginInfo
from physqgen.generator import generateQuestions
from io import StringIO

# test basic database interaction
if __name__ == "__main__":
    testConfig = StringIO(
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

    sess = Session(
        login_info=LoginInfo(
            "test_first_name",
            "test_last_name",
            "test@email.a"
        ),
        questions=generateQuestions(testConfig)
    )

    # test commiting session data
    sess.commitSessionToDatabase()
    
    sess2 = Session(
        LoginInfo("test2", "last2", "email2"),
        questions=generateQuestions(testConfig)
    )
    sess2.commitSessionToDatabase()

    sess3 = Session(
        LoginInfo("test3", "last3", "email3"),
        questions=generateQuestions(testConfig)
    )
    sess3.commitSessionToDatabase()

    # these commits aren't rolled back, in order to test database operation. use the admin app's clear data button to remove them before committing
