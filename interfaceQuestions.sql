-- search runner (everything about the runner)
SELECT * 
FROM runner
WHERE name = '' -- insert name here

-- or just the name and id
SELECT runner_id, name
FROM runner
WHERE name = '' -- insert name here

-- show a specific race 
SELECT event.event_id, event_type.name 
FROM event JOIN event_type USING (eventtype_id)
Where name = '' -- insert name here

-- or show every race tha the runner has competed in
SELECT runner.name, eventtype.NAME
FROM runner JOIN participation_details USING (runner_id) JOIN event_type USING (eventtype_id)

-- top runner overall
SELECT runner.name, event.distance
FROM runner JOIN participation_details USING (runner_id) JOIN event USING (event_id)
GROUP BY runner.name, event.distance, official_time
HAVING official_time <= ALL(
    SELECT official_time FROM participation_details
)

-- top runners for each distance
SELECT DISTINCT runner.name, event.distance
FROM runner JOIN participation_details USING (runner_id) JOIN event USING (event_id)
WHERE (event.distance, official_time) IN(
SELECT event.distance, MIN(official_time)
FROM participation_details JOIN event USING (event_id)
GROUP BY event.distance
)

ORDER BY event.distance

------------------PLOTS

-- age and time
SELECT age_class, official_time
FROM participation_details JOIN age_class USING(ageclass_id)

-- distance vs time
SELECT distance, official_time
FROM participation_details JOIN event USING(event_id)

-- event vs sex
SELECT sex, event_type
FROM runner JOIN participation_details USING(runner_id)JOIN event_type USING(eventtype_id)

-- event year vs distance
SELECT event_year, distance 
FROM event 

-- team vs time
SELECT team.name, event.distance
FROM team JOIN participation_details USING (team_id) JOIN event USING(event_id)