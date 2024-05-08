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

from flask import Flask


#creating app
def create_app():
    """Creates base Flask app/server to render the HTML for the user."""
    # create app
    app = Flask(__name__, template_folder="website")
    # secret key to be used for session cookies, security
    app.config["SECRET_KEY"] ="Ajkjaksjksjaksjkiooooo"

    # registering pages
    # must be imported in this function or will cause circular import error
    from physqgen.app.auth import auth
    from physqgen.app.view import views

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
