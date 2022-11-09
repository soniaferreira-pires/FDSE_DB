# imports
import pwinput
import pandas as pd
import numpy as np
import psycopg2
import datetime
import csv
import re
import glob
import matplotlib.pyplot as plt
#import mysql.connector



# Auxiliary function(s)
def convert_time_to_minutes(time_values_list):
    
    # Copy the input list/array
    converted_time_values = time_values_list.copy()
    
    # Convert official time entries to string
    for idx, time_value in enumerate(converted_time_values):
        # Convert official time values into minutes
        converted_time_values[idx] = ((time_value.hour * 60 * 60) + (time_value.minute * 60) + (time_value.second)) / 60
    

    return converted_time_values



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

#--------------------------------------------GET VALUES----------------------------------------------------------



# Result 1: Relation between age and time
cur = con.cursor()
cur.execute(f'SELECT age_class, official_time FROM participation_details JOIN age_class USING(ageclass_id)')
result = cur.fetchall()
# print(f"Raw Result 1: {result}")


# Organise data into two list for plotting purposes
age_class, official_time = list(), list()
for r in result:
    age_class.append(r[0])
    official_time.append(r[1])


# Some debug prints
# print(f"Age Class: {age_class}")
# print(f"Official Time: {official_time}")

# Convert official time entries to minutes
official_time = convert_time_to_minutes(time_values_list=official_time)


# Sanity check
# print(f"Official Time (converted into minutes): {official_time}")


# Plot this values using
plt.bar(x=age_class, height=official_time)
plt.xlabel("Age class")
plt.ylabel("Official running time (minutes)")
plt.title("Relation between age and official running time")
plt.show()



# Result 2: Relation between distance and time
cur = con.cursor()
cur.execute(f'SELECT distance, official_time FROM participation_details JOIN event USING(event_id)')
result = cur.fetchall()
print(f"Raw Result 2: {result}")


# Organise data into two list for plotting purposes
distance, official_time = list(), list()
for r in result:
    distance.append(r[0])
    official_time.append(r[1])


# Some debug prints
print(f"Distance: {distance}")
print(f"Official Time: {official_time}")

# Convert official time entries to minutes
official_time = convert_time_to_minutes(time_values_list=official_time)


# Sanity check
# print(f"Official Time (converted into minutes): {official_time}")


# Plot this values using
plt.scatter(x=distance, y=official_time)
plt.xlabel("Running distance (km)")
plt.ylabel("Official running time (minutes)")
plt.title("Relation between running distance and official running time")
plt.show()



# Result 3: Relation between event and sex
cur = con.cursor()
# cur.execute(f'SELECT sex, COUNT(sex), event_type.name FROM runner JOIN participation_details USING(runner_id)JOIN event USING(event_id) JOIN event_type USING(eventtype_id) GROUP BY sex, event_type.name')
cur.execute(f'SELECT sex, eventtype_name FROM runner JOIN participation_details USING(runner_id)JOIN event USING(event_id) JOIN event_type USING(eventtype_id)')
result = cur.fetchall()
# print(f"Raw Result 3: {result}")


# Organise data into two list for plotting purposes
sex, event = list(), list()
for r in result:
    sex.append(r[0])
    event.append(r[1])


# Some debug prints
# print(f"Sex: {sex}")
# print(f"Event: {event}")


# Convert this into dataframe to facilitate plotting
df = {'Sex': sex, 'Event':event}
df = pd.DataFrame.from_dict(data=df)
print(f"DataFrame:\n{df}")

df_group = df.groupby(['Event','Sex']).size().unstack()
# print(df_group)


# Plot
df_group.plot(kind='bar', stacked=False, color=['orchid','blue'])
plt.title("Relation between event and participants' sex")
plt.xlabel('Event')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.legend()
plt.show()




# Result 4: Relation between event year and distance
cur = con.cursor()
cur.execute(f'SELECT event_year, distance  FROM event ')
result = cur.fetchall()
# print(f'Raw Result 4: {result}')


# Organise data into two list for plotting purposes
event_year, distance = list(), list()
for r in result:
    event_year.append(r[0])
    distance.append(r[1])


# Some debug prints
# print(f"Event Year: {event_year}")
# print(f"Distance: {distance}")


# Plot this values using
plt.scatter(x=event_year, y=distance)
plt.xlabel("Event year")
plt.ylabel("Running distance (km)")
plt.title("Relation between event year and running distance")
plt.xticks(event_year)
plt.show()






