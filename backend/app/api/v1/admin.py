from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users")
def users():
    return {"items": []}


@router.get("/analytics")
def analytics():
    return {"users": 0, "requests": 0}


@router.patch("/jobs/{job_id}/status")
def update_job_status(job_id: int):
    return {"job_id": job_id, "status": "updated"}
