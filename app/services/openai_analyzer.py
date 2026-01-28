from openai import OpenAI
from app.config import settings


def get_openai_client() -> OpenAI:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not configured")

    return OpenAI(api_key=settings.OPENAI_API_KEY)


def analyze_profile(profile_text: str) -> dict:
    """
    Analyze LinkedIn profile text using OpenAI with true personalization.
    """

    client = get_openai_client()

    system_prompt = """
You are a top-tier LinkedIn profile reviewer who works with:
- startup founders
- hiring managers
- ambitious college students
- early-career tech professionals

Rules you MUST follow:
- You are NOT allowed to give generic advice
- You must infer context from the profile text itself
- Every strength, weakness, and suggestion must feel written for THIS person
- If input changes, output must change
- Return ONLY valid JSON (no markdown, no explanations)
"""

    user_prompt = f"""
Analyze the following RAW LinkedIn profile text.

This text may include UI noise, repeated sections, buttons, or irrelevant words.
Ignore those and focus only on the actual profile content.

Return JSON in EXACTLY this format:
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
        temperature=0.6,
    )

    return response.choices[0].message.content
