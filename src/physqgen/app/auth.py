"""
"""
# importing Flask and other modules
from flask import Flask, request, render_template, Blueprint
from os import path

#defining views for routes
auth = Blueprint('auth', __name__)


@auth.route('/')
def log_in():
    return render_template("loginpage.html")


   

""" if form is submitted by user
    if request.method == "POST":
        getting input from said form
        FIRST_NAME= request.form.get("name") 
        LAST_NAME = request.form.get("last-name") 
        EMAIL_A = request.form.get("email-address")

        if EMAIL_A = ms jones email 
            mb send to the teacher view? 

    return render_template("loginpage.html")"""