#Dependencies
from sqlalchemy import create_engine
from sqlalchemy import inspect
import pandas as pd
import psycopg2
import datetime as dt
import config

# Check config file
config.username

# Details for connection to local SQL database
protocol = 'postgresql'
username = config.username #'<username>'
password = config.password #'<password>'
host = 'localhost'
port = 5432
database_name = 'project3db'

# Build SQL con inital
conn = psycopg2.connect(user=username, password=password, host=host, port=port)
conn.autocommit = True

# store DB cursor 
cursor = conn.cursor()

# create table statement
sql = "create database "+database_name+";"

# create database 
cursor.execute(sql)
print("Database created successfully........")

# Build SQL con to database
conn = psycopg2.connect(user=username, password=password, host=host, port=port, database=database_name)
conn.autocommit = True

# reset cursor 
cursor = conn.cursor()

# Drop table if exists 
cursor.execute("DROP TABLE IF EXISTS flu_data")

# Creating table 1
sqltable1 ='''CREATE TABLE flu_data (
week TEXT,
state TEXT PRIMARY KEY,
age_group TEXT,
sex TEXT,
type_subtype TEXT,
count INTEGER
)'''
cursor.execute(sqltable1)
print("Table created successfully........")
conn.commit()

# Drop table if exists 
cursor.execute("DROP TABLE IF EXISTS covid_data")

# Creating table 2
sqltable2 ='''CREATE TABLE covid_data (
week TEXT,
state TEXT PRIMARY KEY,
confirmed INT,
recovered INT,
deaths INT,
confirmed_cum INT,
recovered_cum INT,
deaths_cum INT
)'''
cursor.execute(sqltable2)
print("Table created successfully........")
conn.commit()

# close connection
conn.close()

# import dataset from URL
url = 'https://raw.githubusercontent.com/M3IT/COVID-19_Data/master/Data/COVID_AU_state.csv'
covid_states_df = pd.read_csv(url)
covid_states_df.head(5)

# group by week ending Friday
covid_states_df['date'] = pd.to_datetime(covid_states_df['date']) - pd.to_timedelta(7, unit='d')
covid_states_df = covid_states_df.groupby(['state_abbrev', pd.Grouper(key='date', freq='W-FRI')]).sum().reset_index().sort_values('date')

# inspect data
covid_states_df.head(5)

# drop unneeded columns
covid_states_df.drop(['tests', 'confirmed_cum', 'deaths_cum', 'recovered_cum' , 'tests_cum', 'positives', 'positives_cum', 'hosp', 'hosp_cum', 'icu', 'icu_cum', 'vent', 'vent_cum', 'vaccines', 'vaccines_cum'],   axis=1, inplace=True)

# fill na columns 
covid_states_df = covid_states_df.fillna(0)

# cumalitive counts confirmed
covid_states_df['confirmed_cum'] = covid_states_df.groupby('state_abbrev')['confirmed'].cumsum()

# cumalitive counts recovered
covid_states_df['recovered_cum'] = covid_states_df.groupby('state_abbrev')['recovered'].cumsum()

# cumalitive counts deaths
covid_states_df['deaths_cum'] = covid_states_df.groupby('state_abbrev')['deaths'].cumsum()

# rename column date to week
covid_states_df.rename(columns={'date':'week'}, inplace=True)

# rename column state_abbrev to state
covid_states_df.rename(columns={'state_abbrev':'state'}, inplace=True)

# reset index
covid_states_df.reset_index(drop=True, inplace=True)

# rearrange columns
covid_states_df = covid_states_df[['week', 'state', 'confirmed','recovered','deaths', 'confirmed_cum', 'recovered_cum', 'deaths_cum']]

# inspect data
covid_states_df.head()

# Read second worksheet
flu_df2 = pd.read_excel('Data/national-notifiable-diseases-surveillance-system-nndss-public-dataset-influenza-laboratory-confirmed-dataset.xlsx', sheet_name=1, skiprows=[0, 1, 2, 3])
flu_df2

# Read third worksheet
flu_df3 = pd.read_excel('Data/national-notifiable-diseases-surveillance-system-nndss-public-dataset-influenza-laboratory-confirmed-dataset.xlsx', sheet_name=2, skiprows=[0, 1, 2, 3])
flu_df3

# Concatenate the dataframes
flu_df = pd.concat([flu_df2, flu_df3])
flu_df.shape

flu_df.columns

# convert the week ending date to datetime
flu_df['Week Ending (Friday)'] = pd.to_datetime(flu_df['Week Ending (Friday)']) - pd.to_timedelta(7, unit='d')
flu_groupby = flu_df.groupby(['Week Ending (Friday)', 'State', 'Age  group', 'Sex', 'Type/Subtype'], as_index = False)['Indigenous status'].count()
flu_groupby = flu_groupby.rename(columns={'Week Ending (Friday)': 'week', 'State': 'state', 'Age  group': 'age_group', 'Sex': 'sex', 'Type/Subtype': 'type_subtype', 'Indigenous status': 'Count'})
flu_groupby.head(-50)

# Connect to local SQL database
rds_connection_string = f'{protocol}://{username}:{password}@{host}:{port}/{database_name}'
# Create engine
engine = create_engine(rds_connection_string)
insp = inspect(engine)

# Check for tables
insp.get_table_names()

# send data to sql table
flu_groupby.to_sql(name='flu_data', con=engine, if_exists='replace', index=False)

# send data to sql table
covid_states_df.to_sql(name='covid_data', con=engine, if_exists='replace', index=False)

# check data upload
pd.read_sql_query('select * from covid_data', con=engine).head()

# check data upload
pd.read_sql_query('select * from flu_data', con=engine).head()