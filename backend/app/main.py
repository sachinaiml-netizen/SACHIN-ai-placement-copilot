import json
from pathlib import Path

from fastapi import FastAPI

from .schemas import CandidateProfile, Job, MatchResult
from .scoring import rank_jobs

app = FastAPI(
    title="SACHIN AI Placement Copilot",
    version="1.0.0",
    description="Explainable hybrid job matching API.",
)

DATA_PATH = Path(__file__).parent / "data" / "jobs.json"


def load_jobs() -> list[Job]:
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    return [Job.model_validate(item) for item in raw]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/jobs", response_model=list[Job])
def jobs() -> list[Job]:
    return load_jobs()


@app.post("/match", response_model=list[MatchResult])
def match(candidate: CandidateProfile) -> list[MatchResult]:
    return rank_jobs(candidate, load_jobs())
