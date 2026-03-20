# InfiOnboard: AI-Adaptive Onboarding Engine
**Team:** Ratnesh Singh Bhandari  
**Hackathon Submission:** AI-Adaptive Learning Engine

---

## Slide 1: Solution Overview
### Value Proposition & Problem-Solving Approach
* **The Problem:** Static, "one-size-fits-all" corporate onboarding wastes experienced hires' time and overwhelms beginners, leading to severe operational inefficiencies.
* **The Solution:** *InfiOnboard*, an AI-driven Adaptive Pathing Engine that dynamically maps personalized training journeys by calculating the exact delta between a candidate's resume and a target job description.
* **Key Features:** 
  * Intelligent PDF parsing for instant skills extraction.
  * Experience-aware gap analysis (Beginner, Intermediate, Advanced).
  * 100% Grounded outputs (Zero Hallucination).

---

## Slide 2: Architecture & Workflow
### System Design & Data Flow
* **Frontend UI:** Glassmorphism React/Tailwind MVP offering seamless PDF Drag & Drop and real-time visualization of learning pathways.
* **FastAPI Backend:** High-performance, async API capable of processing complex NLP extractions.
* **Algorithm Core:** 
  1. Parse PDF `->` Extract Skills.
  2. Parse JD `->` Extract Required Skills.
  3. `Gap = JD(Skills) - Resume(Skills)`.
* **Database:** Strict SQLite integration ensures the system only assigns real-world, approved corporate training courses.

---

## Slide 3: Tech Stack & Models
### Frameworks & LLM Citations
* **Backend:** Python 3.9+, FastAPI, PyPDF (`pdfplumber` equivalent).
* **Frontend:** React (via CDN) + Tailwind CSS + Interactive DOM updates.
* **Simulated/Integrated Models:**
  * **Extraction Engine:** Heuristics based on keyword extraction, simulating the behavior of **Mistral/BERT** models to categorize experience levels and extract cross-domain taxonomies.
  * **Extensibility:** The architecture natively supports `google-generativeai` (Gemini) if a key is provided in the `.env` configuration.

---

## Slide 4: Algorithms & Training
### Our Original "Adaptive Pathing" Logic
* **Knowledge Tracing Core:** Our original implementation operates via a robust Set-Difference mathematical delta (`Gap = JD_Skills - Resume_Skills`).
* **Skill Extraction Logic:** Simulates a bespoke NLP model using sophisticated boundary matching across taxonomies derived from public datasets.
* **Experience Tagging:** Extracts competency markers (e.g., "5+ years", "Senior") to automatically classify a candidate's baseline as Beginner, Intermediate, or Advanced.
* **Graph/Timeline Mapping:** Outputs pathways dynamically ordered from lowest difficulty to highest difficulty to maintain pedagogical integrity, complete with transparent **Reasoning Traces**.

---

## Slide 5: Datasets, Models & Metrics
### Data Transparency & Validation Metrics
* **Public Datasets Utilized (via explicit extraction taxonomy modeling):**
  1. [Kaggle Resume Dataset](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset/data)
  2. [O*NET Database Updates](https://www.onetcenter.org/db_releases.html)
  3. [Kaggle Jobs and Job Description](https://www.kaggle.com/datasets/kshitizregmi/jobs-and-job-description)
* **Open-Source Model Simulation:** Simulates the classification capabilities of **Mistral/BERT** models tailored for HR constraints.
* **Internal Metrics for Validation:**
  * **TTR (Time-To-Readiness):** Calculates hours saved by skipping redundant training via the Adaptive Pathing gap-delta.
  * **Zero-Hallucination Ratio:** Maintains 100% grounding by restricting pathway assignment exclusively to a local SQLite course catalog.
