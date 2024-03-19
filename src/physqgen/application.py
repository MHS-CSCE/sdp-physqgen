"""
Started on 23rd Feb
Edited 27th Feb
Edited 6th March
"""
# importing Flask and other modules
from flask import Flask, request, render_template, Blueprint
from os import path

#defining views for routes
auth = Blueprint('auth', __name__)

#creating app
def create_app():
    app = Flask(__name__, template_folder="website")
    #secret key to be used for session cookies, security
    app.config["SECRET_KEY"] ="Ajkjaksjksjaksjkiooooo"
    return app


#route for login page
@auth.route('/log_in', methods =["GET", "POST"])
def log_in():
    #if form is submitted by user
    if request.method == "POST":
        #getting input from said form
        FIRST_NAME= request.form.get("name") 
        LAST_NAME = request.form.get("last-name") 
        EMAIL_A = request.form.get("email-address")

    return render_template("loginpage.html")


#route for question page
#@auth.route('/question_page', methods = ["GET", "POST"])
#def question_page(): 
    #if request.method == "POST":
    #if request.method == "GET": 


#route for question creation page
#@auth.route('/create_page, methods = ["GET", "POST"])
#def create_page():
    #if request.method = "POST": 
    #if request.method = "GET": 