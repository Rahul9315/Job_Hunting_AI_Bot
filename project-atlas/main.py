from job_scraper import run as scrape_jobs
from gemini_judge import run as judge_jobs
from linkedin_apply import run as apply_jobs

def main():
    print(" \n\n Scraping JoBs \n\n ")
    scrape_jobs()

    print(" \n🧠 Judging jobs with Gemini...\ ")
    judge_jobs()

    print(" \n🚀 Applying on LinkedIn...\ ")
    apply_jobs()

    print(" \n✔ Atlas pipeline completed successfully\ ")

if __name__ == "__main__":
    main()
