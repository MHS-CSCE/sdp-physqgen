"""
Started on 23rd Feb
Edited 27th Feb
Edited 6th March
"""
# importing Flask and other modules
from flask import Flask, request, render_template, Blueprint
from os import path

#creating app
def create_app():
    #setting up app
    app = Flask(__name__, template_folder=".\\src\\website")
    #secret key to be used for session cookies, security
    app.config["SECRET_KEY"] ="Ajkjaksjksjaksjkiooooo"

    from physqgen.app.view import views
    from physqgen.app.auth import auth

    #registering pages
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    return app


