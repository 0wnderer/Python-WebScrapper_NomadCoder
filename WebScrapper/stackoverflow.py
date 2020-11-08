import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python"


def extract_stackoverflow_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pagination[-2].get_text(strip=True)
    return int(last_page)


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page-84):
        print(f"page {page + 1}...")
        result = requests.get(f"{URL}&page={page + 1}")
        soup = BeautifulSoup(result.text, "html.parser")
        job_list = soup.find("div", {"class": "listResults"}).find_all("a", {"class": "s-link"})
        for i in range(len(job_list)):
            jobs.append(job_list[i].string)
    for i in range(len(jobs)):
        print(jobs[i])


extract_jobs(extract_stackoverflow_pages())
