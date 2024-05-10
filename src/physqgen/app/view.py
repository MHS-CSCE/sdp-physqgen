from os.path import join

from flask import (Blueprint, redirect, render_template, request, session,
                   url_for, Response)

from physqgen.app.constants import DATABASEPATH, IMG_FOLDER_PATH
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
    # redirect to login if not logged in
    try:
        # also extracts session data for ease of use
        sessionData: dict = session["session"]
    except KeyError:
        return redirect(url_for("auth.log_in"), code=302)

    if request.method == "POST":
        answer: str = request.get_data("answer", as_text=True)
        # remove the extra characters
        # is currently formatted: "answer={actual value}&submit=Send"
        answer = answer[len("answer="):-1*len("&submit=Send")]

        try:
            sessionObject = Session.recreateSession(DATABASEPATH, sessionData)
        # happens when a session that no longer exists tries to access page, as the data fetched from the database will be None and not behave correctly
        # this should only happen if the database is cleared mid-session, but may as well redirect instead of showing error page
        except TypeError:
            return redirect(url_for("auth.log_in"), code=302)
    
        try:
            activeQuestion = sessionObject.questions[sessionObject.active_question]

            # if not correct, increment. store whether correct
            # will raise value error on float(answer) if it is not a valid float
            activeQuestion.correct = activeQuestion.check_answer(float(answer))
            
            # after assignment to only increment if is a valid float

            # whether to increment to next active question
            increment = ((sessionObject.active_question + 1) < len(sessionObject.questions)) and activeQuestion.correct
            # reload stored data, also allows checking whether last submission was correct
            sessionObject.updateActiveQuestionData(increment)
            # correct & last question
            if not increment and activeQuestion.correct:
                return redirect(url_for("views.exit"), code=302)
        
            # pass data back, so any change are visible on page
            # doesn't need to happen if invalid answer was submitted
            session["session"] = sessionObject
        
        except ValueError:
            # don't count as a submission if the input is not a float value
            pass
    else:
        # GET request
        # redirect to exit page if have already completed all questions
        if len(sessionData["questions"]) == sessionData["questions_correct"]:
            return redirect(url_for("views.exit"), code=302)

    # fetch image filename for active question
    file = join(IMG_FOLDER_PATH, sessionData["active_question_data"]["imageName"])
    
    return render_template("questionpage.html", image=file)

@views.route('/exit', methods = ['GET'])
def exit() -> str | Response:
    """
    Last page of the generator, used as a transition page to tell the user to exit.\n
    Returns an HTML template or a Response.
    """
    # if there is no registered session, redirect to login page
    try:
        session["session"]
    except KeyError:
        return redirect(url_for("auth.log_in"), code=302)
    
    try:
        # load session, updates the counter for number of questions correct
        sessionObject = Session.recreateSession(DATABASEPATH, session["session"])
        session["session"] = sessionObject
    # happens when a session that no longer exists tries to access page, as the data fetched from the database will be None and not behave correctly
    # this should only happen if the database is cleared mid-session, but may as well redirect instead of showing error page
    except TypeError:
        return redirect(url_for("auth.log_in"), code=302)
    
    # check if have gotten all questions correct, redirect to question page if not
    if sessionObject.questions_correct != len(sessionObject.questions):
        return redirect(url_for("views.qpage"), code=302)

    return render_template("exit.html")
