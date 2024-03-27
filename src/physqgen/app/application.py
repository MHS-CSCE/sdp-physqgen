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
# importing Flask and other modules
from flask import Flask, request, render_template, Blueprint, url_for
from os import path

#creating app
def create_app():
    #setting up app
    app = Flask(__name__, template_folder="website")
    #secret key to be used for session cookies, security
    app.config["SECRET_KEY"] ="Ajkjaksjksjaksjkiooooo"

    from physqgen.app.view import views
    from physqgen.app.auth import auth

    #registering pages
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    return app


