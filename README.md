# InfiOnboard — AI-Adaptive Onboarding Engine

> **Hackathon Submission** · Personalized training pathways powered by Intelligent NLP Parsing, Cross-Domain Skill-Gap Analysis, and a zero-hallucination SQLite course catalog.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-009688?style=flat&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-CDN-38B2AC?style=flat&logo=tailwind-css&logoColor=white)
![PyPDF](https://img.shields.io/badge/PyPDF-3.0+-blue?style=flat&logo=pdf&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat&logo=docker&logoColor=white)

---

## What It Does

InfiOnboard is an AI-Adaptive Onboarding Engine that:

1. **Intelligent Parsing**: Accepts a Resume (PDF) and a Job Description. Our NLP engine extracts both technical skills *and* experience levels (Beginner, Intermediate, Advanced).
2. **Dynamic Mapping**: Identifies the exact skill deltas, then queries an operational SQLite catalog.
3. **Reasoning Trace**: Generates a grounded, ordered learning pathway with full reasoning traces explaining *why* courses were assigned.
4. **Cross-Domain Scalability**: Fully supports technical (Python, AWS, React) AND operational roles (B2B Sales, Warehouse Logistics, HR Compliance).

---

## Architecture & Data Flow

```
┌──────────────────────────────────────────────────────┐
│                    Browser (Frontend)                │
│   React-CDN + Tailwind — Drag & Drop PDF Interface  │
│   PDF File + Textarea (JD) → FormData → POST /analyze│
└──────────────────┬───────────────────────────────────┘
                   │ HTTP/Multipart
┌──────────────────▼───────────────────────────────────┐
│               FastAPI Backend (main.py)              │
│   Adaptive Pathing Algorithm:                        │
│   1. PyPDF extract_text()                            │
│   2. process_nlp_extraction(resume) → {skill: level} │
│   3. process_nlp_extraction(jd)     → {skill: level} │
│   4. gap = jd_skills - resume_skills (Set Difference)│
│   5. get_courses_for_skills(gap)                     │
└──────────────────┬───────────────────────────────────┘
                   │ sqlite3
┌──────────────────▼───────────────────────────────────┐
│           SQLite Database (catalog.db)               │
│   Table: courses (id, title, skill_tag, level, etc.) │
│   16 seeded courses (Tech, GenAI, Sales, Warehouse)  │
└──────────────────────────────────────────────────────┘
```

---

## Models & Data Compliance (Judging Criteria)

- **Simulated NLP Algorithm:** The skill and experience extraction engine strategically simulates a Mistral/BERT model by classifying resume text using a deep taxonomy and contextual keyword frequency.
- **Kaggle Resume Dataset:** Inspired the foundation of our robust skill taxonomy mapping list.
- **O*NET Core Competency DB:** Guided our expansion into non-technical, cross-domain operational labor skills like "Warehouse Safety", "CRM Management", and "OSHA Compliance".

> **Zero-Hallucination Guarantee**: Courses are only assigned if they exist in `catalog.db`. The generative logic determines the path, but the assignments are 100% grounded in corporate reality.

---

## Setup & Running

### Prerequisites
- Python 3.9+ OR Docker installed
- Git

### Running Local Python Server

```bash
# Clone the repository
git clone https://github.com/Ratnesh25012005/InfiOnboard.git
cd InfiOnboard

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\activate   # Windows
# OR source venv/bin/activate # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start the server
python run.py
```
Open **http://localhost:8000**

### Running via Docker (Judging Environment)

We have provided a Dockerized environment for seamless hackathon judging.
```bash
docker build -t infionboard .
docker run -p 8000:8000 infionboard
```
Open **http://localhost:8000**

---

## Technical Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | ≥0.135 | Async web framework |
| `uvicorn` | ≥0.42 | ASGI server |
| `pydantic` | ≥2.0 | Schema validation |
| `pypdf` | ≥3.0 | PDF Resume extraction engine |
| `python-multipart`| ≥0.0.22| Form data handling for file uploads |
| SQLite3 | Built-in | Course catalog database |

---

## Team

**Ratnesh Singh Bhandari** · AI-Adaptive Onboarding Challenge 2026
