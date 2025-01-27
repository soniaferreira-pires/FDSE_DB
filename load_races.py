import pwinput
import pandas as pd
import numpy as np
import psycopg2
import datetime
import csv
import re
import glob

# -------------------------------------------------- WELCOME ----------------------------------------------------------#
print(r"""____    __    ____  _______  __        ______   ______   .___  ___.  _______
\   \  /  \  /   / |   ____||  |      /      | /  __  \  |   \/   | |   ____|
 \   \/    \/   /  |  |__   |  |     |  ,----'|  |  |  | |  \  /  | |  |__   
  \            /   |   __|  |  |     |  |     |  |  |  | |  |\/|  | |   __|  
   \    /\    /    |  |____ |  `----.|  `----.|  `--'  | |  |  |  | |  |____ 
    \__/  \__/     |_______||_______| \______| \______/  |__|  |__| |_______|
                                                                             """)
print("This is the load_races wizzard! \n")
print("'Patience is bitter, but its fruit is sweet.' ~ Aristotle")

print("The process of creating and populating the database may take some time, but I will keep you informed on "
      "the status along the way :) \n")
# -------------------------------------------- CONNECT TO  DATABASE ---------------------------------------------------#

connected = False
while not connected:

    username = input('Type your database username: ')
    password = pwinput.pwinput(prompt='Type your database password: ', mask='*')

    try:
        con = psycopg2.connect(
            database=username,  # your database is the same as your username
            user=username,  # your username
            password=password,  # your password
            host="dbm.fe.up.pt",  # the database host
            port="5433",
            options='-c search_path=public')  # use the schema you want to connect to
        connected = True

    except psycopg2.OperationalError:
        print("You're not connected to FEUP VPN or inputed wrong credentials.")
    else:
        print("You successfully connected to the database.")
    finally:
        continue


# ------------------------------------------ DELETE DATABASE RECORDS --------------------------------------------------#

def delete_records():
    cur0 = con.cursor()
    cur0.execute("TRUNCATE TABLE team, runner, event_type, age_class, event, participation_details;")
    con.commit()


def delete_all_tables():
    cur0 = con.cursor()
    cur0.execute("DROP TABLE team, runner, event_type, age_class, event, participation_details;")
    con.commit()


chosen = False
while not chosen:

    user_input1 = input('Please choose what you would like to do (enter the letter describing your choice): \n'
                        '(a) I wish to delete all records from the database (in public schema) \n'
                        '(b) I wish to delete all records AND tables from the database (in public schema) \n'
                        '(c) I wish to start a database from scratch \n')

    if user_input1.lower() == 'a':
        chosen = True
        delete_records()
        continue

    elif user_input1.lower() == 'b':
        chosen = True
        delete_all_tables()
        continue

    elif user_input1.lower() == 'c':
        chosen = True
        continue

    else:
        print('Please input a valid choice.')
        continue

# ---------------------------------------------- CREATE DATABASE ------------------------------------------------------#
if user_input1.lower() == 'b' or user_input1.lower() == 'c':
    print("-----------------STARTING CREATING TABLES--------------------")

    sql_create = open('races.sql', 'r')
    sql_create_script = sql_create.read()
    sql_create.close()

    print("read the script")

    cur = con.cursor()
    cur.execute(sql_create_script)
    con.commit()
    # con.close()

    print("created the tables in DB")
    print("------------------FINISHED CREATING TABLES---------------------")


# ------------------------------------------------ LOAD DATASET -------------------------------------------------------#

data = pd.read_csv('all_races_dataset.csv',
                   low_memory=False,
                   encoding='utf-8')

# ---------------------------------------------- CLEAN DATASET --------------------------------------------------------#

print("-----------------STARTING TO CLEAN DATA SET -------------------")

# DROPING ROWS REPEATING THE NAME OF COLUMNS

for i, j in data.iterrows():
    # print(f"i: {i}  -- j: {j}")
    if j[1] in data.columns:
        data.drop(i, inplace=True)

print("removed dupplicated column name rows")

# CONVERTING DTYPES

data_type = data.copy()

pd.set_option('display.max_columns', None)

