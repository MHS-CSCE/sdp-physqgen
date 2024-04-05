"""
"""
# importing Flask and other modules
from os import path

from flask import (Blueprint, Flask, redirect, render_template, request,
                   session, url_for)

from physqgen.app.application import app
from physqgen.session import LoginInfo, Session

#defining views for routes
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def log_in():
    #rendering the site
    return render_template("loginpage.html")
    
