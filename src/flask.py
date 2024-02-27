"""
Started on 23rd Feb
Edited 27th Feb
"""

#importing all of the important functions/libraries
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

"""
used this site as a tutorial 
https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
"""

basedir = os.path.abspath(os.path.dirname(__file__))

#initializing app
app = Flask(__name__)

#can be anything i believe? 
app.config['SECRET KEY'] = 'SABWWITSSJOQJIOQW3ASUI1'

#specifies database used
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

#disables tracking of modifications, to save memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initializing variable for database
db = SQLAlchemy(app) 

#find a way to connect these to the submissions in login page?
#creates a class for all of the information from the student
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())


    #returns student name
    def __repr__(self):
        return f'<Student {self.firstname}>'
    
#MORE IS NECESSARY FOR IT TO RUN PROPERLY, BUT MISSING THE DATABASE TO CONNECT TO


#determining if recieved answer is within proper range
#rearrange with variables from answer in answer page
#range of answer can be altered depending on client preferences
def inrange(solu, res): 
    #solving for min and max of the range of accepted answers
    solu1 = solu- solu*0.1
    solu2 = solu+ solu*0.1 

    #checking if it's within said range
    if res in range(solu1, solu2):
        return True
    else:
        return False
