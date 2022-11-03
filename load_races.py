import pwinput
import pandas as pd
from datetime import datetime, timedelta
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
    finally:
        continue

# ---------------------------------------------- CREATE DATABASE ------------------------------------------------------#

# sql_create = open('races.sql', 'r')
# sql_create_script = sql_create.read()
# sql_create.close()
#
#
# cur = con.cursor()
# cur.execute(sql_create_script )
# con.commit()
# con.close()

# ------------------------------------------ DELETE DATABASE RECORDS --------------------------------------------------#

# TODO: code for deleting all DB records

# ------------------------------------------------ LOAD DATASET -------------------------------------------------------#

data = pd.read_csv('all_races_dataset.csv',
                   low_memory=False,
                   encoding='utf-8')

# ---------------------------------------------- PREPARE DATASET ------------------------------------------------------#

# DROPING ROWS REPEATING THE NAME OF COLUMNS
for i, j in data.iterrows():
    # print(f"i: {i}  -- j: {j}")
    if j[1] in data.columns:
        data.drop(i, inplace=True)

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
data_type['official_time'] = data['official_time'].apply(lambda x: pd.to_timedelta(x)).copy().astype('int64') // 10**9
data_type['net_time'] = data['net_time'].apply(lambda x: pd.to_timedelta(x)).copy().astype('int64') // 10**9
data_type['birth_date'] = data['birth_date'].apply(lambda x: pd.to_datetime(x, dayfirst=True)).copy()
data_type['event'] = data['event'].astype('string')
data_type['event_year'] = data['event_year'].apply(lambda x: (pd.to_datetime(x)).year).copy()
data_type['distance'] = data['distance'].astype('int64')

# REMOVE DUPPLICATED LINES

data_type.drop_duplicates(subset=None, keep='first', inplace=True)


# O data et estava duplicado na totalidade. Por isso é que existia uma linha a meio com o título das colunas.
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

# --------------------------------------------- POPULATE DATABASE -----------------------------------------------------#


# data_type = pd.read_csv('Book2.csv', low_memory=False, encoding='utf-8')


# columns_lst = data_type.columns[0].split(";")
idx = 0
for index, row in data_type.iterrows():
    age = row['event_year'] - row['birth_date'].year
    place = row['place']
    age_class = row['age_class']
    place_in_class = row['place_in_class']
    bib = row['bib']
    name = row['name']
    sex = row['sex']
    nation = row['nation']
    team = row['team']
    official_time = row['official_time']
    net_time = row['net_time']
    birth_date = row['birth_date']
    event = row['event']
    event_year = row['event_year']
    distance = row['distance']
    cur = con.cursor()
    cur.execute(f"INSERT INTO runner VALUES ({int(index) + 1},'{name}', '{sex}', '{nation}', '{birth_date}'); \n"
                f"INSERT INTO age_class VALUES ({int(index) + 1},'{age_class}'); \n"
                f"INSERT INTO event_type VALUES ({int(index) + 1},'{event}'); \n"
                f"INSERT INTO event VALUES ({int(index) + 1},'{distance}', '{event_year}', {int(index) + 1}); \n"
                f"INSERT INTO team VALUES ({int(index) + 1},'{team}');\n"
                f"INSERT INTO participation_details VALUES ({int(index) + 1},'{bib}', "
                f"'{str(timedelta(seconds=official_time))}','{str(timedelta(seconds=net_time))}',"
                f" {place}, {place_in_class}, {age}, {int(index) + 1}, {int(index) + 1},"
                f" {int(index) + 1},{int(index) + 1});\n"
                )
    con.commit()

# AINDA NÃO ESTÁ ACABADO:
# necessário validar se age_class já existe antes de introduzir valor

