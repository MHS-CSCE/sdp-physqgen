"""
Physics Question Generator
ICS4U
Stuart, Isabelle, Amelia
Generates physics questions and displays them on a website.
History:
March 21st 2024: Program Creation
"""

#importing flask and other modules
import os
from os import path
from flask import Blueprint, Flask, render_template, request, session
from physqgen.session import Session, LoginInfo
from physqgen.generator.config import generateQuestions
from physqgen.app.application import app
from json import load

views = Blueprint('views', __name__)

@views.route('/')
def redirectpage():
    return render_template("index.html")


img = os.path.join('static', 'images')

@views.route('/qpage', methods=['GET', 'POST'])
def qpage():
    
    #find way to have file path match one added to the question data
    file = os.path.join(img, 'https://blog.blueprintprep.com/wp-content/uploads/2013/05/Blog-Discrete-P1a12.png')

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

        # add this in return 'image=file'
        return render_template("questionpage.html", correct, image=file)

    # TODO: redirect to login if not logged in
    # get method is included here

    # add this in return 'image=file'
    return render_template("questionpage.html", image=file)







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


