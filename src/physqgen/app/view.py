"""
Physics Question Generator
ICS4U
Stuart, Isabelle, Amelia
Generates physics questions and displays them on a website.
History:
March 21st 2024: Program Creation
"""

#importing flask and other modules
from flask import Blueprint, Flask, render_template

views = Blueprint('views', __name__)

@views.route('/')
def redirectpage():
    return render_template("index.html")

@views.route('/qpage')
def qpage():
    return render_template("questionpage.html")

@views.route('/create')
def q_create(): 
    return render_template("createquestion.html")

@views.route('/tview')
def t_view():
    return render_template("teacherview.html")

@views.route('/topen')
def t_open(): 
    return render_template("teacheropening.html")


