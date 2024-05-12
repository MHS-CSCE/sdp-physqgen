from os.path import join

from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)

from physqgen.app import DATABASEPATH, IMG_FOLDER_PATH
from physqgen.generator.config import appConfig
from physqgen.session import LoginInfo, Session

#defining views for routes
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def log_in() -> str:
    """
    Allows the user to login to the site, stores their information for the database, and redirects them to the questionpage.\n
    Returns an HTML template.
    """
    #getting input from the form, passing it into the session class
    if request.method == "POST":
        sess = Session(
            DATABASEPATH,
            LoginInfo(
                # user input
                request.form["name"],
                request.form["last-name"],
                request.form["email-address"]
            ),
            questions=appConfig.generateQuestions()
        )
        # set an active question
        sess.setNewActiveQuestion()

        # add new session to the database
        sess.addToDatabase()

        # https://dev.to/sachingeek/session-in-flask-store-user-specific-data-on-server-28ap
        session["user"] = sess.frontendData
        # add image path for initial display before any submissions
        session["user"]["activeQuestion"]["imagePath"] = join(IMG_FOLDER_PATH, session["user"]["activeQuestion"]["imageFilename"])

        return redirect(url_for("views.qpage"), code=302)
    else:
        #rendering the site
        return render_template("loginpage.html")
    
