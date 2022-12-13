from flask import Flask, render_template, request, redirect, flash
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


@app.route('/')
def hello_world():
    return render_template(
        'home.html',
        title='Анализатор страниц',
    )


@app.post('/urls/add')
def urls_add():
    dt = datetime.datetime.now()
    form = request.form.to_dict()
    valid_url = validators.url(form['url'])
    if valid_url:
        cur = conn.cursor()
        cur.execute('SELECT id FROM urls WHERE name=(%s);', (form['url'],))
        id_find = cur.fetchone()
        cur.close()
        if id:
            return redirect(f'/urls/{id_find[0]}')
        cur.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s);",
                   (form['url'], dt))
        id_insert = cur.fetchone()
        cur.close()
        return redirect(f'/urls/{id_insert[0]}')


@app.get('/urls/')
def get_urls():
    cur = conn.cursor()
    cur.execute('SELECT urls.id, urls.name, url_checks.created_at '
                'FROM urls LEFT JOIN url_checks '
                'ON urls.id = url_checks.url_id;')
    site = cur.fetchall()
    return render_template('urls.html', site=site)


@app.get('/urls/<int:id>/')
def show_url(id):
    cur = conn.cursor()
    cur.execute('SELECT * FROM urls WHERE id=(%s);', (id,))
    site = cur.fetchone()
    cur.execute('SELECT * FROM url_checks WHERE url_id = (%s);', (id,))
    site2 = cur.fetchall()
    cur.close()
    return render_template('show_url.html', site=site, site2=site2)


@app.post('/urls/<int:id>/checks')
def urls_id_checks_post(id):
    dt = datetime.datetime.now()
    cur = conn.cursor()
    cur.execute('INSERT INTO url_checks (created_at, url_id ) VALUES (%s, %s);', (dt, id))
    cur.close()
    return redirect(f'/urls/{id}/')

