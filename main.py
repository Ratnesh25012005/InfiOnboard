"""
main.py — InfiOnboard FastAPI Backend
Implements the Adaptive Pathing Algorithm for skill-gap analysis and course assignment.
"""
import re
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from database import init_db, get_courses_for_skills, get_all_courses

# ─────────────────────────────────────────────
# App Setup
# ─────────────────────────────────────────────
app = FastAPI(
    title="InfiOnboard API",
    description="AI-Adaptive Onboarding Engine — Skill Gap Analysis & Learning Pathway Generator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

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
}


def extract_skills(text: str) -> set:
    """
    Extract recognized skills from text using keyword matching against the taxonomy.
    Returns a set of canonical skill names.
    """
    text_lower = text.lower()
    found = set()
    for canonical, aliases in SKILL_TAXONOMY.items():
        for alias in aliases:
            # Use word boundary matching to avoid false positives
            pattern = r'\b' + re.escape(alias) + r'\b'
            if re.search(pattern, text_lower):
                found.add(canonical)
                break
    return found


def build_reasoning_trace(skill: str, course: dict) -> str:
    """Build a human-readable reasoning trace for a course assignment."""
    return (
        f"Resume lacks '{skill.title()}' → "
        f"JD requires '{skill.title()}' → "
        f"Skill gap identified → "
        f"Assigned: {course['title']} ({course['level']}, {course['duration_hours']}h)"
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
    matched_skill: str
    reasoning: str


class AnalyzeResponse(BaseModel):
    resume_skills: list
    jd_skills: list
    skill_gap: list
    common_skills: list
    pathway: list
    total_hours: int
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


@app.get("/api/health")
async def health_check():
    courses = get_all_courses()
    return {
        "status": "healthy",
        "catalog_size": len(courses),
        "message": "InfiOnboard API is running"
    }


@app.get("/api/catalog")
async def get_catalog():
    """Return all courses in the training catalog."""
    courses = get_all_courses()
    return {"courses": courses, "total": len(courses)}


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """
    Adaptive Pathing Algorithm:
    1. Extract skills from Resume text
    2. Extract required skills from JD text
    3. Compute gap = JD skills - Resume skills
    4. Query SQLite catalog for matching courses
    5. Build reasoning traces and return structured pathway
    """
    if not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text cannot be empty.")
    if not request.jd_text.strip():
        raise HTTPException(status_code=400, detail="JD text cannot be empty.")

    # Step 1 & 2: Extract skills
    resume_skills = extract_skills(request.resume_text)
    jd_skills = extract_skills(request.jd_text)

    # Step 3: Calculate gap
    skill_gap = jd_skills - resume_skills
    common_skills = resume_skills & jd_skills

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

    # Build summary
    if not skill_gap:
        summary = "Great news! Your resume already covers all the skills required by this job description. No additional training is needed."
    elif not pathway:
        summary = f"We identified {len(skill_gap)} skill gap(s), but no matching courses were found in the current catalog. Please contact HR to request specialized training."
    else:
        summary = (
            f"Identified {len(skill_gap)} skill gap(s) across {len(pathway)} training module(s). "
            f"Estimated total learning time: {total_hours} hours. "
            f"Your personalized pathway has been optimized from Beginner to Advanced."
        )

    return AnalyzeResponse(
        resume_skills=sorted(list(resume_skills)),
        jd_skills=sorted(list(jd_skills)),
        skill_gap=sorted(list(skill_gap)),
        common_skills=sorted(list(common_skills)),
        pathway=pathway,
        total_hours=total_hours,
        summary=summary,
    )


# ─────────────────────────────────────────────
# Startup
# ─────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    init_db()
    print("[InfiOnboard] Server started. Catalog database initialized.")
