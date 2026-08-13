from fastapi import APIRouter

router = APIRouter(prefix="/roadmap", tags=["roadmap"])


@router.post("/generate")
def generate_roadmap():
    return {"status": "queued"}


@router.get("/{roadmap_id}")
def get_roadmap(roadmap_id: int):
    return {"roadmap_id": roadmap_id}
