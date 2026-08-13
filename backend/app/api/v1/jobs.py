from fastapi import APIRouter

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/match")
def match_job():
    return {"status": "queued"}


@router.get("/recommendations")
def recommendations():
    return {"items": []}
