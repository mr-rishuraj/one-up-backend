from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.analyze import router as analyze_router

app = FastAPI()

# 🔥 DEBUG CORS — FORCE ALLOW EVERYTHING
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # MUST be False with "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok"}
