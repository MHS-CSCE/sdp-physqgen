"""
Physics Question Generator
ICS4U
Stuart, Isabelle, Amelia
Generates physics questions and displays them on a website.
History:
Febrary 1, 2024: Program Creation
March 8th: Altered app.run
"""
from json import load
from os.path import join

from physqgen.app.application import create_app

if __name__ == '__main__':
    app = create_app()
    
    # get config on run
    with open(join(".", "configs", "active_config.json")) as file:
        app.questionConfig = join(".", "configs", load(file)["activeConfigName"])

    app.run(port=8080, host='0.0.0.0',debug='True')
