from fastapi import APIRouter

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("/upload")
def upload_resume():
    return {"message": "Resume upload accepted"}


@router.get("/{resume_id}")
def get_resume(resume_id: int):
    return {"resume_id": resume_id}
