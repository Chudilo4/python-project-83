from flask import Flask, render_template, request, redirect
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


@app.route('/urls/', methods=['GET', 'POST'])
def urls():
    if request.method == 'POST':
        a = request.form.to_dict()
        if validators.url(a['url']):
            cur = conn.cursor()
            dt = datetime.date.today()
            names = a['url']
            cur.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s);",
                        (names, dt))
            cur.execute("SELECT id FROM urls WHERE name=(%s);",
                        (names,))
            id = cur.fetchone()
            print(id)
            cur.close()
            return redirect(f'/urls/{id[0]}')
        return redirect('/')
    else:
        cur = conn.cursor()
        cur.execute('SELECT * FROM urls;')
        site = cur.fetchall()
        cur.close()
        return render_template('urls.html', site=site)


@app.route('/urls/<int:id>/', methods=['GET', 'POST'])
def show_url(id):
    cur = conn.cursor()
    cur.execute('SELECT * FROM urls WHERE id = (%s);', (id, ))
    site = cur.fetchone()
    cur.close()
    return render_template('show_url.html', site=site)
