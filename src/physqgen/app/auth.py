"""
"""
# importing Flask and other modules
from main import app
from flask import Flask, request, render_template, Blueprint, redirect, url_for, session
from os import path
from physqgen.session import Session, LoginInfo
from physqgen.generator.config import generateQuestions

#defining views for routes
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def log_in():
     #getting input from the form, passing it into the session class
   if request.method == "POST":
        session["session"] = Session(
           LoginInfo(
               #setting the form input as the login info
               request.form["name"],
               request.form["last-name"],
               request.form["email-address"]
            ),
           generateQuestions(app.questionConfig)
        )
        return session["session"]

    #rendering the site
   return render_template("loginpage.html")
    
