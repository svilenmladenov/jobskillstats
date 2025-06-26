SELECT * FROM project.jobs_total;
SELECT * FROM project.jobs;
SELECT id FROM jobs_total where date = "2025-06-24" and role = "DevOps";

DELETE FROM jobs_total WHERE id =2

INSERT INTO jobs (id, link, date_posted, company_name, role, job_position, jobid, payment_type, quality_score, value, city, work_type, hrcompany_name, last_seen) 
VALUES (8, "https://dev.bg/company/jobads/a1-bulgaria-senior-checkmk-devops-engineer-m-f-d-a1-competence-delivery-center/", "2025-06-06", "A1 Bulgaria", "DevOps", "Senior Checkmk DevOps Engineer (m/f/d) @ A1 Competence Delivery Center", "444777", "paid", "2", "200", "София", "", "", "2025-06-18")