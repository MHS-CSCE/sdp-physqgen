"""
Physics Question Generator
ICS4U
Stuart, Isabelle, Amelia
Generates physics questions and displays them on a website.
History:
March 21st 2024: Program Creation
"""

#importing flask and other modules
from flask import Blueprint, Flask, render_template, request, session
from physqgen.session import Session, LoginInfo
from physqgen.generator.config import generateQuestions
from physqgen.app.application import app
from json import load

views = Blueprint('views', __name__)

@views.route('/')
def redirectpage():
    return render_template("index.html")

@views.route('/qpage', methods=['GET', 'POST'])
def qpage():
    if request.method == "POST":
        answer = request.get_data["answer"]
        sessionData: Session = session["session"]
        try:
            # if not correct, increment. store whether correct
            # will raise value error on float(answer) if it is not a valid float
            if not (correct := (activeQuestion := sessionData.questions[sessionData.active_question]).check_answer(float(answer))):
                activeQuestion.numberTries += 1
            
            # increment to next active question and reload
            if correct:
                if (sessionData.active_question + 1) < len(sessionData.questions):
                    sessionData.active_question += 1
                    sessionData.reloadActiveQuestionData()
                else:
                    # user just finished last question
                    # TODO: final redirect
                    pass
            
            # commit session to database
            sessionData.commitSessionToDatabase()
        
        except ValueError as e:
            # don't count as a submission if the input is not a float value
            correct = False

        # TODO: indication of correct / false on page. may need to store in session
        return render_template("questionpage.html"), correct

    # TODO: redirect to login if not logged in
    # get method is included here
    return render_template("questionpage.html")







#No longer used templates
# @views.route('/create', methods=['GET', 'POST'])
# def q_create(): 
#     return render_template("createquestion.html")

# @views.route('/tview', methods=['GET', 'POST'])
# def t_view():
#     return render_template("teacherview.html")

# @views.route('/topen', methods=['GET', 'POST'])
# def t_open(): 
#     return render_template("teacheropening.html")


