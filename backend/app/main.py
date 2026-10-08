import json
from pathlib import Path

from fastapi import FastAPI

from .schemas import CandidateProfile, Job, MatchResult
from .scoring import rank_jobs

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "jobs.json"
FRONTEND_PATH = BASE_DIR.parents[2] / "frontend"

app = FastAPI(
    title="SACHIN AI Placement Copilot",
    version="1.0.0",
    description="Explainable hybrid job matching API.",
)


def load_jobs() -> list[Job]:
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        return [Job.model_validate(item) for item in json.load(handle)]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/jobs", response_model=list[Job])
def jobs() -> list[Job]:
    return load_jobs()


@app.post("/match", response_model=list[MatchResult])
def match(candidate: CandidateProfile) -> list[MatchResult]:
    return rank_jobs(candidate, load_jobs())


if FRONTEND_PATH.exists():
    from fastapi.staticfiles import StaticFiles

    app.mount("/", StaticFiles(directory=FRONTEND_PATH, html=True), name="frontend")
