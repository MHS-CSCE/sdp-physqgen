"""
Started on 23rd Feb
Edited 27th Feb
"""
# importing Flask and other modules
from flask import Flask, request, render_template 

# Flask constructor
app = Flask(__name__) 

# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])

def gfg():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        FIRST_NAME= request.form.get("name")
        # getting input with name = lname in HTML form 
        LAST_NAME = request.form.get("lastname") 
        EMAIL_A = request.form.get("email")

if __name__=='__main__':
    app.run()
