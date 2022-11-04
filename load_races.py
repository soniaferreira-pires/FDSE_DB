import pwinput
import pandas as pd
import numpy as np
import psycopg2

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
            options='-c search_path=public') # use the schema you want to connect to
        connected = True

    except psycopg2.OperationalError:
        print("You're not connected to FEUP VPN or inputed wrong credentials.")
    else:
        print("You successfully connected to the database.")
    finally:
        continue

# ---------------------------------------------- CREATE DATABASE ------------------------------------------------------#

print("-----------STARTING CREATING TABLES--------------")

sql_create = open('races.sql', 'r')
sql_create_script = sql_create.read()
sql_create.close()

print("read the script")


cur = con.cursor()
cur.execute(sql_create_script)
con.commit()
con.close()

print("created the tables in DB")
print("-----------FINNISHED CREATING TABLES--------------")

# ------------------------------------------ DELETE DATABASE RECORDS --------------------------------------------------#

# TODO: code for deleting all DB records

# ------------------------------------------------ LOAD DATASET -------------------------------------------------------#

data = pd.read_csv('all_races_dataset.csv',
                   low_memory=False,
                   encoding='utf-8')

# ---------------------------------------------- CLEAN DATASET ------------------------------------------------------#

print("--------------------STARTING TO CLEAN DATA SET -------------------")

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


# O data et estava duplicado na totalidade. Por isso é que existia uma linha a meio com o título das colunas.
# Passamos de um dataset com 293858 registos para 146923 registos.

# POPULATE AGE GROUP COLUMN

# Este dataset continha muitos erros no age_group e podemos popular a coluna corretamente
print("removed dupplicates")

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

print("--------------------FINISHED CLEAN DATA SET --------------")

# ----------------------------------------- PREPARE TABLES TO DATABASE ------------------------------------------------#

print("--------------------STARTING TO PREPARE TABLES TO DATA BASE --------------")

# ORIGINAL TABLE

data_idx = data_type.copy()
data_idx['age'] = data_idx.apply(lambda x: (x.event_year - x.birth_date.year), axis=1)
idx_lst = [item for item in range(1, (len(data_idx.index)) + 1)]
data_idx.insert(loc=0, column='origin_idx', value=idx_lst)

print("ORIGINAL TABLE DATAFRAME was successfully created")

# TEAM TABLE

data_team = data_idx.loc[:, ['team']].copy()
data_team.drop_duplicates(subset=None, keep='first', inplace=True)
team_idx_lst = [item for item in range(1, (len(data_team.index)) + 1)]
data_team.insert(loc=0, column='team_idx', value=team_idx_lst)

print("TEAM TABLE DATAFRAME was successfully created")

# RUNNER TABLE

data_runner = data_idx.loc[:, ['name', 'sex', 'nation', 'birth_date']].copy()
data_runner.drop_duplicates(subset=None, keep='first', inplace=True)
runner_idx_lst = [item for item in range(1, (len(data_runner.index)) + 1)]
data_runner.insert(loc=0, column='runner_idx', value=runner_idx_lst)
# data_runner.to_csv('data_runner.csv')

print("RUNNER TABLE DATAFRAME was successfully created")

# EVENT TYPE TABLE

data_event_type = data_idx.loc[:, ['event']].copy()
data_event_type.drop_duplicates(subset=None, keep='first', inplace=True)
event_type_idx_lst = [item for item in range(1, (len(data_event_type.index)) + 1)]
data_event_type.insert(loc=0, column='event_type_idx', value=event_type_idx_lst)

print("EVENT_TYPE TABLE DATAFRAME was successfully created")

# data_event_type.to_csv('data_event_type.csv')

# AGE CLASS TABLE

data_age_class = data_idx.loc[:, ['age_class']].copy()
data_age_class.drop_duplicates(subset=None, keep='first', inplace=True)
age_class_idx_lst = [item for item in range(1, (len(data_age_class.index)) + 1)]
data_age_class.insert(loc=0, column='age_class_idx', value=age_class_idx_lst)
# data_age_class.to_csv('data_age_class.csv')

print("AGE_CLASS TABLE DATAFRAME was successfully created")

# EVENT TABLE

data_event = data_idx.loc[:, ['event', 'distance', 'event_year', ]].copy()
data_event.drop_duplicates(subset=None, keep='first', inplace=True)
event_idx_lst = [item for item in range(1, (len(data_event.index)) + 1)]
data_event.insert(loc=0, column='event_idx', value=event_idx_lst)
data_event.insert(loc=4, column='event_type_idf', value=0)
for i in range(len(data_event)):
    event_type = data_event.iloc[i, 1]
    event_type_id = data_event_type.loc[data_event_type['event'] == event_type]['event_type_idx']
    data_event.iloc[i, 4] = event_type_id

print("DATA_EVENT TABLE DATAFRAME was successfully created")

data_event2 = data_event.loc[:, ['event_idx', 'distance', 'event_year', 'event_type_idf']].copy()
print("DATA_EVENT 2 TABLE DATAFRAME was successfully created")
# data_event.to_csv('data_event.csv')
# data_event2.to_csv('data_event2.csv')

