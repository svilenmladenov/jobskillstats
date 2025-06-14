import requests
from bs4 import BeautifulSoup

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
print("\nExtracted Job Ad URLs:")
for job_url in sorted(job_urls):
    print(job_url)
