from os.path import join

from flask import (Blueprint, Response, redirect, render_template, request,
                   session, url_for)

from physqgen.app import DATABASEPATH, IMG_FOLDER_PATH
from physqgen.session import Session

views = Blueprint('views', __name__)

@views.route('/')
def redirectpage() -> str:
    """
    Opening page to redirect the user to the login page.\n
    Returns an HTML template.
    """
    return render_template("index.html")

@views.route('/qpage', methods=['GET', 'POST'])
def qpage() -> str | Response:
    """
    Renders question page, processes the question data and sends it to the front end.\n
    Returns an HTML template or a Response.
    """
    # redirect to login if not logged in. this key is only added during the login process
    try:
        session["user"]
    except KeyError:
        return redirect(url_for("auth.log_in"), code=302)

    if request.method == "POST":
        # TODO: try request.form["submission"] instead
        submission: str = request.get_data("submission", as_text=True)
        # remove the extra characters
        # is currently formatted: "submission={actual value}&submit=Send"
        submission = submission[len("submission="):-1*len("&submit=Send")]

        invalidAnswer = False
        try:
            # will raise value error on float(submission)
            submission = float(submission)
        except ValueError:
            # don't count as a submission if the input is not a float value
            invalidAnswer = True

        if not invalidAnswer:
            sess = Session.fromDatabase(DATABASEPATH, session["user"]["sessionUUID"])

            # checks whether the submission is correct, and if so activates a new question if there is any that are not complete
            # TODO: should update number tries, check submission, increment if not last question, update data in database
            sess.updateBasedOnSubmission(submission)
            
            # update data visible on frontend
            # doesn't need to happen if invalid submission was submitted
            session["user"] = sess.frontendData
            # add imagePath, it needs the folder path, so is more convenient to deal with here
            session["user"]["activeQuestion"]["imagePath"] = join(IMG_FOLDER_PATH, session["user"]["activeQuestion"]["imageFilename"])

    # all questions complete, applies to both GET and POST
    if session["user"]["sessionComplete"]:
        return redirect(url_for("views.exit"), code=302)
    
    return render_template("questionpage.html")

@views.route('/exit', methods = ['GET'])
def exit() -> str | Response:
    """
    Last page of the generator, used as a transition page to tell the user to exit.\n
    Returns an HTML template or a Response.
    """
    # if there is no registered session, redirect to login page
    try:
        session["user"]
    except KeyError:
        return redirect(url_for("auth.log_in"), code=302)
    
    try:
        # load session, updates the counter for number of questions correct
        sess = Session.recreateSession(DATABASEPATH, session["user"])
        session["user"] = sess
    # happens when a session that no longer exists tries to access page, as the data fetched from the database will be None and not behave correctly
    # this should only happen if the database is cleared mid-session, but may as well redirect instead of showing error page
    except TypeError:
        return redirect(url_for("auth.log_in"), code=302)
    
    # check if have gotten all questions correct, redirect to question page if not
    if not sess.allQuestionsCorrect():
        return redirect(url_for("views.qpage"), code=302)

    return render_template("exit.html")
