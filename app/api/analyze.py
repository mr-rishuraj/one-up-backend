from fastapi import APIRouter, HTTPException
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.services.openai_analyzer import analyze_profile

router = APIRouter(tags=["Analysis"])


@router.post("/analyze-profile", response_model=AnalyzeResponse)
def analyze_profile_api(request: AnalyzeRequest):
    if len(request.profile_text.strip()) < 100:
        raise HTTPException(
            status_code=400,
            detail="Profile text too short for analysis"
        )

    return analyze_profile(request.profile_text)
