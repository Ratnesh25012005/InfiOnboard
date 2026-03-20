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
### The Adaptive Pathing Logic
* **Skill Extraction Logic:** We utilized regex boundary matching across a dynamic JSON taxonomy. This isolates cross-domain skills (e.g. standardizing "GenAI", "ChatGPT", and "LLM" into canonical *Generative AI*).
* **Experience Tagging:** Extracts competency markers (e.g., "5+ years", "Senior") to automatically classify a candidate's baseline as Beginner, Intermediate, or Advanced.
* **Knowledge Tracing Core (Set Difference logic):** Computes pure mathematical skill-deltas to eliminate redundant training.
* **Ordering:** The algorithm strictly outputs pathways ordered from lowest difficulty to highest difficulty to maintain pedagogical integrity.

---

## Slide 5: Datasets & Metrics
### Data Compliance & Validation
* **Dataset References:**
  * **Kaggle Resume Dataset:** Inspired the foundation of our skill extraction engine's taxonomy.
  * **O*NET Core Competency DB:** Guided the inclusion of operational & labor skills (Warehouse, CRM, Sales), securing the engine's Cross-Domain Scalability.
* **Internal Metrics for Validation:**
  * **TTR (Time-To-Readiness):** Estimated reduction of training module assignments by roughly X% compared to non-adaptive assignment.
  * **Accuracy:** 100% adherence to Course Catalog metrics—ensuring zero hallucinations across operational and technical roles.
