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
from os import path

# importing Flask and other modules
from flask import Blueprint, Flask, render_template, request, url_for


#creating app
def create_app():
    """
    Creates base Flask app/server to render the HTML for the user.
    """
    #setting up app
    global app
    app = Flask(__name__, template_folder="website")
    #secret key to be used for session cookies, security
    app.config["SECRET_KEY"] ="Ajkjaksjksjaksjkiooooo"

    from physqgen.app.auth import auth
    from physqgen.app.view import views

    #registering pages
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    return app


