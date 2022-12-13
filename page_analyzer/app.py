from flask import Flask, render_template, request, redirect
from dotenv import dotenv_values
import psycopg2
import os
import validators
import datetime
import requests


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
            r = cur.execute('SELECT id FROM urls WHERE name=(%s), (names);')
            if r:
                cur.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s);",
                            (names, dt))
                id = cur.fetchone()
                cur.close()
                return redirect(f'/urls/{id[0]}')
            id = cur.fetchone()
            cur.close()
            return redirect(f'/urls/{id[0]}')
        return redirect('/')
    else:
        cur = conn.cursor()
        cur.execute('SELECT urls.id, urls.name, url_checks.created_at, url_checks.status_code '
                    'FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id;')
        site = cur.fetchall()
        print(site)
        cur.close()
        return render_template('urls.html', site=site)


@app.route('/urls/<int:id>/', methods=['GET', 'POST'])
def show_url(id):
    cur = conn.cursor()
    cur.execute('SELECT * FROM urls WHERE id=(%s);', (id,))
    site = cur.fetchone()
    cur.execute('SELECT * FROM url_checks WHERE url_id=(%s);', (id,))
    site2 = cur.fetchone()
    print(site2)
    print(site)
    cur.close()
    return render_template('show_url.html', site=site, site2=site2)


@app.post('/urls/<int:id>/checks')
def urls_id_checks_post(id):
    dt = datetime.date.today()
    cur = conn.cursor()
    a = cur.execute('SELECT * FROM url_checks WHERE url_id = (%s)', (id,))
    print(bool(a))
    print(a)
    if a:
        cur.execute('UPDATE url_checks '
                    'SET created_at = (%s) WHERE url_id = (%s);', (dt, id))
        cur.close()
        return redirect(f'/urls/{id}/')
    cur.execute("INSERT INTO url_checks (url_id, created_at) VALUES (%s, %s);",
                (id, dt))
    cur.close()
    return redirect(f'/urls/{id}/')

