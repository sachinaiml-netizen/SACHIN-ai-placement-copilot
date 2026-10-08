from pydantic import BaseModel, Field


class LearnerProfile(BaseModel):
    goal: str = Field(min_length=1, max_length=120)
    skills: list[str] = Field(default_factory=list)
    weekly_hours: float = Field(gt=0, le=80)
    assessment: dict[str, float] = Field(default_factory=dict)


class Topic(BaseModel):
    name: str
    difficulty: int = Field(ge=1, le=5)
    hours: float = Field(gt=0)
    prerequisites: list[str] = Field(default_factory=list)


class PlanItem(BaseModel):
    week: int
    topic: str
    hours: float
    reason: str


class LearningPlan(BaseModel):
    goal: str
    estimated_gap_score: float
    priority_topics: list[str]
    plan: list[PlanItem]
