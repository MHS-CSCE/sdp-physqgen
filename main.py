"""
Physics Question Generator
ICS4U
Stuart, Isabelle, Amelia
Generates physics questions and displays them on a website.
History:
Febrary 1, 2024: Program Creation
March 8th: Altered app.run
"""
from physqgen.app.application import create_app
from os.path import join
from json import load

if __name__ == '__main__':
    app = create_app()
    
    # get config on run
    with open(join(".", "configs", "active_config.json")) as file:
        with open(join(".", "configs", load(file)["activeConfigName"])) as configFile:
            # use generateQuestions to interpret it, generating question from it
            app.questionConfig = configFile.read()

    app.run(port=8080, host='0.0.0.0',debug='True')
