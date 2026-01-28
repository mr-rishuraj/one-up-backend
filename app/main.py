from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analyze import router as analyze_router

app = FastAPI(
    title="One-Up Backend",
    version="0.1.0",
)

# ✅ CORS CONFIG — FIXED & PRODUCTION SAFE
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://one-upp.vercel.app",   # PROD frontend (exact match)
        "http://localhost:3000",        # LOCAL frontend
        "https://one-up.vercel.app",   # PROD frontend (exact match)

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(analyze_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok"}
