from dotenv import dotenv_values
import psycopg2
import os

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
conn.autocommit = True
conn.cursor().execute(open(os.path.join(os.curdir, 'page_analyzer', 'database.sql')).read())