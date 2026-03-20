"""
run.py — InfiOnboard Server Launcher
Starts the FastAPI server with uvicorn.
"""
import uvicorn

if __name__ == "__main__":
    print("=" * 50)
    print("  InfiOnboard — AI-Adaptive Onboarding Engine")
    print("  Starting server at http://localhost:8000")
    print("=" * 50)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
