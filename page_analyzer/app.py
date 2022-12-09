from flask import Flask
from dotenv import dotenv_values

dotenv_values()
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome to Flask!'
