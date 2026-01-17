from pypdf import PdfReader
import json
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT = """
You are an expert recruitment analyst.
Extract structured information from this CV.
Return only valid JSON in this format:
{
"name": "",
"roles": [],
"skills": [],
"experience_years": 0,
"location": "",
"education": [],
"keywords": []
}
"""

def read_cv_text(path="cv.pdf"):
    reader = PdfReader(path)
    return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])

def build_profile():
    text = read_cv_text("cv.pdf")

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=PROMPT + "\nCV:\n" + text
    )

    raw = response.text.strip()
    profile = json.loads(raw)

    os.makedirs("data", exist_ok=True)
    with open("data/cv.json", "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)

    print("CV profile created → data/cv.json")

if __name__ == "__main__":
    build_profile()