data_type['place'] = data['place'].astype('int64')
data_type['age_class'] = data['age_class'].astype('string')
data_type['place_in_class'] = data['place_in_class'].astype('int64')
data_type['bib'] = data['bib'].astype('int64')
data_type['name'] = data['name'].astype('string')
data_type['sex'] = data['sex'].astype('string')
data_type['nation'] = data['nation'].astype('string')
data_type['team'] = data['team'].astype('string')
data_type['official_time'] = data['official_time'].apply(lambda x: pd.to_timedelta(x)).copy().astype('int64') // 10 ** 9
data_type['net_time'] = data['net_time'].apply(lambda x: pd.to_timedelta(x)).copy().astype('int64') // 10 ** 9
data_type['birth_date'] = data['birth_date'].apply(lambda x: pd.to_datetime(x, dayfirst=True)).copy()
data_type['event'] = data['event'].astype('string')
data_type['event_year'] = data['event_year'].apply(lambda x: (pd.to_datetime(x)).year).copy()
data_type['distance'] = data['distance'].astype('int64')

print("converted datatypes")

# REMOVE DUPPLICATED LINES

data_type.drop_duplicates(subset=None, keep='first', inplace=True)

print("removed dupplicates")

# O data set estava duplicado na totalidade. Por isso é que existia uma linha a meio com o título das colunas.
# Passamos de um dataset com 293858 registos para 146923 registos.

# POPULATE AGE GROUP COLUMN

# Este dataset continha muitos erros no age_group e podemos popular a coluna corretamente


def year_class(event_year, birth_year):
    diff = event_year - birth_year
    if diff >= 65:
        return "65"
    elif diff >= 60:
        return "60"
    elif diff >= 55:
        return "55"
    elif diff >= 50:
        return "50"
    elif diff >= 45:
        return "45"
    elif diff >= 40:
        return "40"
    elif diff >= 35:
        return "35"
    elif diff >= 20:
        return "20"
    elif diff >= 18:
        return "18"
    else:
        return "17"


data_type['age_class'] = data_type.apply(lambda x: x.sex + year_class(x.event_year, x.birth_date.year), axis=1)

print("corrected age_groups")

print("--------------------FINISHED CLEAN DATA SET -------------------")

# ----------------------------------------- PREPARE TABLES TO DATABASE ------------------------------------------------#

print("------------STARTING TO PREPARE TABLES TO DATA BASE -----------")

# ORIGINAL TABLE

data_idx = data_type.copy()
data_idx['age'] = data_idx.apply(lambda x: (x.event_year - x.birth_date.year), axis=1)
idx_lst = [item for item in range(1, (len(data_idx.index)) + 1)]
data_idx.insert(loc=0, column='origin_idx', value=idx_lst)

print("ORIGINAL TABLE DATAFRAME was successfully created")

# TEAM TABLE

data_team = data_idx.loc[:, ['team']].copy()
data_team.drop_duplicates(subset=None, keep='first', inplace=True)
data_team.dropna(axis='rows', inplace=True)
team_idx_lst = [item for item in range(1, (len(data_team.index)) + 1)]
data_team.insert(loc=0, column='team_idx', value=team_idx_lst)
data_team.to_csv("tmp-data_team.csv", sep="%", index=False, header=False, encoding="utf-8")

print("TEAM TABLE DATAFRAME was successfully created")

# RUNNER TABLE

data_runner = data_idx.loc[:, ['name', 'sex', 'nation', 'birth_date']].copy()
data_runner.drop_duplicates(subset=None, keep='first', inplace=True)
runner_idx_lst = [item for item in range(1, (len(data_runner.index)) + 1)]
data_runner.insert(loc=0, column='runner_idx', value=runner_idx_lst)
data_runner.to_csv("tmp-data_runner.csv", sep="%", index=False, header=False, encoding="utf-8")

print("RUNNER TABLE DATAFRAME was successfully created")

# EVENT TYPE TABLE

data_event_type = data_idx.loc[:, ['event']].copy()
data_event_type.drop_duplicates(subset=None, keep='first', inplace=True)
data_event_type.dropna(axis='rows', inplace=True)
event_type_idx_lst = [item for item in range(1, (len(data_event_type.index)) + 1)]
data_event_type.insert(loc=0, column='event_type_idx', value=event_type_idx_lst)
data_event_type.to_csv("tmp-data_event_type.csv", sep="%", index=False, header=False, encoding="utf-8")

print("EVENT_TYPE TABLE DATAFRAME was successfully created")

# AGE CLASS TABLE

