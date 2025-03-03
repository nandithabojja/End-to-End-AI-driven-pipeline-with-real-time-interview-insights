from pydantic import BaseModel

class ResumeAnalysis(BaseModel):
    candidate_name: str
    score: float
    strengths: list[str]
    weaknesses: list[str]
    fit: str
