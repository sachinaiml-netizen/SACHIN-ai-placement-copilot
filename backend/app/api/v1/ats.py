from fastapi import APIRouter

router = APIRouter(prefix="/ats", tags=["ats"])


@router.post("/score")
def generate_score():
    return {"score": 0, "status": "queued"}


@router.get("/{report_id}")
def get_report(report_id: int):
    return {"report_id": report_id}
