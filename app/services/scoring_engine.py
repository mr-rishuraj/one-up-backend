# app/services/scoring_engine.py

SCORE_WEIGHTS = {
    "headline_clarity": 20,
    "headline_positioning": 10,
    "about_structure": 15,
    "about_credibility": 15,
    "experience_impact": 20,
    "differentiation": 10,
    "keyword_relevance": 10
}

VALUE_MAP = {
    "strong": 1.0,
    "clear": 1.0,

    "moderate": 0.6,
    "partial": 0.5,

    "weak": 0.3,

    "generic": 0.0,
    "low": 0.0,
    "missing": 0.0
}


def compute_score(signals: dict) -> int:
    total = 0.0

    for key, weight in SCORE_WEIGHTS.items():
        raw_value = signals.get(key, "missing")
        normalized = VALUE_MAP.get(raw_value, 0.0)
        total += normalized * weight

    return round(total)
