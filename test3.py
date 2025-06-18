import requests
from bs4 import BeautifulSoup
import json5
import re

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


# Print all unique job ad URLs
# print("\nExtracted Job Ad URLs:")
for job_url in sorted(job_urls):
    print(".", end="", flush=True)

    # Send a GET request to fetch the page content
    response = requests.get(job_url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    #print blank row
    print(f"")

    # Find the location section
    location_section = soup.find('div', class_='tags-wrap')

    # Get only the visible text, strip whitespace
    # location = location_section.get_text(strip=True)

    # Extract "София"
    city = location_section.find('a')
    city_text = city.get_text(strip=True) if city else None

    # Extract "Hybrid"
    hybrid = location_section.find('span', class_='suffix-hybrid')
    hybrid_text = hybrid.get_text(strip=True) if hybrid else None

    print("City:", city_text)
    print("Work type:", hybrid_text)
        
    print("URL: ")
    print(job_url)
    print()

    # print("Location: ")
    # print(location_section)
    print()