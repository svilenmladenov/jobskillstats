import requests
from bs4 import BeautifulSoup
import json5
import re
import mysql.connector
from datetime import datetime
from datetime import date

# Database connection config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MySvilen',
    'database': 'project'
}

# Base URL pattern
base_url = 'https://dev.bg/company/jobs/devops/?_paged='
page = 1
job_urls = set()  # Use a set to avoid duplicates
jobs_total = 0

try:
    # Connect to database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    while True:
        url = f"{base_url}{page}"
        # print(f"Fetching page {page}: {url}")
        response = requests.get(url)

        if response.status_code != 200:
            print("Page not found or request failed. Stopping.")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all job ad links
        links = soup.find_all('a', href=True)
        page_job_urls = set(
            a['href'] for a in links
            if a['href'].startswith("https://dev.bg/company/jobads/")
        )

        # If no job ads found on the page, assume we've reached the end
        if not page_job_urls:
            # print("No job ads found on this page. Done.")
            break

        job_urls.update(page_job_urls)
        page += 1


    # Print all unique job ad URLs
    for job_url in sorted(job_urls):
        print(f"\n\n------------\n")

        # Initialize an empty list
        skills_all = []

        # Send a GET request to fetch the page content
        response = requests.get(job_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        #print blank row
        print(f"")

        # Find the tech-stack section
        tech_stack_section = soup.find('div', class_='tech-stack')

        # Find the date-posted section
        datejob = soup.find('li', class_='date-posted')

        # Find the location section
        location_section = soup.find('div', class_='tags-wrap')

        # Extract "София"
        city = location_section.find('a')
        city_text = city.get_text(strip=True) if city else None

        # Extract "Hybrid"
        hybrid = location_section.find('span', class_='suffix-hybrid')
        hybrid_text = hybrid.get_text(strip=True) if hybrid else None

        # Find the script section
        script_tags = soup.find_all("script")

        # Search for the one that contains 'the_data'
        for script in script_tags:
            script_text = script.get_text()
            if "the_data" in script_text:
                # Extract just the JS object assigned to the_data
                match = re.search(r"the_data\s*=\s*(\{.*?\});", script_text, re.DOTALL)
                if match:
                    js_obj = match.group(1)

                    try:
                        # Parse with json5 to handle JS-like syntax
                        the_data = json5.loads(js_obj)
                        company_name = the_data.get("attributes", {}).get("companyName")
                        print(f"Company Name: {company_name}")

                        role = the_data.get("attributes", {}).get("jobSubType")
                        print(f"Role: {role}")

                        job_position = the_data.get("attributes", {}).get("jobPosition")
                        print(f"jobPosition: {job_position}")

                        job_id = the_data.get("attributes", {}).get("jobId")
                        print(f"jobId: {job_id}")

                        payment_type = the_data.get("attributes", {}).get("paymentType")
                        print(f"paymentType: {payment_type}")            

                        quality_score = the_data.get("attributes", {}).get("qualityScore")
                        print(f"qualityScore: {quality_score}")     

                        value = the_data.get("attributes", {}).get("value")
                        print(f"value: {value}")  
                    except Exception as e:
                        print("Failed to parse the_data:", e)
                break

        
        print(f"URL: {job_url}")
        print("Date: ", datejob.find('time')['datetime'])
        print(f"City: {city_text}")
        print(f"Work type:  {hybrid_text}")

        hrcompany_span = soup.find('span', class_='company-name')
        hrcompany_name = hrcompany_span.get_text(strip=True) if hrcompany_span else None

        if company_name:  # True if company_name is not None or empty
            hrcompany_name = None

        print(f"HR Agency: {hrcompany_name}")

        if tech_stack_section:
            badges_clickable = tech_stack_section.find_all('div', class_='component-square-badge has-image clickable')
            badges_non_clickable = tech_stack_section.find_all('div', class_='component-square-badge has-image')

            # Combine them
            badges = badges_clickable + badges_non_clickable
            skills = [badge.find('img').get('title') for badge in badges if badge.find('img')]
            skills_all = skills_all + skills


            print("Skills:")
            for skill in skills:
                print(f"- {skill}")
                insert_query = "INSERT INTO skills (skill, jobid) VALUES (%s, %s)"
                cursor.execute(insert_query, (skill, job_id))
                conn.commit()

        # Select check if job already exists
        select_query = "SELECT id FROM project.jobs where link=%s and date_posted=%s and jobid=%s"
        cursor.execute(select_query, (job_url, datejob.find('time')['datetime'], job_id))
        result = cursor.fetchone()

        if not result:
            # Insert query
            insert_query = "INSERT INTO jobs (link, date_posted, company_name, role, job_position, jobid, payment_type, quality_score, value, city, work_type, hrcompany_name, last_seen) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (job_url, datejob.find('time')['datetime'], company_name, role, job_position, job_id, payment_type, quality_score, value, city_text, hybrid_text, hrcompany_name, datetime.today() ))
            # Commit changes
            conn.commit()
            print(f"Inserted with ID: {cursor.lastrowid}")
        else:
            update_query = "UPDATE jobs SET last_seen=%s WHERE link=%s and date_posted=%s and jobid=%s"
            cursor.execute(update_query, (datetime.today(), job_url, datejob.find('time')['datetime'], job_id))
            conn.commit()
            print(f"Updated row with jobID: {job_id}")

        jobs_total = jobs_total + 1

    # Select check if job total for that date already exists
    select_query_totaljobs = "SELECT id FROM jobs_total where date=%s and role=%s"
    cursor.execute(select_query_totaljobs, (date.today(), role))
    resultj = cursor.fetchone()

    if not resultj:
        # Insert query
        insert_query_totaljobs = "INSERT INTO jobs_total (date, jobs_total, role) VALUES (%s, %s, %s)"
        cursor.execute(insert_query_totaljobs, (datetime.today(), jobs_total, role))
        # Commit changes
        conn.commit()
    else:
        update_query_totaljobs = "UPDATE jobs_total SET jobs_total=%s WHERE date = %s and role = %s;"
        cursor.execute(update_query_totaljobs, (jobs_total, datetime.today(), role))
        conn.commit()


    print(f"\n\n---------\nTotal Jobs: {jobs_total}")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
