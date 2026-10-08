from pydantic import BaseModel, Field
from typing import List


class CandidateProfile(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    target_roles: List[str] = Field(min_length=1)
    skills: List[str] = Field(default_factory=list)
    years_experience: float = Field(default=0, ge=0)
    resume_summary: str = Field(default="", max_length=4000)


class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str
    min_experience: float = Field(default=0, ge=0)
    skills: List[str] = Field(default_factory=list)
    description: str = ""


class MatchResult(BaseModel):
    job_id: str
    title: str
    company: str
    location: str
    score: float
    skill_coverage: float
    role_alignment: float
    experience_fit: float
    reasons: List[str]
    gaps: List[str]
