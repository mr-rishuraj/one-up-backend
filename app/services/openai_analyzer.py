from openai import OpenAI
from app.config import settings
import json


def get_openai_client() -> OpenAI:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not configured")

    return OpenAI(api_key=settings.OPENAI_API_KEY)


def analyze_profile(profile_text: str) -> dict:
    """
    Analyze LinkedIn profile text and extract STRUCTURED SIGNALS only.
    Scoring is handled separately in scoring_engine.py
    """

    client = get_openai_client()

    # ✅ SYSTEM PROMPT — STRICT, NO SCORING
    system_prompt = """
You are a strict LinkedIn profile evaluator.

IMPORTANT RULES:
- You DO NOT calculate or return any numeric score.
- You DO NOT rate the profile.
- You ONLY extract structured signals and qualitative observations.
- You MUST return valid JSON only.
- No explanations. No markdown. No extra text.
"""

    # ✅ USER PROMPT — SIGNAL EXTRACTION + QUALITATIVE FEEDBACK
    user_prompt = f"""
Analyze the following LinkedIn profile text.

Return ONLY valid JSON in EXACTLY this format:

{{
  "signals": {{
    "headline_clarity": "strong | moderate | weak | missing",
    "headline_positioning": "strong | generic | missing",
    "about_structure": "strong | moderate | weak | missing",
    "about_credibility": "strong | moderate | weak | missing",
    "experience_impact": "strong | moderate | weak | missing",
    "differentiation": "strong | moderate | low | missing",
    "keyword_relevance": "strong | partial | weak | missing"
  }},
  "strengths": [
    "Specific strength referencing the profile text",
    "Specific strength referencing the profile text",
    "Specific strength referencing the profile text"
  ],
  "weaknesses": [
    "Specific weakness referencing the profile text",
    "Specific weakness referencing the profile text",
    "Specific weakness referencing the profile text"
  ],
  "improvements": [
    {{
      "section": "headline | about | experience | projects | skills",
      "current": "Quote or paraphrase what is currently weak",
      "suggested": "Rewrite tailored to this person",
      "reason": "Why this change improves THIS profile",
      "impact": "High | Medium | Low"
    }}
  ]
}}

PROFILE TEXT:
\"\"\"
{profile_text}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,   # 🔒 ABSOLUTE REQUIREMENT
        top_p=1
    )

    raw_content = response.choices[0].message.content

    try:
        return json.loads(raw_content)
    except json.JSONDecodeError:
        raise RuntimeError("OpenAI returned invalid JSON")
