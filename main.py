"""
main.py — InfiOnboard FastAPI Backend
Adaptive Pathing Algorithm: skill-gap analysis, experience tracing, and learning pathway generation.
"""
import re
import os
import io
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, File, UploadFile, Form, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pypdf import PdfReader
from database import init_db, get_courses_for_skills, get_all_courses

# ─────────────────────────────────────────────
# Lifespan (replaces deprecated @app.on_event)
# ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("[InfiOnboard] Server started. Catalog database initialized.")
    yield

# ─────────────────────────────────────────────
# App Setup
# ─────────────────────────────────────────────
app = FastAPI(
    title="InfiOnboard API",
    description="AI-Adaptive Onboarding Engine — Skill Gap Analysis & Learning Pathway Generator",
    version="1.1.0",
    lifespan=lifespan,
)

# Versioned router
v1 = APIRouter(prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend-react", "dist")
# Mount Vite's asset folder specifically to match the build output /assets/
if os.path.exists(os.path.join(FRONTEND_DIR, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")

# ─────────────────────────────────────────────
# Skill Keyword Taxonomy
# All recognized skills and their aliases
# ─────────────────────────────────────────────
SKILL_TAXONOMY = {
    "python": ["python", "py", "django", "flask", "fastapi", "pandas", "numpy", "scipy"],
    "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite", "t-sql", "plsql", "rdbms", "database query"],
    "react": ["react", "reactjs", "react.js", "jsx", "tsx", "next.js", "nextjs"],
    "aws": ["aws", "amazon web services", "ec2", "s3", "lambda", "cloudformation", "iam", "vpc", "eks"],
    "docker": ["docker", "containerization", "containers", "dockerfile"],
    "machine learning": ["machine learning", "ml", "deep learning", "dl", "neural network", "tensorflow", "pytorch", "scikit", "sklearn", "ai model"],
    "typescript": ["typescript", "ts", "angular"],
    "fastapi": ["fastapi", "fast api", "rest api", "restful api", "api development"],
    "kubernetes": ["kubernetes", "k8s", "helm", "kubectl", "orchestration"],
    "tableau": ["tableau", "data visualization", "power bi", "powerbi", "looker", "superset", "charting", "dashboards"],
    "agile": ["agile", "scrum", "kanban", "sprint", "jira", "confluence", "project management"],
    "generative ai": ["generative ai", "genai", "llm", "large language model", "gpt", "chatgpt", "prompt engineering", "rag", "langchain"],
    "sales": ["sales", "b2b", "negotiation", "crm", "salesforce", "pipeline", "outbound"],
    "warehouse": ["warehouse", "logistics", "supply chain", "inventory", "forklift", "osha", "safety"],
    "customer success": ["customer success", "client relations", "onboarding", "nps", "churn", "retention"],
    "hr": ["hr", "human resources", "compliance", "employee relations", "dei", "recruiting", "talent"]
}

# ─────────────────────────────────────────────
# NLP Extraction Engine (Kaggle Resume Dataset & O*NET inspired)
# ─────────────────────────────────────────────
_EXPERT_KW   = ["expert", "senior", "lead", "advanced", "architect", "5+ years", "10 years", "principal", "staff engineer"]
_BEGINNER_KW = ["junior", "beginner", "entry", "intern", "familiar", "learning", "basic", "fundamental", "exposure", "novice"]
_WINDOW = 60  # characters around a skill mention to search for experience markers


def _detect_level_near(text: str, match_start: int) -> str:
    """Find experience level within a proximity window around the skill mention."""
    start = max(0, match_start - _WINDOW)
    end   = min(len(text), match_start + _WINDOW)
    window = text[start:end]
    if any(k in window for k in _EXPERT_KW):
        return "Advanced"
    if any(k in window for k in _BEGINNER_KW):
        return "Beginner"
    return None


def process_nlp_extraction(text: str) -> dict:
    """
    Adaptive NLP extraction engine.
    Extracts skill tokens and infers experience level per-skill using
    proximity window matching (inspired by Kaggle Resume & O*NET datasets).
    Returns a dict mapping canonical skill names to experience levels.
    """
    text_lower = text.lower()
    extracted = {}

    # Document-level fallback experience (for skills with no nearby marker)
    doc_level = "Intermediate"
    if any(k in text_lower for k in _EXPERT_KW):
        doc_level = "Advanced"
    elif any(k in text_lower for k in _BEGINNER_KW):
        doc_level = "Beginner"

    for canonical, aliases in SKILL_TAXONOMY.items():
        for alias in aliases:
            pattern = r'\b' + re.escape(alias) + r'\b'
            match = re.search(pattern, text_lower)
            if match:
                # Try proximity window first; fall back to doc-level
                level = _detect_level_near(text_lower, match.start()) or doc_level
                extracted[canonical] = level
                break
    return extracted


def build_reasoning_trace(skill: str, course: dict, candidate_level: str = None) -> str:
    """
    Build an enriched reasoning trace for a course assignment.
    Explains the skill gap, why this difficulty level was selected, and what the course covers.
    """
    level_reason = {
        "Beginner":     "Candidate has no prior exposure to this skill — starting from fundamentals.",
        "Intermediate": "Candidate has foundational knowledge but lacks professional depth.",
        "Advanced":     "Candidate profile indicates seniority — advanced application required.",
    }
    rationale = level_reason.get(course["level"], "Level matched to skill gap analysis.")
    return (
        f"Gap: Resume missing '{skill.title()}' · JD requires it. "
        f"Level assigned: {course['level']}. "
        f"{rationale} "
        f"→ Assigned: {course['title']} ({course['duration_hours']}h)"
    )


# ─────────────────────────────────────────────
# Request / Response Models
# ─────────────────────────────────────────────
class AnalyzeRequest(BaseModel):
    resume_text: str
    jd_text: str

    class Config:
        json_schema_extra = {
            "example": {
                "resume_text": "Experienced Java developer with SQL skills and 3 years building REST APIs.",
                "jd_text": "Looking for a Python developer with React, AWS, Docker, and Machine Learning experience."
            }
        }


class CourseItem(BaseModel):
    id: int
    title: str
    skill_tag: str
    duration_hours: int
    level: str
    description: str
    resource_type: str
    resource_link: str
    matched_skill: str
    reasoning: str


class AnalyzeResponse(BaseModel):
    resume_skills: dict
    jd_skills: dict
    skill_gap: list
    common_skills: list
    pathway: list
    total_hours: int
    total_catalog_hours: int   # hours if full catalog was assigned (for TTR savings calc)
    ttr_saved_hours: int       # hours saved vs full catalog
    summary: str


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def serve_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "InfiOnboard API is running. Frontend not found."}


# ── Mount versioned routes on both /api (legacy) and /api/v1 ──────────────────


@v1.get("/health")
@app.get("/api/health")  # legacy compat
async def health_check():
    courses = get_all_courses()
    return {
        "status": "healthy",
        "version": "1.1.0",
        "catalog_size": len(courses),
        "message": "InfiOnboard API is running"
    }


@v1.get("/catalog")
@app.get("/api/catalog")  # legacy compat
async def get_catalog():
    """Return all courses in the training catalog."""
    courses = get_all_courses()
    return {"courses": courses, "total": len(courses)}


@v1.post("/analyze", response_model=AnalyzeResponse)
@app.post("/api/analyze", response_model=AnalyzeResponse)  # legacy compat
async def analyze(
    resume_file: UploadFile = File(None),
    resume_text: str = Form(None),
    jd_text: str = Form(...)
):
    """
    Adaptive Pathing Algorithm:
    1. Extract text from PDF (if uploaded) or use raw text
    2. Extract skills & experience levels from Resume via simulated NLP
    3. Extract required skills from JD text
    4. Compute gap = JD skills - Resume skills
    5. Query SQLite catalog for matching courses
    6. Build reasoning traces and return structured pathway
    """
    # Handle Resume Input
    final_resume_text = ""
    if resume_file and resume_file.filename and resume_file.filename.lower().endswith('.pdf'):
        try:
            content = await resume_file.read()
            pdf = PdfReader(io.BytesIO(content))
            final_resume_text = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {str(e)}")
    elif resume_text:
        final_resume_text = resume_text.strip()
        
    if not final_resume_text:
        raise HTTPException(status_code=400, detail="Please provide either a Resume PDF or Paste text.")
    if not jd_text.strip():
        raise HTTPException(status_code=400, detail="JD text cannot be empty.")

    # Step 1 & 2: Extract skills & experience using NLP engine
    resume_extracted = process_nlp_extraction(final_resume_text)
    jd_extracted = process_nlp_extraction(jd_text)

    # Step 3: Calculate gap (set difference on keys)
    resume_skills_set = set(resume_extracted.keys())
    jd_skills_set = set(jd_extracted.keys())
    
    skill_gap = jd_skills_set - resume_skills_set
    common_skills = resume_skills_set & jd_skills_set

    # Step 4: Query DB — only courses from catalog (zero hallucinations)
    matched_courses_raw = get_courses_for_skills(list(skill_gap))

    # Deduplicate by course id (a skill may match multiple aliases)
    seen_ids = set()
    pathway = []
    for course in matched_courses_raw:
        if course["id"] not in seen_ids:
            seen_ids.add(course["id"])
            course["reasoning"] = build_reasoning_trace(course["matched_skill"], course)
            pathway.append(course)

    # Sort by level: Beginner → Intermediate → Advanced
    level_order = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
    pathway.sort(key=lambda c: level_order.get(c["level"], 99))

    total_hours = sum(c["duration_hours"] for c in pathway)

    # TTR savings: hours saved vs being assigned the full catalog
    all_catalog = get_all_courses()
    total_catalog_hours = sum(c["duration_hours"] for c in all_catalog)
    ttr_saved_hours = total_catalog_hours - total_hours

    # Build summary
    if not skill_gap:
        summary = "Great news! Your resume already covers all the skills required by this job description. No additional training is needed."
    elif not pathway:
        summary = f"We identified {len(skill_gap)} skill gap(s), but no matching courses were found in the current catalog. Please contact HR to request specialized training."
    else:
        summary = (
            f"Identified {len(skill_gap)} skill gap(s) across {len(pathway)} training module(s). "
            f"Estimated total learning time: {total_hours} hours. "
            f"You save ~{ttr_saved_hours} hours compared to a full generic onboarding. "
            f"Your personalized pathway has been optimized from Beginner to Advanced."
        )

    return AnalyzeResponse(
        resume_skills=resume_extracted,
        jd_skills=jd_extracted,
        skill_gap=sorted(list(skill_gap)),
        common_skills=sorted(list(common_skills)),
        pathway=pathway,
        total_hours=total_hours,
        total_catalog_hours=total_catalog_hours,
        ttr_saved_hours=max(0, ttr_saved_hours),
        summary=summary,
    )


# ─────────────────────────────────────────────
# Mount versioned router
# ─────────────────────────────────────────────
app.include_router(v1)
