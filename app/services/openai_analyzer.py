import json
from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Weighting for final score (total = 100)
SECTION_WEIGHTS = {
    "headline": 20,
    "experience": 25,
    "projects": 20,
    "keywords": 20,
    "credibility": 15,
}


def compute_final_score(section_scores: dict) -> int:
    """
    Compute weighted final score from section scores (0–10 each).
    """
    total = 0
    for section, weight in SECTION_WEIGHTS.items():
        score = section_scores.get(section, 0)
        total += (score / 10) * weight
    return round(total)


def analyze_profile(profile_text: str) -> dict:
    """
    Analyze raw Ctrl+A / Ctrl+C LinkedIn profile text.
    Returns structured, personalized analysis.
    """

    prompt = f"""
You are an expert LinkedIn profile auditor and senior recruiter.

The input below is RAW TEXT copied using Ctrl+A / Ctrl+C from a LinkedIn profile page.
It contains BOTH the profile owner's data AND large amounts of irrelevant UI, feed,
notification, footer, and platform noise.

Your task is to reconstruct the actual profile FIRST, then analyze it.

────────────────────
STEP 1 — IDENTIFY PROFILE OWNER
────────────────────
Identify the SINGLE individual whose profile this page belongs to.
Use signals like:
- Name at the top
- Headline
- Location
- Experience ownership

IGNORE COMPLETELY:
- Posts by other people
- Feed items
- Suggested profiles
- Notifications
- Ads / Premium prompts
- Footer / legal text
- Messages UI

────────────────────
STEP 2 — EXTRACT ONLY THESE SECTIONS (IF PRESENT)
────────────────────
Extract and reason ONLY on:
- Headline
- About section
- Experience (roles, companies, duration)
- Projects (if explicitly mentioned)
- Skills
- Education
- Certifications
- Recommendations / endorsements

If a section is missing, treat it as weak.
DO NOT invent content.

────────────────────
STEP 3 — EVALUATE AS A RECRUITER
────────────────────
Score EACH section from 0–10:
- headline
- experience
- projects
- keywords
- credibility

────────────────────
STEP 4 — OUTPUT STRICT JSON ONLY
────────────────────
Return EXACTLY this JSON structure:

{{
  "sections": {{
    "headline": {{ "score": 0 }},
    "experience": {{ "score": 0 }},
    "projects": {{ "score": 0 }},
    "keywords": {{ "score": 0 }},
    "credibility": {{ "score": 0 }}
  }},
  "strengths": [
    "Specific strength based on extracted content",
    "Specific strength based on extracted content",
    "Specific strength based on extracted content"
  ],
  "weaknesses": [
    "Specific weakness based on missing or weak sections",
    "Specific weakness",
    "Specific weakness"
  ],
  "improvements": [
    {{
      "section": "headline | experience | projects | keywords | credibility",
      "current": "What is weak or missing in THIS profile",
      "suggested": "Concrete, actionable improvement tailored to THIS profile",
      "reason": "Why this matters to recruiters or ATS",
      "impact": "High | Medium | Low"
    }}
  ]
}}

RULES:
- JSON only
- No markdown
- No explanations
- No assumptions beyond provided text
- Be strict and professional, not flattering

PROFILE TEXT:
\"\"\"
{profile_text}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    try:
        parsed = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        raise RuntimeError("AI returned invalid JSON")

    section_scores = {
        key: value["score"]
        for key, value in parsed["sections"].items()
    }

    final_score = compute_final_score(section_scores)

    return {
        "score": final_score,
        "sections": parsed["sections"],
        "strengths": parsed["strengths"],
        "weaknesses": parsed["weaknesses"],
        "improvements": parsed["improvements"],
    }
