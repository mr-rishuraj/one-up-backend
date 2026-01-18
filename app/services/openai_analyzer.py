from openai import OpenAI
from app.config import settings


def get_openai_client() -> OpenAI:
    """
    Lazily create OpenAI client only when needed.
    """
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not configured")

    return OpenAI(api_key=settings.OPENAI_API_KEY)


def analyze_profile(profile_text: str) -> dict:
    """
    Analyze LinkedIn profile text using OpenAI.
    """

    client = get_openai_client()

    prompt = f"""
You are an expert LinkedIn recruiter and resume analyst.

You will receive RAW COPIED TEXT from a LinkedIn profile page.
This text may contain:
- Navigation text
- Buttons
- Repeated sections
- Noise and irrelevant UI strings

Your job:
1. Identify the actual profile owner
2. Extract relevant professional sections ONLY:
   - Headline
   - About
   - Experience
   - Projects
   - Skills
3. Ignore likes, comments, followers, ads, UI labels

Then evaluate the profile rigorously and return ONLY valid JSON.

Return JSON in this exact format:
{{
  "score": number between 0 and 100,
  "strengths": [3 concise bullets],
  "weaknesses": [3 concise bullets],
  "improvements": [
    {{
      "section": "headline | about | experience | projects | skills",
      "current": "What is weak or missing",
      "suggested": "Concrete improvement",
      "reason": "Why this improves the profile",
      "impact": "High | Medium | Low"
    }}
  ]
}}

Rules:
- JSON only
- No markdown
- No explanations
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content
