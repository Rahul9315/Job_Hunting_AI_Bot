import json
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def load_prompt():
    with open("prompts/gemini_judge.txt", "r", encoding="utf-8") as f:
        return f.read()

PROMPT = load_prompt()


def run():
    with open("data/cv.json") as f:
        cv = json.load(f)

    with open("data/jobs_raw.json") as f:
        jobs = json.load(f)

    approved = []

    
    for job in jobs[:10]: ## change this like to  if u have api paid version else keep it at jobs[:10] ->  for job in jobs: 
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

    TEST_MODE = True
         
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

