import requests
from bs4 import BeautifulSoup
import json5
import re

job_url = "https://dev.bg/company/jobads/yettel-devops-senior-engineer/"
skills_all = []

print("", end="", flush=True)

# Send a GET request to fetch the page content
response = requests.get(job_url)
response.raise_for_status()  # Raise an exception for HTTP errors

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the tech-stack section
tech_stack_section = soup.find('div', class_='tech-stack')

# Find the date-posted section
date = soup.find('li', class_='date-posted')

# Find the location section
location = soup.find('div', class_='job-card-badge location')

# Get only the visible text, strip whitespace
location = location.get_text(strip=True)

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

                work_from = the_data.get("attributes", {}).get("workFrom")
                print(f"workFrom:\n{work_from}\n")          

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

print("Location: ")
print(location)
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

