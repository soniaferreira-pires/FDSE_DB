CREATE TABLE team (
 team_id SERIAL PRIMARY KEY,
 team_name CHARACTER VARYING(100) NOT NULL UNIQUE
);
 
CREATE TABLE runner (
 runner_id SERIAL PRIMARY KEY,
 runner_name VARCHAR NOT NULL,
 sex CHAR(1) NOT NULL CHECK (sex IN ('M', 'F')),
 nation CHAR(2),
 birthdate DATE NOT NULL
);

CREATE TABLE age_class (
 ageclass_id SERIAL PRIMARY KEY,
 age_class VARCHAR(3) NOT NULL UNIQUE
);
 
CREATE TABLE event_type (
 eventtype_id SERIAL PRIMARY KEY,
 eventtype_name VARCHAR(90) NOT NULL UNIQUE
);
 
CREATE TABLE event (
 event_id SERIAL PRIMARY KEY,
 distance INTEGER NOT NULL,
 event_year SMALLINT NOT NULL,
 eventtype_id INTEGER NOT NULL REFERENCES event_type(eventtype_id)
ON DELETE SET NULL ON UPDATE CASCADE
);
 
 
CREATE TABLE participation_details (
 partdet_id SERIAL PRIMARY KEY,
 bib INTEGER NOT NULL,
 official_time TIME NOT NULL,       
 net_time TIME,                    
 place INTEGER NOT NULL,
 place_in_class INTEGER NOT NULL,
 age INTEGER NOT NULL CHECK (age >= 0),    --- field to be calc. with birth_date
 team_id SERIAL REFERENCES team(team_id) ON DELETE SET NULL ON UPDATE CASCADE,
 runner_id SERIAL NOT NULL REFERENCES runner(runner_id) ON DELETE SET NULL ON UPDATE CASCADE,
 ageclass_id SERIAL NOT NULL REFERENCES age_class(ageclass_id) ON DELETE SET NULL ON UPDATE CASCADE,
 event_id SERIAL NOT NULL REFERENCES event(event_id) ON DELETE SET NULL ON UPDATE CASCADE
);
ALTER TABLE participation_details ALTER COLUMN team_id DROP NOT NULL;