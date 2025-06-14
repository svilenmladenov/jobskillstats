import requests
from bs4 import BeautifulSoup

# URL of the job listing
url = 'https://dev.bg/company/jobads/bulwork-azure-infrastructure-engineer/'

# Send a GET request to fetch the page content
response = requests.get(url)
response.raise_for_status()  # Raise an exception for HTTP errors

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the tech-stack section
tech_stack_section = soup.find('div', class_='tech-stack')

if tech_stack_section:
    badges_clickable = tech_stack_section.find_all('div', class_='component-square-badge has-image clickable')
    badges_non_clickable = tech_stack_section.find_all('div', class_='component-square-badge has-image')

    # Combine them
    badges = badges_clickable + badges_non_clickable
    skills = [badge.find('img').get('title') for badge in badges if badge.find('img')]

    # print("Extracted Tech Stack Skills:")
    for skill in skills:
        print(f"- {skill}")
else:
    print("Tech Stack section not found.")
