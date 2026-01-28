from fastapi import APIRouter, HTTPException
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.services.openai_analyzer import analyze_profile

import json

router = APIRouter(tags=["Analysis"])


@router.post("/analyze-profile", response_model=AnalyzeResponse)
def analyze_profile_api(request: AnalyzeRequest):
    if len(request.profile_text.strip()) < 100:
        raise HTTPException(
            status_code=400,
            detail="Profile text too short for analysis"
        )

    try:
        result = analyze_profile(request.profile_text)

        # 🔥 FIX: OpenAI returns JSON AS STRING → convert to dict
        if isinstance(result, str):
            result = json.loads(result)

        return result

    except Exception as e:
        print("ANALYZE_PROFILE_ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail="Failed to analyze profile"
        )
