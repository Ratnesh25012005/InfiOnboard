"""
database.py — InfiOnboard Course Catalog Database
Initializes SQLite catalog.db and seeds 12 corporate training courses.
"""
import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "catalog.db")

COURSES = [
    {
        "id": 1,
        "title": "Python Fundamentals",
        "skill_tag": "python",
        "duration_hours": 20,
        "level": "Beginner",
        "description": "Core Python programming: syntax, functions, OOP, and standard library essentials."
    },
    {
        "id": 2,
        "title": "Advanced SQL Data Analysis",
        "skill_tag": "sql",
        "duration_hours": 15,
        "level": "Intermediate",
        "description": "Window functions, CTEs, query optimization, and analytical SQL techniques."
    },
    {
        "id": 3,
        "title": "React State Management",
        "skill_tag": "react",
        "duration_hours": 18,
        "level": "Intermediate",
        "description": "Redux, Context API, Zustand, and advanced React patterns for scalable frontends."
    },
    {
        "id": 4,
        "title": "AWS Cloud Practitioner",
        "skill_tag": "aws",
        "duration_hours": 25,
        "level": "Beginner",
        "description": "EC2, S3, Lambda, IAM, VPC fundamentals and AWS infrastructure essentials."
    },
    {
        "id": 5,
        "title": "Docker & Containerization",
        "skill_tag": "docker",
        "duration_hours": 12,
        "level": "Intermediate",
        "description": "Building Docker images, Compose, networking, volumes, and deployment best practices."
    },
    {
        "id": 6,
        "title": "Machine Learning with Scikit-Learn",
        "skill_tag": "machine learning",
        "duration_hours": 30,
        "level": "Intermediate",
        "description": "Supervised/unsupervised learning, model evaluation, feature engineering, and pipelines."
    },
    {
        "id": 7,
        "title": "TypeScript for Professional Developers",
        "skill_tag": "typescript",
        "duration_hours": 14,
        "level": "Intermediate",
        "description": "Types, interfaces, generics, decorators, and strict TypeScript configuration."
    },
    {
        "id": 8,
        "title": "REST API Design with FastAPI",
        "skill_tag": "fastapi",
        "duration_hours": 10,
        "level": "Intermediate",
        "description": "Building high-performance APIs with FastAPI, Pydantic validation, and OpenAPI docs."
    },
    {
        "id": 9,
        "title": "Kubernetes Fundamentals",
        "skill_tag": "kubernetes",
        "duration_hours": 20,
        "level": "Advanced",
        "description": "Pods, Deployments, Services, ConfigMaps, and orchestrating containers at scale."
    },
    {
        "id": 10,
        "title": "Data Visualization with Tableau",
        "skill_tag": "tableau",
        "duration_hours": 16,
        "level": "Beginner",
        "description": "Building interactive dashboards, calculated fields, and publishing reports."
    },
    {
        "id": 11,
        "title": "Agile & Scrum Methodology",
        "skill_tag": "agile",
        "duration_hours": 8,
        "level": "Beginner",
        "description": "Sprint planning, retrospectives, user stories, and agile team collaboration."
    },
    {
        "id": 12,
        "title": "Generative AI & Prompt Engineering",
        "skill_tag": "generative ai",
        "duration_hours": 12,
        "level": "Intermediate",
        "description": "LLM fundamentals, prompt design, RAG pipelines, and responsible AI practices."
    },
]


def init_db():
    """Initialize the database and seed course catalog."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            skill_tag TEXT NOT NULL,
            duration_hours INTEGER NOT NULL,
            level TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    # Seed only if empty
    cursor.execute("SELECT COUNT(*) FROM courses")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.executemany(
            "INSERT INTO courses (id, title, skill_tag, duration_hours, level, description) VALUES (:id, :title, :skill_tag, :duration_hours, :level, :description)",
            COURSES
        )
        print(f"[DB] Seeded {len(COURSES)} courses into catalog.db")
    else:
        print(f"[DB] catalog.db already has {count} courses — skipping seed.")

    conn.commit()
    conn.close()


def get_courses_for_skills(skills: list) -> list:
    """
    Query the catalog for courses matching the given skill tags.
    Returns a list of matching course dicts.
    """
    if not skills:
        return []

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    results = []
    for skill in skills:
        skill_lower = skill.lower().strip()
        cursor.execute(
            "SELECT * FROM courses WHERE LOWER(skill_tag) LIKE ?",
            (f"%{skill_lower}%",)
        )
        rows = cursor.fetchall()
        for row in rows:
            course = dict(row)
            course["matched_skill"] = skill
            results.append(course)

    conn.close()
    return results


def get_all_courses() -> list:
    """Return all courses in the catalog."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses ORDER BY id")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
    courses = get_all_courses()
    print(f"\nCourse Catalog ({len(courses)} courses):")
    for c in courses:
        print(f"  [{c['id']}] {c['title']} — {c['skill_tag']} ({c['level']}, {c['duration_hours']}h)")
