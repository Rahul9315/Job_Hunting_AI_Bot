from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv


load_dotenv()

SEARCHES = [
    {"platform": "indeed", "query": "Junior Software developer Ireland"},
    {"platform": "linkedin", "query": "Junior Software Engineer Ireland"}
]




def scrape_indeed(page, query):
    url = f"https://www.indeed.com/jobs?q={query.replace(' ', '+')}"
    page.goto(url)

    page.wait_for_timeout(5000)
    page.screenshot(path="Indeed.png", full_page=True)
    soup = BeautifulSoup(page.content(), "html.parser")
    jobs = []


    for card in soup.select("a.tapItem")[:20]:
        title = card.select_one("h2.jobTitle span")
        company = card.select_one("span.companyName")
        link = "https://www.indeed.com" + card.get("href")


        jobs.append({
            "platform": "Indeed",
            "title": title.text.strip() if title else "",
            "company": company.text.strip() if company else "",
            "location": "Ireland",
            "link": link
        })


    return jobs


def login_linkedin(page):
    page.goto("https://www.linkedin.com/login")
    page.fill("input#username", os.getenv("LINKEDIN_EMAIL"))
    page.fill("input#password", os.getenv("LINKEDIN_PASSWORD"))
    page.screenshot(path="Linkedin_login.png", full_page=True)
    page.click("button[type=submit]")
    page.wait_for_timeout(12000)
    page.context.storage_state(path="linkedin_cookies.json")


def load_context(browser):
    if os.path.exists("linkedin_cookies.json"):
        return browser.new_context(storage_state="linkedin_cookies.json")
    return browser.new_context()

def scrape_linkedin(page, query):
    #url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}&location=Ireland" # all jobs including easy apply
    url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}&location=Ireland&f_AL=true" # easy apply jobs only link
    page.goto(url)
    page.wait_for_timeout(8000)

    cards = page.locator("li.scaffold-layout__list-item")
    count = cards.count()
    print(f"LinkedIn cards found: {count}")

    jobs = []

    for i in range(min(25, count)):
        card = cards.nth(i)
        card.scroll_into_view_if_needed()
        card.click()
        page.wait_for_timeout(2000)

        jobs.append({
            "platform": "LinkedIn",
            "link": page.url
        })

    return jobs






def run():
    all_jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = load_context(browser)
        page = context.new_page()

        if not os.path.exists("linkedin_cookies.json"):
            login_linkedin(page)

        for s in SEARCHES:
            if s["platform"] == "indeed":
                i = 0
                #all_jobs.extend(scrape_indeed(page, s["query"]))
            else:
                all_jobs.extend(scrape_linkedin(page, s["query"]))

        browser.close()

    os.makedirs("data", exist_ok=True)
    with open("data/jobs_raw.json", "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"Collected {len(all_jobs)} jobs → data/jobs_raw.json")



if __name__ == "__main__":
    run()