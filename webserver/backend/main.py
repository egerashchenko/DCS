import psycopg2
import os
from flask import Flask, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_USER = os.getenv("USER_DB")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB = os.getenv("DB")


NUM = 0


def connect_to_postgres():
    conn = psycopg2.connect(
    	user=DB_USER, 
    	password=PASSWORD, 
    	host=HOST, 
    	port=PORT, 
    	database=DB
    	)

    return conn


def check(cur, num):
    cur.execute("SELECT num FROM nums WHERE num=%s", (num,))
    res = cur.fetchone()
    
    if res:
        return False
    
    return True


@app.route("/error_one")
def error_one():
    print("This number is already in DB.")
    return "This number is already in DB."


@app.route("/error_two")
def error_two():
    print("This number is one less than number in DB.")
    return "This number is one less than number in DB."


@app.route("/next_number")
def next_number():
	return str(NUM + 1)


@app.route("/", methods=['GET', 'POST'])
def main():
	if request.method == "POST":
	    conn = connect_to_postgres()
	    cur = conn.cursor()
	    
	    num = request.form.get("num")
	    
	    global NUM
	    NUM = int(num)
	    
	    if not check(cur, NUM):
	        return redirect(url_for("error_one"))

	    if not check(cur, NUM + 1):
	        return redirect(url_for("error_two"))
	    
	    
	    cur.execute("INSERT INTO nums VALUES (%s)", (NUM,))
	    conn.commit()
	    
	    return redirect(url_for("next_number"))
	
	return '''
           <form method="POST">
               <div>
                   <label>Number: <input type="int" name="num"></label>
               </div>
               <br>
               <input type="submit" value="Submit">
           </form>
           '''


if __name__ == "__main__":
	app.run()

