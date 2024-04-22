"""
Physics Question Generator
ICS4U
Stuart, Isabelle, Amelia
Generates physics questions and displays them on a website.
History:
Feb 23rd 2024: Program Creation
Edited 27th Feb
Edited 6th March
"""

from json import load
from os.path import join

from flask import Flask

from physqgen.generator.config import Config, copyQuestionImagesToServerFolder

# TODO: not fixed
#creating app
def create_app():
    """Creates base Flask app/server to render the HTML for the user."""
    #setting up app
    global app
    app = Flask(__name__, template_folder="website")
    #secret key to be used for session cookies, security
    app.config["SECRET_KEY"] ="Ajkjaksjksjaksjkiooooo"

    #registering pages
    from physqgen.app.auth import auth
    from physqgen.app.view import views

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

def registerConfig() -> None:
    """Stores the current Config on server run."""
    # get config on run
    with open(join(".", "configs", "active_config.json")) as file:
        with open(join(".", "configs", load(file)["activeConfigName"])) as configFile:
            app.questionConfig = Config.fromFile(load(configFile))


# restarting the server will change the values for variables, but things should still work
if __name__ == '__main__':
    # run with `flask run -h "0.0.0.0" -p 1250`. -h must be 0.0.0.0, -p is the port to use and can be changed.
    app = create_app()
    registerConfig()
    copyQuestionImagesToServerFolder()
    app.run(port=8080, host='0.0.0.0')
