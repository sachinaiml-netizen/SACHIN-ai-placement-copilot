from fastapi import APIRouter

router = APIRouter(prefix="/interviews", tags=["interviews"])


@router.post("/session/start")
def start_session():
    return {"status": "started"}


@router.post("/session/{session_id}/answer")
def answer_question(session_id: int):
    return {"session_id": session_id, "status": "answer_recorded"}


@router.get("/session/{session_id}/feedback")
def get_feedback(session_id: int):
    return {"session_id": session_id, "feedback": "pending"}
