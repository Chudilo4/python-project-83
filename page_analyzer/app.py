from flask import Flask, render_template
from dotenv import dotenv_values

dotenv_values()
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template(
        'base.html',
        title='Анализатор страниц',
    )
