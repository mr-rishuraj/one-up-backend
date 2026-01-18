from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analyze import router as analyze_router

app = FastAPI(
    title="One-Up Backend",
    version="0.1.0",
)

# ✅ CORS CONFIG (THIS FIXES YOUR ERROR)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://one-upp.vercel.app",   # production frontend
        "http://localhost:3000",       # local dev (optional)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(analyze_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok"}
