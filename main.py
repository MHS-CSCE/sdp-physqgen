"""
Physics Question Generator
ICS4U
Stuart, Isabelle, Amelia
Generates physics questions and displays them on a website.
History:
Febrary 1, 2024: Program Creation
"""

#importing necessary functions/libraries
from physqgen.flask import create_app

if __name__ == "__main__":
    app = create_app()
    
    app.run()
