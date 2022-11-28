import psycopg2
import config
from flask import Flask, render_template, jsonify
import pandas as pd

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
def plots():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT week, confirmed FROM covid_data ORDER BY week;')
    covid_data = cur.fetchall()
    covid_df= pd.DataFrame(covid_data, columns=['week', 'confirmed'])
    cur.execute('SELECT f.week, f.Count FROM flu_data as f GROUP BY f.week ORDER BY f.week;')
    flu_data = cur.fetchall()
    flu_df = pd.DataFrame(flu_data, columns=['week', 'Count'])    
    cur.close()
    conn.close()
    # covid_df['week'].dt.strftime("%Y-%m-%d")
    # flu_df['week'].dt.strftime("%Y-%m-%d")
    covid_groupby = covid_df.groupby('week')['confirmed'].sum()
    #covid_groupby = covid_groupby.sort_index(ascending=True)
    c_week = covid_groupby.index.tolist()
    c_confirmed = covid_groupby.values.tolist()
    flu_groupby = flu_df.groupby('week')['Count'].sum()
    #flu_groupby = flu_groupby.sort_index(ascending=True)
    f_week = flu_groupby.index.tolist()
    f_count = flu_groupby.values.tolist()
    return render_template("index.html", c_w = c_week, c_c = c_confirmed, f_w = f_week, f_c = f_count)

@app.route('/api/refresh/<value>', methods=['GET'])
def refresh(value):
    if value =='1' :
        s = 'NSW'
    elif value =='2' :
        s = 'VIC'
    elif value =='3' :
        s = 'QLD'
    elif value =='4' :
        s = 'SA'
    elif value =='5' :
        s = 'WA'
    elif value =='6' :
        s = 'TAS'
    elif value =='7' :
        s = 'NT'
    elif value =='8' :
        s = 'ACT'
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT week, state, confirmed FROM covid_data ORDER BY week;", s)
    covid_data = cur.fetchall()
    covid_df= pd.DataFrame(covid_data)
    cur.execute('SELECT f.week, f.Count FROM covid_data as f GROUP BY f.week ORDER BY f.week;') 
    flu_data = cur.fetchall()
    flu_df = pd.DataFrame(flu_data)
    cur.close()
    conn.close()
    covid_groupby = covid_df.groupby('week', as_index =False).apply(lambda x: x[x['state'] == 'NSW' ]['confirmed'].sum())
    flu_groupby = flu_df.groupby('week', as_index =False).apply(lambda x: x[x['state'] == 'NSW' ]['Count'].sum())
    #covid_groupby = covid_df.groupby('week')['confirmed'].sum()
    c_week = covid_groupby.index.tolist()
    c_confirmed = covid_groupby.values.tolist()
    #flu_groupby = flu_df.groupby('week')['Count'].sum()
    f_week = flu_groupby.index.tolist()
    f_count = flu_groupby.values.tolist()
    
    return jsonify(c_w = c_week, c_c = c_confirmed, f_w = f_week, f_c = f_count)

# @app.route('/flu')
# def flu():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM flu_data;')
#     flu_data = cur.fetchall()
#     cur.close()
#     conn.close()
#     return render_template('flu.html', flu_data=flu_data)

if __name__ == '__main__':
   app.run(debug = True, host='localhost', port=5000)