data_age_class = data_idx.loc[:, ['age_class']].copy()
data_age_class.drop_duplicates(subset=None, keep='first', inplace=True)
data_age_class.dropna(axis='rows', inplace=True)
age_class_idx_lst = [item for item in range(1, (len(data_age_class.index)) + 1)]
data_age_class.insert(loc=0, column='age_class_idx', value=age_class_idx_lst)
data_age_class.to_csv("tmp-data_age_class.csv", sep="%", index=False, header=False, encoding="utf-8")

print("AGE_CLASS TABLE DATAFRAME was successfully created")

# EVENT TABLE

data_event = data_idx.loc[:, ['event', 'distance', 'event_year', ]].copy()
data_event.drop_duplicates(subset=None, keep='first', inplace=True)
data_event.dropna(axis='rows', inplace=True)
event_idx_lst = [item for item in range(1, (len(data_event.index)) + 1)]
data_event.insert(loc=0, column='event_idx', value=event_idx_lst)
data_event.insert(loc=4, column='event_type_idf', value=0)
for i in range(len(data_event)):
    event_type = data_event.iloc[i, 1]
    event_type_id = data_event_type.loc[data_event_type['event'] == event_type]['event_type_idx']
    data_event.iloc[i, 4] = event_type_id

print("DATA_EVENT TABLE DATAFRAME was successfully created")

data_event2 = data_event.loc[:, ['event_idx', 'distance', 'event_year', 'event_type_idf']].copy()
data_event2.to_csv("tmp-data_event2.csv", sep="%", index=False, header=False, encoding="utf-8")
print("DATA_EVENT 2 TABLE DATAFRAME was successfully created")
print("The next step takes around 40 min.")

# PARTICIPATION DETAILS TABLE

data_participation_details = data_idx.loc[:, ['bib', 'official_time', 'net_time', 'place', 'place_in_class', 'age',
                                              'team', 'name', 'age_class', 'event', 'birth_date', 'sex',
                                              'nation', 'event_year']].copy()
data_participation_details.drop_duplicates(subset=None, keep='first', inplace=True)
participation_details_idx_lst = [item for item in range(1, (len(data_participation_details.index)) + 1)]
data_participation_details.insert(loc=0, column='part_det_idx', value=participation_details_idx_lst)
data_participation_details.insert(loc=15, column='team_idf', value=0)
data_participation_details.insert(loc=16, column='runner_idf', value=0)
data_participation_details.insert(loc=17, column='ageclass_idf', value=0)
data_participation_details.insert(loc=18, column='event_idf', value=0)
for i in range(len(data_participation_details)):
    runner = data_participation_details.iloc[i, 8]
    birth_date = data_participation_details.iloc[i, 11]
    sex = data_participation_details.iloc[i, 12]
    nation = data_participation_details.iloc[i, 13]
    runner_id = data_runner.loc[(data_runner['name'] == runner) & (data_runner['birth_date'] == birth_date) &
                                (data_runner['sex'] == sex) & (data_runner['nation'] == nation)]['runner_idx']

    data_participation_details.iloc[i, 16] = runner_id

print("....... and we're done, thank you!")
print("DATA_PARTICIPATION_DETAILS TABLE DATAFRAME was successfully created")

data_participation_details2 = data_participation_details.copy()
for i in range(len(data_participation_details2)):
    ageclass = data_participation_details2.iloc[i, 9]
    ageclass_id = data_age_class.loc[data_age_class['age_class'] == ageclass]['age_class_idx']
    data_participation_details2.iloc[i, 17] = ageclass_id

print("DATA_PARTICIPATION_DETAILS2: age class fk TABLE DATAFRAME was successfully created")

for i in range(len(data_participation_details2)):
    event = data_participation_details2.iloc[i, 10]
    event_year = data_participation_details2.iloc[i, 14]
    event_id = data_event.loc[(data_event['event'] == event) & (data_event['event_year'] == event_year)]['event_idx']
    data_participation_details2.iloc[i, 18] = event_id

print("DATA_PARTICIPATION_DETAILS2: event_id fk TABLE DATAFRAME was successfully created")

for i in range(len(data_participation_details2)):
    team = data_participation_details2.iloc[i, 7]
    if (team is not None) and (not pd.isna(team)):
        if (team.lower() != 'individual') and (team.lower() != 'indibidual'):
            team_id = data_team.loc[data_team['team'] == team]['team_idx'].to_string(index=False)
        else:
            team_id = ""
    else:
        team_id = ""

    data_participation_details2.iloc[i, 15] = team_id

