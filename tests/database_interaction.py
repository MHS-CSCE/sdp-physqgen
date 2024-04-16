from json import load
from os.path import join

from physqgen.generator import generateQuestions
from physqgen.session import LoginInfo, Session

# test basic database interaction
if __name__ == "__main__":

    # load active config
    with open(join(".", "configs", "active_config.json")) as activeFile:
        activeData = load(activeFile)
    with open(join(".", "configs", activeData["activeConfigName"])) as currentConfig:
        testConfig = load(currentConfig)

    sess = Session(
        login_info=LoginInfo("test_first_name", "test_last_name", "test@email.a"),
        questions=generateQuestions(testConfig)
    )

    # test commiting session data
    sess.commitSessionToDatabase()

    print("session 1 commited")
    
    sess2 = Session(
        LoginInfo("test2", "last2", "email2"),
        questions=generateQuestions(testConfig)
    )
    sess2.commitSessionToDatabase()

    print("session 2 commited")

    sess3 = Session(
        LoginInfo("test3", "last3", "email3"),
        questions=generateQuestions(testConfig)
    )
    sess3.commitSessionToDatabase()

    print("sessiona 3 committed")

    # these commits aren't rolled back, in order to test database operation. use the admin app's clear data button to remove them before committing
