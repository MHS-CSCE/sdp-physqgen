"""
"""
# importing Flask and other modules
from os import path

from flask import (Blueprint, Flask, redirect, render_template, request,
                   session, url_for)

from physqgen.app.application import app
from physqgen.generator.config import generateQuestions
from physqgen.session import LoginInfo, Session

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
    
