from flask import Flask, render_template, request, redirect, url_for
from dotenv import dotenv_values
import psycopg2
import os
import validators
import datetime


# Connect to your postgres DB
dotenv_values()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template(
        'home.html',
        title='Анализатор страниц',
    )

@app.route('/urls', methods=['GET', 'POST'])
def urls():
    if request.method == 'POST':
        a = request.form.to_dict()
        if validators.url(a['url']):
            cur = conn.cursor()
            dt = datetime.date.today()
            print(dt)
            names = a['url']
            cur.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s);", (names, dt))
            cur.close()
            return redirect('/urls')
        return redirect('/')
    else:
        cur = conn.cursor()
        cur.execute('SELECT * FROM urls;')
        return render_template('urls.html', context={"site": cur.fetchone(),
                                                     }
                               )
