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
        # TODO: submit answer, check if correct, alter session active question
        return render_template("questionpage.html")

    # TODO: redirect to login if not logged in
    # get method is included here
    return render_template("questionpage.html")

# @views.route('/create', methods=['GET', 'POST'])
# def q_create(): 
#     return render_template("createquestion.html")

# @views.route('/tview', methods=['GET', 'POST'])
# def t_view():
#     return render_template("teacherview.html")

# @views.route('/topen', methods=['GET', 'POST'])
# def t_open(): 
#     return render_template("teacheropening.html")


