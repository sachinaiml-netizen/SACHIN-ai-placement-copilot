from fastapi import FastAPI

from .recommend import recommend
from .schemas import LearnerProfile, LearningPlan

app = FastAPI(
    title="AI Personalized Learning Engine",
    version="1.0.0",
    description="Explainable adaptive learning-plan API.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/plan", response_model=LearningPlan)
def plan(profile: LearnerProfile) -> LearningPlan:
    return recommend(profile)
