from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.analyze import router as analyze_router
import os
import uvicorn

app = FastAPI()

# 🔥 DEBUG CORS — FORCE ALLOW EVERYTHING (OK FOR BETA)
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


# 🔥🔥🔥 THIS IS THE CRITICAL PART YOU WERE MISSING 🔥🔥🔥
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )
