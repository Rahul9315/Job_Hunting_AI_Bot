from playwright.sync_api import sync_playwright
import json
import time
import os
from tracker import log

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


def apply_job(page, job):
    page.goto(job["link"])
    page.wait_for_timeout(6000)

    # Click the job card so LinkedIn loads the right panel
    try:
        page.locator("li.scaffold-layout__list-item").first.click(timeout=5000)
        page.wait_for_timeout(4000)
    except:
        pass

    # Now Easy Apply exists
    easy_apply = page.locator("button:has-text('Easy Apply')")
    apply_now = page.locator("button:has-text('Apply')")

    if easy_apply.count() == 0 and apply_now.count() == 0:
        return "Skipped (No Easy Apply)"

    if easy_apply.count():
        easy_apply.first.click()
    else:
        apply_now.first.click()

    page.wait_for_timeout(5000)

    # Simple submit
    if page.locator("button:has-text('Submit')").count():
        page.locator("button:has-text('Submit')").click()
        page.wait_for_timeout(4000)
        return "Applied"

    return "Needs Manual Review"


def run():
    with open("data/jobs_filtered.json") as f:
        jobs = json.load(f)


    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        #page = browser.new_page()

        context = load_context(browser)
        page = context.new_page()

        if not os.path.exists("linkedin_cookies.json"):
            login_linkedin(page)


        for job in jobs:
            status = apply_job(page, job)
            log(job, status)
            time.sleep(10)


        browser.close()


if __name__ == "__main__":
    run()