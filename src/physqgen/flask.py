"""
Started on 23rd Feb
Edited 27th Feb
"""

#importing all of the important functions/libraries
import os
from flask import Flask, render_template, request, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import func

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # testing
    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app

"""
used this site as a tutorial 
https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
"""

basedir = os.path.abspath(os.path.dirname(__file__))

#can be anything i believe? 
# app.config['SECRET KEY'] = 'SABWWITSSJOQJIOQW3ASUI1'

# #specifies database used
# app.config['SQLALCHEMY_DATABASE_URI'] =\
#         'sqlite:///' + os.path.join(basedir, 'database.db')

# #disables tracking of modifications, to save memory
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# #initializing variable for database
# db = SQLAlchemy(app) 

# #find a way to connect these to the submissions in login page?
# #creates a class for all of the information from the student
# class Student(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(100), nullable=False)
#     lastname = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(80), unique=True, nullable=False)
#     created_at = db.Column(db.DateTime(timezone=True),
#                            server_default=func.now())


#     #returns student name
#     def __repr__(self):
#         return f'<Student {self.firstname}>'
    
#MORE IS NECESSARY FOR IT TO RUN PROPERLY, BUT MISSING THE DATABASE TO CONNECT TO
