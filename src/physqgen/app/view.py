"""
Physics Question Generator
ICS4U
Stuart, Isabelle, Amelia
Generates physics questions and displays them on a website.
History:
March 21st 2024: Program Creation
"""

from os.path import join

from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)

from physqgen.app.constants import DATABASEPATH
from physqgen.session import Session

views = Blueprint('views', __name__)

@views.route('/')
def redirectpage():
    """
    Opening page to redirect the user to the login page.

    Returns:
       (HTML template)

    """
    return render_template("index.html")


#for image display purposes
IMG_FOLDER_PATH = join('static', 'images')
@views.route('/qpage', methods=['GET', 'POST'])
def qpage():
    """
    Renders question page, processes the question data and sends it to the front end. 

    Returns:
    (HTML template)
    (bool)
    (image file)
    """

    if request.method == "POST":
        answer: str = request.get_data("answer", as_text=True)
        # remove the extra characters
        # is currently formatted: "answer={actual value}&submit=Send"
        answer = answer[len("answer="):-1*len("&submit=Send")]

        sessionObject = Session.recreateSession(DATABASEPATH, session["session"])
        try:
            activeQuestion = sessionObject.questions[sessionObject.active_question]

            # if not correct, increment. store whether correct
            # will raise value error on float(answer) if it is not a valid float
            activeQuestion.correct = activeQuestion.check_answer(float(answer))
            
            # after assignment to only increment if is a valid float
            activeQuestion.numberTries += 1

            # increment to next active question and reload
            if ((sessionObject.active_question + 1) < len(sessionObject.questions)) and activeQuestion.correct:
                sessionObject.incrementActiveQuestionData()
            # correct & last question
            elif activeQuestion.correct:
                sessionObject.updateSessionDataInDatabase()
                return redirect(url_for("views.exit"), code=302)
            else:
                # incorrect answer
                sessionObject.updateSessionDataInDatabase()
        
        except ValueError:
            # don't count as a submission if the input is not a float value
            # TODO: catch the error and notify user somehow
            pass

        # pass data back, so page updates and etc.
        session["session"] = sessionObject

        return redirect(url_for("views.qpage"), code=302)

    # redirect to login if not logged in
    try:
        session["session"]
    except KeyError:
        return redirect(url_for("auth.log_in"), code=302)

    # fetch image filename for active question
    file = join(IMG_FOLDER_PATH, session["session"]["questions"][session["session"]["active_question"]]["img"])
    
    # get method is included in the no-if path
    return render_template("questionpage.html", image=file)

@views.route('/exit', methods = ['GET', 'POST'])
def exit():
    """
    Last page of the generator, used as a transition page to tell the user to exit.
    """
    try:
        session["session"]
    except KeyError:
        return redirect(url_for("auth.log_in"), code=302)
    
    # load session, updates the counter for number of questions correct
    session["session"] = Session.recreateSession(DATABASEPATH, session["session"])
    
    # check if have gotten all questions correct, redirect to question page if not so
    if session["session"].questions_correct != len(session["session"].questions):
        return redirect(url_for("views.qpage"), code=302)

    return render_template("exit.html")
