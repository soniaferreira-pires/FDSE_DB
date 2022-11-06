--a)  Who run the fastest 10K race ever (name, birthdate, time)?
SELECT runner.runner_name, runner.birthdate, participation_details.official_time
FROM runner, participation_details
LEFT JOIN event on event.event_id = participation_details.event_id
WHERE event.distance = '10' AND
	  runner.runner_id = participation_details.runner_id AND 
	  official_time IN (SELECT min(official_time) 
			FROM participation_details)


--b)  What 10K race had the fastest average time (event, event date)?
SELECT event_type.eventtype_name AS event_name, event.event_year, AVG(participation_details.official_time) AS fastest_AVG_time_10kRun
FROM event_type JOIN 
	 event USING(eventtype_id) JOIN 
	 participation_details USING(event_id)
WHERE event.distance = '10'
GROUP BY event_type.eventtype_name, event.event_year
HAVING AVG(participation_details.official_time) <= ALL (
	SELECT AVG(participation_details.official_time)
	FROM participation_details JOIN event USING(event_id) JOIN event_type USING(eventtype_id)
	GROUP BY event_type.eventtype_name, event.event_year
)


--c)  What teams had more than 3 participants in the 2016 maratona  (team)?
SELECT team.team_name, COUNT(participation_details.team_id) AS nr_participants
FROM team JOIN 
	 participation_details  USING(team_id) JOIN 
	 event USING(event_id) JOIN 
	 event_type USING(eventtype_id)
WHERE event.event_year = '2016' AND
      event_type.eventtype_name = 'maratona'
GROUP BY team.team_name
HAVING COUNT(team.team_id) > 3
ORDER BY team.team_name


--d)  What are the 5 runners with more kilometers in total (name, birthdate, kms)?
SELECT runner.runner_name, runner.birthdate, SUM(event.distance) AS sum_kms
FROM runner JOIN 
	 participation_details USING(runner_id) JOIN 
	 event USING(event_id)
GROUP BY runner.runner_name, runner.birthdate
ORDER BY SUM(event.distance) DESC, runner.birthdate ASC
LIMIT 5 


--e)  What was the best time improvement in two consecutive maratona  races (name, birthdate, improvement)?





SELECT t1.runner_name, t1.event_year, t2.event_year, t1.official_time, t2.official_time, t2.official_time - t1.official_time AS time
FROM
	(SELECT * 
		FROM runner JOIN 
		     participation_details USING(runner_id) JOIN
		     event USING(event_id) JOIN
		     event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t1
	JOIN
	(SELECT *
		FROM runner JOIN 
		    participation_details USING(runner_id) JOIN
		    event USING(event_id) JOIN
		    event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t2
		USING (runner_id)
WHERE t1.event_year > t2.event_year
ORDER BY t1.runner_name
LIMIT 50



SELECT runner_name,  event.event_year,
FROM runner JOIN 
	participation_details USING(runner_id) JOIN
	event USING(event_id) JOIN
	event_type USING(eventtype_id)
WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos'
ORDER BY runner_name, event.event_year DESC
LIMIT 50 



-- catia
SELECT t1.runner_name, t1.event_year, t2.event_year, t1.official_time, t2.official_time, t2.official_time - t1.official_time AS time
FROM
	(SELECT * 
		FROM runner JOIN 
		     participation_details USING(runner_id) JOIN
		     event USING(event_id) JOIN
		     event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t1
	JOIN
	(SELECT *
		FROM runner JOIN 
		    participation_details USING(runner_id) JOIN
		    event USING(event_id) JOIN
		    event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t2
		USING (runner_id)
WHERE t1.event_year = t2.event_year + 1
LIMIT 50


-- opção 1
SELECT *
FROM (SELECT t1.runner_name, t1.event_year, t2.event_year, t1.official_time, t2.official_time,  t2.official_time – t1.official_time AS time
FROM
	(SELECT * 
		FROM runner JOIN 
		     participation_details USING(runner_id) JOIN
		     event USING(event_id) JOIN
		     event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t1
	JOIN
	(SELECT *
		FROM runner JOIN 
		    participation_details USING(runner_id) JOIN
		    event USING(event_id) JOIN
		    event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t2
		USING (runner_id)
WHERE t2.event_year = t1.event_year + 1)) AS result
WHERE time <= ALL (SELECT time
		FROM runner JOIN 
		     participation_details USING(runner_id) JOIN
		     event USING(event_id) JOIN
		     event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t1
	JOIN
	(SELECT *
		FROM runner JOIN 
		    participation_details USING(runner_id) JOIN
		    event USING(event_id) JOIN
		    event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t2
		USING (runner_id)
WHERE t2.event_year = t1.event_year + 1)
)

--opcç\ao2
SELECT *
	FROM 
	(SELECT t1.runner_name, t1.event_year, t2.event_year, t1.official_time, t2.official_time,  t2.official_time – t1.official_time AS time
		FROM
		(SELECT * 
			FROM runner JOIN 
			     participation_details USING(runner_id) JOIN
			     event USING(event_id) JOIN
			     event_type USING(eventtype_id)
			WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t1
		JOIN
		(SELECT *
			FROM runner JOIN 
			    participation_details USING(runner_id) JOIN
			    event USING(event_id) JOIN
			    event_type USING(eventtype_id)
			WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t2
			USING (runner_id)
		WHERE t2.event_year = t1.event_year + 1)) AS result
		WHERE time = min(SELECT time
				FROM runner JOIN 
				     participation_details USING(runner_id) JOIN
				     event USING(event_id) JOIN
				     event_type USING(eventtype_id)
				WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t1
			JOIN
			(SELECT *
				FROM runner JOIN 
				    participation_details USING(runner_id) JOIN
				    event USING(event_id) JOIN
				    event_type USING(eventtype_id)
				WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t2
				USING (runner_id)
		WHERE t2.event_year = t1.event_year + 1) as t4
)



#-----
SELECT *
FROM (SELECT t1.runner_name, t1.event_year, t2.event_year, t1.official_time, t2.official_time,  t2.official_time – t1.official_time AS time
FROM
	(SELECT * 
		FROM runner JOIN 
		     participation_details USING(runner_id) JOIN
		     event USING(event_id) JOIN
		     event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t1
	JOIN
	(SELECT *
		FROM runner JOIN 
		    participation_details USING(runner_id) JOIN
		    event USING(event_id) JOIN
		    event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t2
		USING (runner_id)
WHERE t2.event_year = t1.event_year + 1)) AS result
WHERE time = min(SELECT time
		FROM runner JOIN 
		     participation_details USING(runner_id) JOIN
		     event USING(event_id) JOIN
		     event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t1
	JOIN
	(SELECT *
		FROM runner JOIN 
		    participation_details USING(runner_id) JOIN
		    event USING(event_id) JOIN
		    event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'maratona' and runner_name = 'Abel Santos') AS t2
		USING (runner_id)
WHERE t2.event_year = t1.event_year + 1) as subq
)







--Extra points: Think of other interesting questions to ask!
-- top runners for each distance 
SELECT DISTINCT runner.runner_name, event_type.eventtype_name , event.distance, event.event_year
    FROM runner JOIN 
    	   participation_details USING (runner_id) JOIN 
    	   event USING (event_id) JOIN
    	   event_type USING (eventtype_id)
	WHERE (event.distance, official_time) IN(
	SELECT event.distance, MIN(official_time)
	FROM participation_details JOIN event USING (event_id)
	GROUP BY event.distance
	)
ORDER BY event.distance






