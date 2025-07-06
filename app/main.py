from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import students  # ✅ Import router file (not model)
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# CORS settings for frontend (React @ localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register the student route
app.include_router(students.router)
