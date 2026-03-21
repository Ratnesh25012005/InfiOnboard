# Changelog

All notable changes to InfiOnboard are documented here.

---

## [1.1.0] – 2026-03-21

### Fixed
- `requirements.txt` null-byte encoding corruption — `pip install` was broken for judges
- `main.py`: replaced deprecated `@app.on_event("startup")` with FastAPI `lifespan` context manager
- `main.py`: added `None` guard on `resume_file.filename` to prevent `AttributeError` on empty uploads
- `README.md`: corrected clone URL (was pointing to wrong GitHub user)
- `database.py`: fixed module docstring (said 12 courses, catalog has 16)
- Removed orphaned `frontend/results.html` dead file

### Added
- **Per-skill proximity NLP**: experience level is now detected within a ±60-char window around each skill mention, not globally across the entire document
- **Enriched reasoning traces**: each course now explains *why* a specific difficulty level was assigned
- **TTR savings metric**: API response now includes `ttr_saved_hours` and `total_catalog_hours` so the UI can show hours saved vs full generic onboarding
- **API versioning**: all routes available at `/api/v1/` in addition to legacy `/api/` paths
- **Frontend SaaS polish**:
  - Fixed top navbar with API Docs link
  - Always-visible paste-text fallback (no longer hidden behind double-click)
  - "Try Demo" button pre-fills sample resume + JD for quick judging
  - TTR savings progress bar in results
  - Summary card with live stats (gaps, courses, hours, savings)
  - Polished course cards with hover effects
  - Improved ambient background, typography, and visual hierarchy
- `.env.example` fully documented with all configurable values

---

## [1.0.0] – 2026-03-20

### Added
- Initial release: FastAPI backend, SQLite course catalog (16 courses), glassmorphism frontend
- Adaptive pathing algorithm: set-difference skill gap, Beginner→Advanced ordering
- PDF drag-and-drop upload via PyPDF
- Cross-domain coverage: Tech, GenAI, Sales, Warehouse, HR
- Dockerfile for reproducible judging environment
- 5-slide presentation deck