# print(data_event2)

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

print("DATA_PARTICIPATION_DETAILS TABLE DATAFRAME was successfully created")

data_participation_details2 = data_participation_details.copy()
for i in range(len(data_participation_details2)):
    ageclass = data_participation_details2.iloc[i, 9]
    ageclass_id = data_age_class.loc[data_age_class['age_class'] == ageclass]['age_class_idx']
    # print(f" i: {i}, runner_id: {runner_id}, runner: {runner}")
    data_participation_details2.iloc[i, 17] = ageclass_id

print("DATA_PARTICIPATION_DETAILS2: age class fk TABLE DATAFRAME was successfully created")

for i in range(len(data_participation_details2)):
    event = data_participation_details2.iloc[i, 10]
    event_year = data_participation_details2.iloc[i, 14]
    event_id = data_event.loc[(data_event['event'] == event) & (data_event['event_year'] == event_year)]['event_idx']
    # print(f" i: {i}, runner_id: {runner_id}, runner: {runner}")
    data_participation_details2.iloc[i, 18] = event_id

print("DATA_PARTICIPATION_DETAILS2: event_id fk TABLE DATAFRAME was successfully created")

for i in range(len(data_participation_details2)):
    team = data_participation_details2.iloc[i, 7]
    if (team is not None) and (not pd.isna(team)):
        if (team.lower() != 'individual'):
            team_id = int(data_team.loc[data_team['team'] == team]['team_idx'])
        else:
            team_id = np.nan
    else:
        team_id = np.nan

    data_participation_details2.iloc[i, 15] = team_id

print("DATA_PARTICIPATION_DETAILS2: team_id fk TABLE DATAFRAME was successfully created")

data_participation_details3 = data_participation_details2.loc[:, ['part_det_idx', 'bib', 'official_time',
                                                                  'net_time', 'place', 'place_in_class',
                                                                  'age', 'team_idf', 'runner_idf',
                                                                  'ageclass_idf', 'event_idf']].copy()

print("DATA_PARTICIPATION_DETAILS3: TABLE DATAFRAME was successfully created")

# --------------------------------------------- POPULATE DATABASE -----------------------------------------------------#


print("-------------------------STARTING POPULATING DATABASE--------------------")

# TABLE TEAM
for index, row in data_team.iterrows():
    team_idx = row['team_idx']
    name = row['name']
    cur = con.cursor()
    cur.execute(f"INSERT INTO team VALUES ({team_idx},'{name}');")
    con.commit()

print("TEAM TABLE was successfully populated")

# TABLE RUNNER

for index, row in data_runner.iterrows():
    runner_idx = row['runner_idx']
    name = row['name']
    sex = row['sex']
    nation = row['nation']
    birth_date = row['birth_date']
    cur = con.cursor()
    cur.execute(f"INSERT INTO runner VALUES ({runner_idx},'{name}', '{sex}', '{nation}',"
                f"'{birth_date});")
    con.commit()

print("RUNNER TABLE was successfully populated")

# TABLE AGE_CLASS

for index, row in data_age_class.iterrows():
    age_class_idx = row['age_class_idx']
    age_class = row['age_class']
    cur = con.cursor()
    cur.execute(f"INSERT INTO age_class VALUES ({age_class_idx},'{age_class}');")
    con.commit()

print("AGE_CLASS TABLE was successfully populated")

# TABLE EVENT_TYPE

for index, row in data_event_type.iterrows():
    event_type_idx = row['event_type_idx']
    event = row['event']
    cur = con.cursor()
    cur.execute(f"INSERT INTO event_type VALUES ({event_type_idx},'{event}');")
    con.commit()

print("EVENT_TYPE TABLE was successfully populated")

# TABLE EVENT

for index, row in data_event2.iterrows():
    event_idx = row['event_idx']
    distance = row['distance']
    event_year = row['event_year']
    event_type_idf = row['event_type_idf']
    cur = con.cursor()
    cur.execute(f"INSERT INTO event VALUES ({event_idx}, {distance}, '{event_year}', "
                f"{event_type_idf});")
    con.commit()

print("EVENT TABLE was successfully populated")

# TABLE PARTICIPATION_DETAILS

for index, row in data_participation_details3.iterrows():
    part_det_idx = row['part_det_idx']
    bib = row['bib']
    official_time = (pd.to_datetime(row['official_time'], unit='s')).dt.time
    net_time = (pd.to_datetime(row['net_time'], unit='s')).dt.time
    place = row['place']
    place_in_class = row['place_in_class']
    age = row['age']
    runner_idf = row['runner_idf']
    ageclass_idf = row['ageclass_idf']
    event_idf = row['event_idf']
    if not pd.isna(row['team_idf']):
        team_idf = int(row['team_idf'])
    else:
        team_idf = row['team_idf']
    cur = con.cursor()
    cur.execute(f"INSERT INTO participation_details VALUES ({part_det_idx},{bib}, '{official_time}', '{net_time}', "
                f"{place}, {age}, {team_idf}, {ageclass_idf}, {event_idf} ) ;")
    con.commit()
print("PARTICIPATION_DETAILS TABLE was successfully populated")

con.close()

