import uvicorn
import sys
from pathlib import Path

# Add project root to sys.path so 'backend.app' resolves cleanly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if __name__ == "__main__":
    print("=" * 65)
    print("  CivicPulse AI Operations Platform — FastAPI Backend Server")
    print("  Live Docs:   http://localhost:8000/docs")
    print("  Frontend UI: http://localhost:8000/")
    print("  API Base:    http://localhost:8000/api/v1")
    print("=" * 65)
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
