import json
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

TEST_MODE = True

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT = """
You are a senior technical recruiter in Ireland.

Open this job link and analyze it.

Return ONLY valid JSON in this format:

{
  "title": "",
  "company": "",
  "location": "",
  "skills": [],
  "salary": "",
  "visa_sponsorship": true,
  "apply": true,
  "reason": ""
}

Rules:
- apply = true only if suitable for Rahul
- Rahul is a junior software developer in Ireland
- He needs visa sponsorship
- Focus on entry level / graduate / junior roles
- Prefer Python, JavaScript, web, backend, AI
- If visa is not mentioned, infer from company size & wording
"""

def run():
    with open("data/cv.json") as f:
        cv = json.load(f)

    with open("data/jobs_raw.json") as f:
        jobs = json.load(f)

    approved = []

    """
    for job in jobs[:2]:
        prompt = f"{PROMPT}\n\nCV:\n{json.dumps(cv, indent=2)}\n\nJOB LINK:\n{job['link']}"
        response = client.models.generate_content(
            model="models/gemini-3-flash-preview",
            contents=[{"role": "user", "parts":[{"text": prompt}]}]
        )

        time.sleep(8)

        raw = response.text.strip()
        start = raw.find("{")
        end = raw.rfind("}") + 1
        data = json.loads(raw[start:end])

        data["platform"] = job["platform"]
        data["link"] = job["link"]

        if data["apply"]:
            approved.append(data)

    ###   """
         
    for job in jobs[:2]:

        if TEST_MODE:
            fake = {
                "title": "Junior Software Engineer",
                "company": "Test Company Ltd",
                "location": "Ireland",
                "skills": ["Python", "JavaScript", "Docker"],
                "salary": "€35,000 - €45,000",
                "visa_sponsorship": True,
                "apply": True,
                "reason": "Entry level role matching Rahul's profile"
            }
            fake["platform"] = job["platform"]
            fake["link"] = job["link"]
            approved.append(fake)
            continue

    # real Gemini call goes here later
     

    os.makedirs("data", exist_ok=True)
    with open("data/jobs_filtered.json", "w", encoding="utf-8") as f:
        json.dump(approved, f, indent=2)

    print(f"Approved {len(approved)} jobs → data/jobs_filtered.json")

if __name__ == "__main__":
    run()

