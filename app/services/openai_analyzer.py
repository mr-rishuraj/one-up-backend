from openai import OpenAI
from app.config import settings


def get_openai_client() -> OpenAI:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not configured")

    return OpenAI(api_key=settings.OPENAI_API_KEY)


def analyze_profile(profile_text: str) -> dict:
    """
    Analyze LinkedIn profile text using OpenAI with dynamic scoring.
    """

    client = get_openai_client()

    # 🔥 SYSTEM PROMPT — FIXES THE 75 SCORE ANCHOR
    system_prompt = """
You are a top-tier LinkedIn profile reviewer.

You MUST compute the final score using this rubric:

- Clarity of positioning (0–25)
- Strength of experience/projects (0–25)
- Specificity & credibility of claims (0–25)
- Differentiation vs average profiles (0–25)

Scoring rules:
- You MUST internally calculate all four subscores
- Add them to get the final score (0–100)
- Different profiles MUST produce different scores
- Weak / vague profiles: 40–55
- Average profiles: 55–65
- Strong student profiles: 65–80
- Exceptional profiles: 80+

You are NOT allowed to default to a fixed or “safe” number.
Return ONLY the final number as "score".
"""

    # USER PROMPT — DATA ONLY
    user_prompt = f"""
Analyze the following RAW LinkedIn profile text.

The text may contain UI noise, repeated sections, or irrelevant strings.
Ignore those and focus only on meaningful profile content.

Return ONLY valid JSON in EXACTLY this format:
{{
  "score": number between 0 and 100,
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
        temperature=0.6,  # allows score variance without chaos
    )

    return response.choices[0].message.content
