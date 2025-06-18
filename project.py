import requests
from bs4 import BeautifulSoup
import json5
import re
import mysql.connector
from datetime import datetime

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
    # print("\nExtracted Job Ad URLs:")
    for job_url in sorted(job_urls):
        print(".", end="", flush=True)

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
        date = soup.find('li', class_='date-posted')

        # Find the location section
        location_section = soup.find('div', class_='tags-wrap')

        # Extract "София"
        city = location_section.find('a')
        city_text = city.get_text(strip=True) if city else None

        # Extract "Hybrid"
        hybrid = location_section.find('span', class_='suffix-hybrid')
        hybrid_text = hybrid.get_text(strip=True) if hybrid else None

        # Find the script section
        # Find all <script> tags
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
                        print(f"Company Name:\n{company_name}\n")

                        role = the_data.get("attributes", {}).get("jobSubType")
                        print(f"Role:\n{role}\n")

                        job_position = the_data.get("attributes", {}).get("jobPosition")
                        print(f"jobPosition:\n{job_position}\n")

                        job_id = the_data.get("attributes", {}).get("jobId")
                        print(f"jobId:\n{job_id}\n")

                        payment_type = the_data.get("attributes", {}).get("paymentType")
                        print(f"paymentType:\n{payment_type}\n")            

                        quality_score = the_data.get("attributes", {}).get("qualityScore")
                        print(f"qualityScore:\n{quality_score}\n")     

                        value = the_data.get("attributes", {}).get("value")
                        print(f"value:\n{value}\n")  
                    except Exception as e:
                        print("Failed to parse the_data:", e)
                break

        
        print("URL: ")
        print(job_url)
        print()

        print("Date: ")
        print(date.find('time')['datetime'])
        print()

        print("City:", city_text)
        print("Work type:", hybrid_text)

        hrcompany_span = soup.find('span', class_='company-name')
        hrcompany_name = hrcompany_span.get_text(strip=True) if hrcompany_span else None

        if company_name:  # True if company_name is not None or empty
            hrcompany_name = None

        print("HR Agency: ")
        print(hrcompany_name)
        print()

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

        # Insert query
        insert_query = "INSERT INTO jobs (link, date_posted, company_name, role, job_position, jobid, payment_type, quality_score, value, city, work_type, hrcompany_name, last_seen) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (job_url, date.find('time')['datetime'], company_name, role, job_position, job_id, payment_type, quality_score, value, city_text, hybrid_text, hrcompany_name, datetime.today() ))

        # Commit changes
        conn.commit()

    print(f"Inserted with ID: {cursor.lastrowid}")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
