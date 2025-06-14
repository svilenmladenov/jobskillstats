import requests
from bs4 import BeautifulSoup
from collections import Counter

# Base URL pattern
base_url = 'https://dev.bg/company/jobs/devops/?_paged='
page = 1
job_urls = set()  # Use a set to avoid duplicates

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

# Initialize an empty list
skills_all = []
# Print all unique job ad URLs
# print("\nExtracted Job Ad URLs:")
for job_url in sorted(job_urls):
    # print(job_url)
    print(".", end="", flush=True)

    # Send a GET request to fetch the page content
    response = requests.get(job_url)
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
        skills_all = skills_all + skills

        # print("Extracted Tech Stack Skills:")
    #     for skill in skills:
    #         print(f"- {skill}")
    # else:
    #     print("Tech Stack section not found.")

# print all collected skills
# for skill in skills_all:
#     print(f"{skill}")

# Count the frequency of each element
skill_counts = Counter(skills_all)
jobs_count = len(job_urls)

#print blank row
print(f"")
# Print each element and its count
for skill, count in skill_counts.most_common():
    print(f"{skill}: {count}   ({count/jobs_count*100:.2f}%)")

# print(len(job_urls))
