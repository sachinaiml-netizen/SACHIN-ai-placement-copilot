from app.recommend import recommend
from app.schemas import LearnerProfile


def test_prioritises_large_skill_gap():
    profile = LearnerProfile(
        goal="AI Engineer",
        skills=["Python", "SQL"],
        weekly_hours=10,
        assessment={
            "python": 0.9,
            "sql": 0.8,
            "machine learning": 0.2,
            "model evaluation": 0.1,
        },
    )

    result = recommend(profile)

    assert result.priority_topics
    assert result.priority_topics[0] in {"Model Evaluation", "Machine Learning"}


def test_constrained_schedule_returns_plan():
    profile = LearnerProfile(
        goal="Software Engineer",
        skills=["Python"],
        weekly_hours=4,
        assessment={"python": 0.8},
    )

    result = recommend(profile)

    assert result.plan
    assert result.plan[0].hours <= 4
