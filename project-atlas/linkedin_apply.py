from playwright.sync_api import sync_playwright
from human_actions import human_sleep, human_type, human_scroll
from tracker import log
import json, time, os

DAILY_CAP = 20

"""
def login_linkedin(page):
    page.goto("https://www.linkedin.com/login")
    page.fill("input#username", os.getenv("LINKEDIN_EMAIL"))
    page.fill("input#password", os.getenv("LINKEDIN_PASSWORD"))
    page.screenshot(path="Linkedin_login.png", full_page=True)
    page.click("button[type=submit]")
    page.wait_for_timeout(12000)
    page.context.storage_state(path="linkedin_cookies.json")

    """

def login_linkedin(page):
    os.makedirs("debug_login", exist_ok=True)

    page.goto("https://www.linkedin.com")
    page.wait_for_timeout(8000)
    #page.screenshot(path="debug_login/1_home.png", full_page=True)

    """
    # Click Sign in (homepage modal)
    page.locator("text=Sign in").first.click()
    page.wait_for_timeout(6000)
    page.screenshot(path="debug_login/2_after_signin.png", full_page=True)
    """

# Click Sign in with Email
    page.locator("text=Sign in with Email").first.click()
    page.wait_for_timeout(6000)
    #page.screenshot(path="debug_login/3_email_click.png", full_page=True)

    # Fill credentials
    page.fill("input#username", os.getenv("LINKEDIN_EMAIL"))
    page.fill("input#password", os.getenv("LINKEDIN_PASSWORD"))
    #page.screenshot(path="debug_login/4_filled.png", full_page=True)

    # Submit
    page.click("button[type=submit]")
    page.wait_for_timeout(15000)
    #page.screenshot(path="debug_login/5_loggedin.png", full_page=True)

    page.context.storage_state(path="linkedin_cookies.json")



def load_context(browser):
    if os.path.exists("linkedin_cookies.json"):
        return browser.new_context(storage_state="linkedin_cookies.json")
    return browser.new_context()




def run():
    with open("data/jobs_filtered.json") as f:
        jobs = json.load(f)


    applied_today = 0


    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True , slow_mo=200)

        context = load_context(browser)
        page = context.new_page()

        #context = browser.new_context()

        if not os.path.exists("linkedin_cookies.json"):
            login_linkedin(page)
       

        page.goto("https://www.linkedin.com")
        page.wait_for_timeout(6000)


        for job in jobs:
            if applied_today >= DAILY_CAP:
                break


            page.goto(job["link"])
            human_sleep(3, 6)
            human_scroll(page)

            page.screenshot(path="debug0/1.png", full_page=True)

            easy_apply = page.locator("button.jobs-apply-button")

            if easy_apply.count() == 0:
                log(job, "Skipped", "No Easy Apply")
                continue

            easy_apply.first.click()
            human_sleep(2, 4)


            # Wait for Easy Apply modal
            page.wait_for_selector("div.jobs-easy-apply-modal", timeout=15000)
            page.screenshot(path="debug0/3.png", full_page=True)


            try:
                # Auto-fill common fields if present
                if page.locator("input[name='phoneNumber']").count():
                    human_type(page, "input[name='phoneNumber']", os.getenv("PHONE", ""))
                
                page.screenshot(path="debug0/4.png", full_page=True)


                # Select already uploaded resume (cv.pdf)
                if page.locator("text=cv.pdf").count():
                    page.locator("text=cv.pdf").first.click()
                    human_sleep(1, 2)


                # Submit flow
                # Step engine: Next → Next → Review → Submit
                while True:
                    if page.locator("button:has-text('Submit')").count():
                        page.locator("button:has-text('Submit')").click()
                        human_sleep(3, 5)
                        log(job, "Applied", "Success")
                        applied_today += 1
                        page.screenshot(path="debug0/5.png", full_page=True)
                        break

                    elif page.locator("button[data-easy-apply-next-button]").count():
                        page.locator("button[data-easy-apply-next-button]").click()
                        human_sleep(3, 5)
                        page.screenshot(path="debug0/step.png", full_page=True)

                    elif page.locator("button:has-text('Review')").count():
                        page.locator("button:has-text('Review')").first.click()
                        human_sleep(3, 5)

                    else:
                        log(job, "Manual Review", "Unknown step")
                        page.screenshot(path="debug0/unknown.png", full_page=True)
                        break



            except Exception as e:
                log(job, "Manual Review", str(e))
                page.screenshot(path="debug0/7.png", full_page=True)


            human_sleep(8, 14)


        browser.close()




if __name__ == "__main__":
    run()