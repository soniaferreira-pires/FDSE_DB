--a)  Who run the fastest 10K race ever (name, birthdate, time)?
SELECT runner.runner_name, runner.birthdate, participation_details.official_time
FROM runner, participation_details
LEFT JOIN event on event.event_id = participation_details.event_id
WHERE event.distance = '10' AND
	  runner.runner_id = participation_details.runner_id AND 
	  official_time IN (SELECT min(official_time) 
			FROM participation_details)



--b)  What 10K race had the fastest average time (event, event date)?
SELECT event_type.eventtype_name AS event_name, event.event_year, AVG(participation_details.official_time)
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
SELECT team.team_name, COUNT(participation_details.team_id)
FROM team JOIN 
	 participation_details  USING(team_id) JOIN 
	 event USING(event_id) JOIN 
	 event_type USING(eventtype_id)
WHERE event.event_year = '2016' AND
      event_type.eventtype_name = 'maratona'
GROUP BY team.team_name
HAVING COUNT(team.team_id) > 3



--d)  What are the 5 runners with more kilometers in total (name, birthdate, kms)?
--------
--- quando a BD tiver completa ver se vale a pena fazer por evento mais recent dos que tem mais totais 
--- ou fazer questão extra para isto
--------
SELECT runner.runner_name, runner.birthdate, SUM(event.distance) AS kms
FROM runner JOIN 
	 participation_details USING(runner_id) JOIN 
	 event USING(event_id)
GROUP BY runner.runner_name, runner.birthdate
ORDER BY SUM(event.distance) DESC
LIMIT 5 


--e)  What was the best time improvement in two consecutive maratona  races (name, birthdate, improvement)?


SELECT first.runner_name, first.event_year, second.event_year, second.eventtype_name, second.official_time - first.official_time AS time
FROM
	(SELECT * 
		FROM runner JOIN 
		     participation_details USING(runner_id) JOIN
		     event USING(event_id) JOIN
		     event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'dia-do-pai') AS first
	JOIN
	(SELECT *
		FROM runner JOIN 
		    participation_details USING(runner_id) JOIN
		    event USING(event_id) JOIN
		    event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'dia-do-pai') AS second
		USING (runner_id)
WHERE first.event_year > second.event_year











SELECT first.runner_name, second.official_time - first.official_time FROM
	(SELECT * 
		FROM runner JOIN 
		     participation_details USING(runner_id) JOIN
		     event USING(event_id) JOIN
		     event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'dia-do-pai' AND
			event.event_year = '2012' ) AS first
	JOIN
	(SELECT *
		FROM runner JOIN 
		    participation_details USING(runner_id) JOIN
		    event USING(event_id) JOIN
		    event_type USING(eventtype_id)
		WHERE event_type.eventtype_name = 'dia-do-pai' AND
			event.event_year = '2013' ) AS second
		USING (runner_id)
WHERE second.official_time - first.official_time >= ALL (
	SELECT second.official_time - first.official_time
	FROM participation_details AS first JOIN
	     participation_details AS second USING (runner_id) JOIN
	     event USING(event_id) JOIN
	     event_type USING(eventtype_id)
	WHERE (first.eventtype_name = 'dia-do-pai' AND first.event_year = '2012') AND
		(second.eventtype_name = 'dia-do-pai' AND second.event_year = '2012')
)









--Extra points: Think of other interesting questions to ask!