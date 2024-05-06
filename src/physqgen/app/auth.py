from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)

from physqgen.app import DATABASEPATH
from physqgen.app.register_config import appConfig
from physqgen.generator import generateQuestions
from physqgen.session import LoginInfo, Session

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

        # TODO: detect an existing session and continue it instead
        session["session"] = Session(
            DATABASEPATH,
            LoginInfo(
                #setting the form input as the login info
                request.form["name"],
                request.form["last-name"],
                request.form["email-address"]
            ),
            questions=generateQuestions(appConfig),
            initial=True
        )
        # creation of Session automatically enters data into database

        # https://dev.to/sachingeek/session-in-flask-store-user-specific-data-on-server-28ap
        return redirect(url_for("views.qpage"), code=302)
    else:
        #rendering the site
        return render_template("loginpage.html")
    
