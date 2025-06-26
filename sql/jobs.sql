SELECT count(*) FROM jobs;

select * from jobs where company_name = "Wiser Technology"

-- removed jobs
SELECT * FROM jobs where last_seen = CURDATE() - INTERVAL 1 DAY;

-- new jobs
SELECT * FROM jobs where date_posted = CURDATE()

-- diff new - removed jobs for the last day
SELECT
(SELECT count(*) FROM jobs where date_posted = CURDATE()) - 
(SELECT count(*) FROM jobs where last_seen = CURDATE() - INTERVAL 1 DAY) AS difference;