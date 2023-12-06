import os
import sys
import psycopg2
from flask import Flask, request, redirect


app = Flask(__name__)


def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="numbers42"
        )

    return conn


def check_number(conn, num):
    cur = conn.cursor()
    cur.execute('SELECT num FROM numbers WHERE num=%s;', (num,))
    result = cur.fetchone()

    return result


@app.route('/redirect_error')
def redirect_error():
    return 'Error!'


@app.route('/redirect_success')
def redirect_error():
    return 'Success!'

@app.route('/', methods=['POST'])
def main():
    number = request.form.get('number')
    conn = connect_db()

    check = check_number(conn, number)
    if check:
        return redirect('/redirect_error')

    check = check_number(conn, int(number) + 1)
    if check:
        return redirect('/redirect_error')

    cur = conn.cursor()
    cur.execute('INSERT INTO numbers (num) VALUES (%s);', (number,))
    conn.commit()

    return redirect('/redirect_success')


if __name__ == "__main__":
    app.run()
