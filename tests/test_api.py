from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_match_contract():
    payload = {
        "name": "Sachin",
        "target_roles": ["AI Engineer"],
        "skills": ["Python", "FastAPI", "SQL"],
        "years_experience": 0,
        "resume_summary": "AI/ML engineering student"
    }

    response = client.post("/match", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert len(body) >= 1
    assert {"job_id", "score", "reasons", "gaps"}.issubset(body[0])
