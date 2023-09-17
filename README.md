# Databases - Running Races of Portugal
#### FEUP, Faculty of Engineering, University of Porto Master in Data Science and Enginnering
##### Cátia Teixeira, Maria Beatriz Gonçalves, Sónia Ferreira
##### Databases, October 2022
---

<br>
This project regards the design of a database for the races of Portugal (running races), using 
the tools of SQL and Python and it’s constituted by the following steps:   
   
<br>
<br>

**1.   Creation of the UML (uml.png file) and Relational Model (relational.txt):**   
Based on the fields provided on the excel file, a UML model of the database was 
created and the related relation model. Several decisions were made like calculating 
the age based on the birth date of the runner, create a separated tables for certain 
details, like event type, age class, etc. 

<br>

**2.   Creation of SQL script (races.sql):**    
This script will create the tables in the database.

<br>

**3.   Load the Data into the Data Base (load_races.py):**   
To load the data form python into the SQL database several actions were done since 
the excel file was not compliant with the format of the database tables and contains 
many errors. Some of that actions were:
* Conversion of the data types;
* Remove duplicated lines;
* Creation of a Age Class table with an automatic determination;
* Treat the null entries 
* Check backlash cells;

<br>

**4.   User Interface (races.py):**   
An interface that allows to manage and interact with the races database. 
At the moment, a few functionalities were developed like:
* Read, delete, update, insert a record for runners where validations were 
put in place to not allow the user to insert wrong information on the 
database,
* FAQS: allows the user to consult some information from the database.

<br>

**5.   SQL questions(question.sql):**   
Pure SQL questions answering specific asked questions.

<br>

**6.   Extra (extra.py):**   
In order to extract some meaningful information from the database four plots were 
achieved:
* Relation between age and time
* Relation between distance and time
* Relation between event and sex
* Relation between event year and distance
