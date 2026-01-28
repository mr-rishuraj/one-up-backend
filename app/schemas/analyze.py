from pydantic import BaseModel
from typing import List


class AnalyzeRequest(BaseModel):
    profile_text: str


class Improvement(BaseModel):
    section: str
    current: str
    suggested: str
    reason: str
    impact: str


class AnalyzeResponse(BaseModel):
    score: int
    strengths: List[str]
    weaknesses: List[str]
    improvements: List[Improvement]
