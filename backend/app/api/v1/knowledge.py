from fastapi import APIRouter

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.post("/query")
def query_knowledge():
    return {"answer": ""}


@router.post("/ingest")
def ingest_knowledge():
    return {"status": "ingestion_started"}


@router.get("/sources")
def list_sources():
    return {"sources": []}
