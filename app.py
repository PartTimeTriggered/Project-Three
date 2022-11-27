import psycopg2
import config
from flask import Flask, render_template

app = Flask(__name__)


#database='project3db', user=config.username , password=config.password, host="127.0.0.1", port="5432"

def get_db_connection():
    conn = psycopg2.connect(database='project3db', user=config.username , password=config.password, host="127.0.0.1", port="5432")
    return conn

try:
    conn = psycopg2.connect(database='project3db', user=config.username , password=config.password, host="127.0.0.1", port="5432")
 
    if conn is not None:
        print('Connection established to PostgreSQL.')
    else:
        print('Connection not established to PostgreSQL.')
         
except (Exception, psycopg2.DatabaseError) as error:
    print(error)



@app.route('/')
def home():
   return render_template('index.html')
if __name__ == '__main__':
   app.run()


@app.route('/covid')
def covid():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM covid_data;')
    covid_data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('covid.html', covid_data=covid_data)

@app.route('/flu')
def flu():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM flu_data;')
    flu_data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('flu.html', flu_data=flu_data)