from openai import OpenAI
from app.config import settings


def get_openai_client() -> OpenAI:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not configured")

    return OpenAI(api_key=settings.OPENAI_API_KEY)


def analyze_profile(profile_text: str) -> dict:
    """
    Analyze LinkedIn profile text using OpenAI with strong personalization.
    """

    client = get_openai_client()

    prompt = f"""
You are a top-tier LinkedIn profile reviewer who works with:
- startup founders
- hiring managers
- early-career engineers
- ambitious college students

You are NOT allowed to give generic advice.

The input is RAW, COPIED LinkedIn profile text.
It may contain UI noise, buttons, repeated sections, and irrelevant text.
You must mentally filter that out.

Your task:
1. Infer who this person is (student / fresher / professional / founder)
2. Infer their ambition and positioning from the text alone
3. Critique the profile as if you are reviewing THIS person, not a template
4. Reference specific phrases or sections from the text
5. Rewrite weak parts so they sound written FOR THIS PERSON

Be honest. If something is vague, say why it hurts THIS profile.

Return ONLY valid JSON in the exact format below.
No markdown. No extra text.

JSON format:
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
      "suggested": "Rewrite tailored to this person's background and goals",
      "reason": "Why this change improves THIS profile specifically",
      "impact": "High | Medium | Low"
    }}
  ]
}}

IMPORTANT RULES:
- No generic advice
- No placeholders like "add more details"
- Suggestions must feel custom-written
- Assume the person wants to stand out, not be safe

Profile text:
\"\"\"
{profile_text}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,  # slightly higher for creativity but still controlled
    )

    return response.choices[0].message.content
