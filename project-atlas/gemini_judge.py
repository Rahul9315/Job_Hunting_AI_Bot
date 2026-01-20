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

You will be given a JOB DESCRIPTION text.
Extract the job details and decide if Rahul should apply.

Return ONLY valid JSON in this format. Do not include any explanation or markdown:

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
- Extract title, company and location ONLY from the job description text
- The role MUST be in software development or software engineering
- Reject roles that are:
  - Data Engineer
  - Data Scientist
  - Cybersecurity
  - IT Support / Helpdesk / SysAdmin
  - Network Engineer
  - DevOps only roles
- Prefer roles that mention:
  - Python, JavaScript, TypeScript, React, Node.js, Backend, Web, API, Cloud, AI, ML
- Entry level, Graduate or Junior roles are ideal, but accept mid-level if skills match
- Visa sponsorship is NOT required for approval
- Apply = true if the role is software development and matches Rahul’s skills
- Apply = false only if the role is clearly not software engineering

"""


def run():
    with open("data/cv.json") as f:
        cv = json.load(f)

    with open("data/jobs_raw.json") as f:
        jobs = json.load(f)

    approved = []

    
    for job in jobs[:2]:
        prompt = f"""{PROMPT}

        CV:
        {json.dumps(cv, indent=2)}

        JOB DESCRIPTION:
        {job['description']}
        """

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

    """
         
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
    # this for loop above this comment has to be removed
    """

    os.makedirs("data", exist_ok=True)
    with open("data/jobs_filtered.json", "w", encoding="utf-8") as f:
        json.dump(approved, f, indent=2)

    print(f"Approved {len(approved)} jobs → data/jobs_filtered.json")

if __name__ == "__main__":
    run()

