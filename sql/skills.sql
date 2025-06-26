SELECT count(*) FROM project.skills;

SELECT * FROM project.skills

SELECT skill, COUNT(*) AS skill_count
FROM project.skills
WHERE jobid in (SELECT jobid FROM project.jobs WHERE last_seen = CURDATE())
GROUP BY skill
ORDER BY skill_count DESC
LIMIT 15;