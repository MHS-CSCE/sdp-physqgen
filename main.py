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

from physqgen import Config, create_app

if __name__ == '__main__':
    app = create_app()
    
    # get config on run
    with open(join(".", "configs", "active_config.json")) as file:
        with open(join(".", "configs", load(file)["activeConfigName"])) as configFile:
            app.questionConfig = Config.fromFile(load(configFile))
    
    exit(app.run(port=8080, host='0.0.0.0',debug='True'))
