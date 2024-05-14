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
    Renders question page, processes the question data and updates frontend, redirecting to exit page if all questions are complete.\n
    Returns an HTML template or a Response.
    """
    # redirect to login if not logged in. this key is only added during the login process
    try:
        session["user"]
    except KeyError:
        return redirect(url_for("auth.log_in"), code=302)

    if request.method == "POST":
        submission: str = request.get_data("submission", as_text=True)
        # remove extra characters
        # is currently formatted "answer={actual value}&submit=Send"
        submission = submission[len("answer="):-1*len("&submit=Send")]

        invalidAnswer = False
        try:
            # will raise value error on float(submission)
            submission = float(submission)
        except ValueError:
            # don't count as a submission if the input is not a float value
            invalidAnswer = True

        if not invalidAnswer:
            try:
                sess = Session.fromDatabase(DATABASEPATH, session["user"]["sessionUUID"])
            except IndexError:
                # will error this way if the database has been cleared since session creation
                # redirect to login
                return redirect(url_for("auth.log_in"), code=302)

            # checks whether the submission is correct, and if so activates a new question if there is any that are not complete
            # if is not time to go to exit page
            if session["user"]["activeQuestion"] is not None:
                sess.update(submission)
            
            # update data visible on frontend after updating sess
            session["user"] = sess.frontendData

            # if is not time to go to exit page
            if session["user"]["activeQuestion"] is not None:
                # update imagePath, it needs the folder path, so is more convenient to deal with here
                # has to go after the replace above so it is not overwritten, and so it does not cause issues when activeQuestion becomes None
                session["user"]["activeQuestion"]["imagePath"] = join(IMG_FOLDER_PATH, session["user"]["activeQuestion"]["imageFilename"])

    # all questions complete, applies to both GET and POST
    # this will continue to redirect the user even if the database is cleared because the cookie is still present
    # could be changed to reconstruct the session object, fail, and send to login, if that is preferred
    # ideally that would be by moving the above .fromDatabase call out of the POST section
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
    
    # check if have gotten all questions correct, redirect to question page if not
    # if the session has been cleared, this will redirect to qpage, and on the first valid submission redirect to login, because of leftover cookies
    if not session["user"]["sessionComplete"]:
        return redirect(url_for("views.qpage"), code=302)

    return render_template("exit.html")
