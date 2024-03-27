"""
"""
# importing Flask and other modules
from flask import Flask, request, render_template, Blueprint, redirect, url_for
from os import path

#defining views for routes
auth = Blueprint('auth', __name__)


@auth.route('/login')
def log_in():
    if request.method == "POST":
        #getting input from the form
        FIRST_NAME = request.form.get("name")
        LAST_NAME = request.form.get("last-name")
        EMAIL_A = request.form.get("email-address")
        return redirect(url_for('/qpage'))
    return render_template("loginpage.html")
