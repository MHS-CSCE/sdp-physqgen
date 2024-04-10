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

    #getting input from the form, passing it into the session class
    if request.method == "POST":

        session["session"] = Session(
            LoginInfo(
                #setting the form input as the login info
                request.form["name"],
                request.form["last-name"],
                request.form["email-address"]
            ),
            questions=generateQuestions(app.questionConfig)
        )
        # TODO: figure out how to return question info to populate page
        # TODO: figure out where the submit on this page will go, how to check and take action based on it
        return render_template("questionpage.html")

    return render_template("questionpage.html")

@views.route('/create', methods=['GET', 'POST'])
def q_create(): 
    return render_template("createquestion.html")

@views.route('/tview', methods=['GET', 'POST'])
def t_view():
    return render_template("teacherview.html")

@views.route('/topen', methods=['GET', 'POST'])
def t_open(): 
    return render_template("teacheropening.html")


