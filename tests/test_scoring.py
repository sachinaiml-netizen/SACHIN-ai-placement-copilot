from backend.app.schemas import CandidateProfile
from backend.app.main import load_jobs
from backend.app.scoring import rank_jobs


def test_python_fastapi_candidate_ranks_software_roles_high():
    candidate = CandidateProfile(
        name="Sachin",
        target_roles=["Software Engineer", "AI Engineer"],
        skills=["Python", "FastAPI", "SQL", "DSA"],
        years_experience=0,
        resume_summary="AI/ML engineering student building backend and ML applications.",
    )

    results = rank_jobs(candidate, load_jobs())

    assert results
    assert results[0].score >= results[-1].score
    assert results[0].skill_coverage > 0


def test_missing_skills_are_exposed():
    candidate = CandidateProfile(
        name="Sachin",
        target_roles=["AI Engineer"],
        skills=["Python"],
        years_experience=0,
        resume_summary="Machine learning student.",
    )

    results = rank_jobs(candidate, load_jobs())

    assert any(results[0].gaps)