print("DATA_PARTICIPATION_DETAILS2: team_id fk TABLE DATAFRAME was successfully created")

data_participation_details3 = data_participation_details2.loc[:, ['part_det_idx', 'bib', 'official_time',
                                                                  'net_time', 'place', 'place_in_class',
                                                                  'age', 'team_idf', 'runner_idf',
                                                                  'ageclass_idf', 'event_idf']].copy()
data_participation_details3['official_time'] = data_participation_details3['official_time'].apply(
    lambda x: datetime.datetime.utcfromtimestamp(x).strftime("%H:%M:%S")
    if x > 0 else datetime.datetime.utcfromtimestamp(0).strftime("%H:%M:%S"))
data_participation_details3['net_time'] = data_participation_details3['net_time'].apply(
    lambda x: datetime.datetime.utcfromtimestamp(x).strftime("%H:%M:%S")
    if x > 0 else datetime.datetime.utcfromtimestamp(0).strftime("%H:%M:%S"))
# data_participation_details3['team_idf'] = data_participation_details3['team_idf'].apply(
#    lambda x: None if x == "null" else int(x))
data_participation_details3.to_csv("tmp-data_participation_details3.csv", sep="%", index=False, header=False,
                                   encoding="utf-8")
print("DATA_PARTICIPATION_DETAILS3: TABLE DATAFRAME was successfully created")

# --------------------------------------------- POPULATE DATABASE -----------------------------------------------------#

print("----------------STARTING POPULATING DATABASE-------------------")

# CLEAN BACKSLASH
def clean_csv(input_csv_file):
    for i in glob.glob(input_csv_file):
        read = open(i, 'r', encoding="utf-8")
        reader = read.read()
        csvre = re.sub(r"\\", r"\\\\", str(reader))
        write = open(i, 'w', encoding="utf-8")
        write.write(csvre)
        read.close()
        write.close()


# TABLE TEAM
clean_csv('tmp-data_team.csv')
with open('tmp-data_team.csv', 'r', encoding="utf-8") as f:
    cur = con.cursor()
    cur.copy_from(f, 'team', sep="%", columns=('team_id', 'team_name'))
    con.commit()

print("TEAM TABLE was successfully populated")

# TABLE RUNNER
clean_csv('tmp-data_runner.csv')
with open('tmp-data_runner.csv', 'r', encoding="utf-8") as f:
    cur = con.cursor()
    cur.copy_from(f, 'runner', sep="%", columns=('runner_id', 'runner_name', 'sex', 'nation', 'birthdate'))
    con.commit()

print("RUNNER TABLE was successfully populated")

# TABLE AGE_CLASS
clean_csv('tmp-data_age_class.csv')
with open('tmp-data_age_class.csv', 'r', encoding="utf-8") as f:
    cur = con.cursor()
    cur.copy_from(f, 'age_class', sep="%", columns=('ageclass_id', 'age_class'))
    con.commit()

print("AGE_CLASS TABLE was successfully populated")

# TABLE EVENT_TYPE
clean_csv('tmp-data_event_type.csv')
with open('tmp-data_event_type.csv', 'r', encoding="utf-8") as f:
    cur = con.cursor()
    cur.copy_from(f, 'event_type', sep="%", columns=('eventtype_id', 'eventtype_name'))
    con.commit()

print("EVENT_TYPE TABLE was successfully populated")

# TABLE EVENT
clean_csv('tmp-data_event2.csv')
with open('tmp-data_event2.csv', 'r', encoding="utf-8") as f:
    cur = con.cursor()
    cur.copy_from(f, 'event', sep="%", columns=('event_id', 'distance', 'event_year', 'eventtype_id'))
    con.commit()

print("EVENT TABLE was successfully populated")

# TABLE PARTICIPATION_DETAILS
clean_csv('tmp-data_participation_details3.csv')
with open('tmp-data_participation_details3.csv', 'r', encoding="utf-8") as f:
    cur = con.cursor()
    cur.copy_from(f, 'participation_details', sep="%", columns=('partdet_id', 'bib', 'official_time', 'net_time',
                                                                'place', 'place_in_class', 'age', 'team_id',
                                                                'runner_id', 'ageclass_id', 'event_id'), null="")
    con.commit()

print("PARTICIPATION_DETAILS TABLE was successfully populated")

print("-------------FINISHED POPULATING THE DATA BASE-----------------")

con.close()

print("\nCongratulations, you've reached the end of the wizzard!")