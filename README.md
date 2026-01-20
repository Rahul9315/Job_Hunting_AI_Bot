# Project Atlas 🤖

### Autonomous LinkedIn Job Application Bot powered by Google Gemini

Project Atlas is a fully automated job hunting system that:

* Finds jobs on LinkedIn
* Filters them using AI (Gemini ATS-style screening)
* Applies automatically using Easy Apply
* Tracks everything in Excel

Built for developers who want interviews, not browser fatigue.

---

## 🚀 Features

* 🔍 LinkedIn Job Scraper (Playwright)
* 🧠 AI Job Judge (Google Gemini Free Tier)
* 🚀 Smart Easy Apply Bot (Stealth Mode)
* 📊 Application Tracker (Excel)
* 🐳 Dockerised – works on any machine
* ⏰ Fully schedulable (runs itself every day)

---

## 🛠 Requirements

### System

* Windows 10/11 (WSL2 recommended) OR macOS OR Linux
* Docker Desktop installed
* Google Chrome installed

### Accounts

* LinkedIn account
* Google account (for Gemini API key)

* Note : If you have paid version of Gemini API then make changes in `gemini_judge.py` line 28 from `for job in jobs[:10] ->  for job in jobs:` as free version will only allow to scan 10 jobs per day

### Note:

* Keep your CV as cv.pdf while replacing the one already their
* Expecting your LinkedIn is already Trained like most of the field is already filled by LinkedIn

---

## 🍴 How to Fork & Run

### 1. Fork the Repository

Click **Fork** on GitHub → clone your fork:

```
git clone https://github.com/Rahul9315/Job_Hunting_AI_Bot.git
cd project-atlas
```

---

### 2. Create `.env` File 

* create new `.env`  or rename `.env.example` file to `.env`  

```
GEMINI_API_KEY=YOUR_GEMINI_KEY
LINKEDIN_EMAIL=your_email
LINKEDIN_PASSWORD=your_password
PHONE=your_phone_number
```

---

### 3. Get Gemini API Key (Free Tier)

1. Go to [https://ai.google.dev](https://ai.google.dev)
2. Create a project → Enable Gemini API
3. Create API Key
4. Paste into `.env`

---

### 4. Build the Container

```
docker compose build
```

---

### 5. Run the Pipeline (One Command)

```
docker compose run atlas
```

This will:

1. Scrape LinkedIn jobs
2. Judge them using Gemini (ATS scan)
3. Apply automatically
4. Save results to `data/applied.xlsx`

---

## 🧠 Customise for Your Role

### Change Target Role & Location

Edit `job_scraper.py`:

```
SEARCHES = [
  {"platform": "linkedin", "query": "Software Engineer Ireland"},
]
```

---

### Change AI Judging Prompt

Edit `promts/gemini_judge.txt` as strict as you wanted but  only make changes in the rules:

```
PROMPT = """
You are a senior recruiter.
Decide if the candidate should apply.
Focus on SOFTWARE ENGINEERING roles.
Reply only YES or NO.
"""
```

---

## ⏰ Run Automatically Every Day

### Windows Task Scheduler

* Program: `docker`
* Arguments: `compose run atlas`
* Start in: `path/to/project-atlas`

### macOS / Linux (cron)

```
0 9 * * * cd /path/to/project-atlas && docker compose run atlas
```

---

## 📊 Output

* `data/applied.xlsx`

| Date | Platform | Company | Role | Location | Status | Note | Link |
| ---- | -------- | ------- | ---- | -------- | ------ | ---- | ---- |

---

## 🔐 Security

* Never commit `.env`
* Use LinkedIn responsibly
* Daily cap built in to avoid bans

---

## 🧭 Roadmap

* Interview Tracker
* Salary Negotiation Assistant
* Offer Comparison Dashboard
* Company Research Bot

---

## 🤝 Contributing

Fork → Improve → PR → Help others get interviews faster

---

## ⭐ Star the Repo

If Atlas helped you land interviews, give it a star and help others win too.

---

Built with ❤️ and caffeine by Rahul
