"""
Physics Question Generator
ICS4U
Stuart, Isabelle, Amelia
Generates physics questions and displays them on a website.
History:
Febrary 1, 2024: Program Creation
"""
from physqgen.application import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0',debug='True')