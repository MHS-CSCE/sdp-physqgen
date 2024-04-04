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
    if request.method == "POST":
        #getting input from the form
        Session(
            LoginInfo(

            ),
            generateQuestions(app.questionConfig)

        )
        session['first_name'] = request.form["name"]
        session['last_name'] = request.form["last-name"]
        session['email_a'] = request.form["email-address"]

        #setting session data as variables to return
        first_name = session['first_name']
        last_name = session['last_name']
        email_a = session['email_a']

        #returning the variables
        return first_name,  last_name, email_a

    #rendering the site
    return render_template("loginpage.html")
    
