import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&ts=1604582843569&limit={LIMIT}"


def extract_indeed_pages():
    result = requests.get(f"{URL}")
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class:", "pagination"})
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    last_page = pages[-1]
    return last_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company_anchor is not None:
        company = company.find("a").string
    else:
        company = company.string
    company = company.strip("\n")
    location = html.find("span", {"class": "location"})
    if location is not None:
        location = html.find("span", {"class": "location"}).string
    else:
        location = html.find("div", {"class": "location"}).string
    job_id = html["data-jk"]
    return {
        'title': title,
        'company': company,
        'location': location,
        "link": f"https://kr.indeed.com/rc/clk?jk={job_id}"
    }


def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}...")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


max_page = extract_indeed_pages()
list_of_jobs = extract_indeed_jobs(max_page)
for i in range(len(list_of_jobs)):
    print(list_of_jobs[i])
