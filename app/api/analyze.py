from fastapi import APIRouter, HTTPException
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.services.openai_analyzer import analyze_profile
from app.services.scoring_engine import compute_score
from app.utils.profile_hash import profile_hash

router = APIRouter(tags=["Analysis"])

# 🧊 In-memory cache (MVP-safe)
PROFILE_CACHE = {}

ALLOWED_SIGNAL_VALUES = {
    "headline_clarity": {"strong", "moderate", "weak", "missing"},
    "headline_positioning": {"strong", "generic", "missing"},
    "about_structure": {"strong", "moderate", "weak", "missing"},
    "about_credibility": {"strong", "moderate", "weak", "missing"},
    "experience_impact": {"strong", "moderate", "weak", "missing"},
    "differentiation": {"strong", "moderate", "low", "missing"},
    "keyword_relevance": {"strong", "partial", "weak", "missing"},
}


def normalize_signals(signals: dict) -> dict:
    normalized = {}

    for key, allowed in ALLOWED_SIGNAL_VALUES.items():
        value = signals.get(key, "missing")
        if value not in allowed:
            value = "missing"
        normalized[key] = value

    return normalized


@router.post("/analyze-profile", response_model=AnalyzeResponse)
def analyze_profile_api(request: AnalyzeRequest):
    if len(request.profile_text.strip()) < 100:
        raise HTTPException(
            status_code=400,
            detail="Profile text too short for analysis"
        )

    try:
        profile_id = profile_hash(request.profile_text)

        # 🔒 CACHE HIT — FULL DETERMINISM
        if profile_id in PROFILE_CACHE:
            return PROFILE_CACHE[profile_id]

        # ❄️ CACHE MISS — CALL OPENAI ONCE
        analysis = analyze_profile(request.profile_text)

        raw_signals = analysis["signals"]
        signals = normalize_signals(raw_signals)

        score = compute_score(signals)

        response = {
            "score": score,
            "strengths": analysis.get("strengths", []),
            "weaknesses": analysis.get("weaknesses", []),
            "improvements": analysis.get("improvements", [])
        }

        PROFILE_CACHE[profile_id] = response

        return response

    except Exception as e:
        print("ANALYZE_PROFILE_ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail="Failed to analyze profile"
        )
