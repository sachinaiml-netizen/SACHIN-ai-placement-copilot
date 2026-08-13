from fastapi import APIRouter

router = APIRouter(prefix="/skills", tags=["skills"])


@router.post("/gap-analysis")
def gap_analysis():
    return {"status": "queued"}
