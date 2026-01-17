from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv


load_dotenv()


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.linkedin.com")
        page.wait_for_timeout(5000)
        print("LinkedIn opened successfully")
        browser.close()


if __name__ == "__main__":
    main()