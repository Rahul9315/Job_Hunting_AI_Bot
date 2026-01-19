from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.linkedin.com/login")
    print("👉 Log in manually, then press ENTER here...")
    input()

    context.storage_state(path="linkedin_cookies.json")
    print("✅ Cookies saved")

    browser.close()
