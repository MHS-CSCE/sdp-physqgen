"""

"""

#importing flask and other modules
from flask import Blueprint, Flask, render_template

views = Blueprint('views', __name__)

@views.route('/')
def redirectpage():
    return render_template("index.html")

@views.route('/create')
def q_create(): 
    return "<h1> Question Creation </h1>"

@views.route('/tview')
def t_view():
    return "<h1> Teacher View </h1>"

@views.route('/topen')
def t_open(): 
    return "<h1> Teacher Open </h1>"


