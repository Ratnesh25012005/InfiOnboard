"""
main.py — InfiOnboard FastAPI Backend
Implements the Adaptive Pathing Algorithm for skill-gap analysis and course assignment.
"""
import re
import os
import io
import requests
from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from twilio.twiml.messaging_response import MessagingResponse
from pydantic import BaseModel
from pypdf import PdfReader
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
    "sales": ["sales", "b2b", "negotiation", "crm", "salesforce", "pipeline", "outbound"],
    "warehouse": ["warehouse", "logistics", "supply chain", "inventory", "forklift", "osha", "safety"],
    "customer success": ["customer success", "client relations", "onboarding", "nps", "churn", "retention"],
    "hr": ["hr", "human resources", "compliance", "employee relations", "dei", "recruiting", "talent"]
}

# Simulated NLP Engine inspired by Kaggle Resume Dataset & O*NET
def process_nlp_extraction(text: str) -> dict:
    """
    Simulates an LLM/NLP extraction engine.
    Returns a dict mapping skill canonical names to their experience levels.
    """
    text_lower = text.lower()
    extracted = {}
    
    # Simple heuristic for experience levels
    expert_keywords = ["expert", "senior", "lead", "advanced", "architect", "5+ years", "10 years"]
    beginner_keywords = ["junior", "beginner", "entry", "intern", "familiar", "learning", "basic"]
    
    default_level = "Intermediate"
    if any(k in text_lower for k in expert_keywords):
        default_level = "Advanced"
    elif any(k in text_lower for k in beginner_keywords):
        default_level = "Beginner"

    for canonical, aliases in SKILL_TAXONOMY.items():
        for alias in aliases:
            pattern = r'\b' + re.escape(alias) + r'\b'
            if re.search(pattern, text_lower):
                extracted[canonical] = default_level
                break
    return extracted


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
    if resume_file and resume_file.filename.endswith('.pdf'):
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
        resume_skills=resume_extracted,
        jd_skills=jd_extracted,
        skill_gap=sorted(list(skill_gap)),
        common_skills=sorted(list(common_skills)),
        pathway=pathway,
        total_hours=total_hours,
        summary=summary,
    )


# ─────────────────────────────────────────────
# WhatsApp Webhook Endpoint
# ─────────────────────────────────────────────
@app.post("/api/whatsapp")
async def whatsapp_webhook(request: Request):
    """
    Webhook handler for Twilio WhatsApp API.
    Expects PDF as an attachment (MediaUrl0) and JD as text (Body).
    Returns an XML TwiML response containing the learning pathway.
    """
    form_data = await request.form()
    jd_text = form_data.get("Body", "").strip()
    media_url = form_data.get("MediaUrl0")
    media_type = form_data.get("MediaContentType0", "")
    
    resp = MessagingResponse()
    
    if not jd_text:
        resp.message("👋 Welcome to InfiOnboard! Please send me a *Job Description* (as text) and attach your *Resume* (as a PDF) to generate an AI-adaptive training path!")
        return Response(content=str(resp), media_type="application/xml")
        
    if not media_url or "pdf" not in str(media_type).lower():
        resp.message("❌ No PDF found. Please attach your Resume (PDF document) to your message along with the Job Description text.")
        return Response(content=str(resp), media_type="application/xml")
        
    try:
        # Download PDF from Twilio URL
        pdf_response = requests.get(media_url)
        pdf_response.raise_for_status()
        pdf = PdfReader(io.BytesIO(pdf_response.content))
        final_resume_text = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        
        # Step 1 & 2: Skill Extraction
        resume_extracted = process_nlp_extraction(final_resume_text)
        jd_extracted = process_nlp_extraction(jd_text)
        
        skill_gap = set(jd_extracted.keys()) - set(resume_extracted.keys())
        
        if not skill_gap:
            resp.message("🎉 Perfect Match! Your resume indicates you have all the required skills for this job. No additional training is needed.")
            return Response(content=str(resp), media_type="application/xml")
            
        # Compile Database Matches
        matched_courses_raw = get_courses_for_skills(list(skill_gap))
        seen_ids = set()
        pathway = []
        for course in matched_courses_raw:
            if course["id"] not in seen_ids:
                seen_ids.add(course["id"])
                pathway.append(course)
                
        # Sort beginner to advanced
        level_order = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
        pathway.sort(key=lambda c: level_order.get(c["level"], 99))
        
        total_hours = sum(c["duration_hours"] for c in pathway)
        
        # Format WhatsApp output
        msg = f"🎯 *InfiOnboard Analysis Complete*\n\n"
        msg += f"🧩 *Skill Gaps:* {len(skill_gap)}\n"
        msg += f"⏱ *Total Learning:* {total_hours}h\n\n"
        msg += "*Your Actionable Pathway:*\n"
        
        for i, c in enumerate(pathway[:5]): # WhatsApp limit
            icon = "▶️" if c["resource_type"] == "Video" else "📄" if c["resource_type"] == "Documentation" else "💻"
            msg += f"{i+1}️⃣ *{c['title']}* ({c['level']})\n"
            msg += f"_{c['description']}_\n"
            msg += f"{icon} {c['resource_link']}\n\n"
            
        if len(pathway) > 5:
            msg += f"...and {len(pathway)-5} more modules!\n"
            
        resp.message(msg.strip())
        
    except Exception as e:
        resp.message(f"⚠️ Oops! Error processing your documents: {str(e)}")

    return Response(content=str(resp), media_type="application/xml")


# ─────────────────────────────────────────────
# Startup
# ─────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    init_db()
    print("[InfiOnboard] Server started. Catalog database initialized.")
