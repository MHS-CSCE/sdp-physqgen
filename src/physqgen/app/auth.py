"""
"""
# importing Flask and other modules
from os import path

from flask import (Blueprint, Flask, redirect, render_template, request,
                   session, url_for)

from physqgen.app.application import app
from physqgen.session import LoginInfo, Session
from physqgen.generator import generateQuestions

#defining views for routes
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def log_in():
    """
    Allows the user to login to the site, stores their information for the database, and redirects them to the questionpage.

    Returns:
        (HTML template)
    """
    #getting input from the form, passing it into the session class
    if request.method == "POST":

        print(app.questionConfig)
        session["session"] = Session(
            LoginInfo(
                #setting the form input as the login info
                request.form["name"],
                request.form["last-name"],
                request.form["email-address"]
            ),
            questions=generateQuestions(app.questionConfig)
        )
        # TODO: not actually redirecting
        # https://dev.to/sachingeek/session-in-flask-store-user-specific-data-on-server-28ap
        return redirect(url_for("views.qpage"), code=302)
    else:
        #rendering the site
        return render_template("loginpage.html")
    
