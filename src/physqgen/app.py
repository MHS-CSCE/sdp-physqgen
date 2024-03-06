"""
Started on 23rd Feb
Edited 27th Feb
Edited 6th March
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
        # getting input with firstname = FIRST_NAME in HTML form
        FIRST_NAME= request.form.get("name")
        # getting input with lastname = LAST_NAME in HTML form 
        LAST_NAME = request.form.get("lastname") 
        #getting input with email = EMAIL_A in HTML form
        EMAIL_A = request.form.get("email")

        return FIRST_NAME, LAST_NAME, EMAIL_A

if __name__=='__main__':
    app.run()
