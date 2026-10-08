from __future__ import annotations

from .catalog import TOPICS
from .schemas import LearnerProfile, LearningPlan, PlanItem, Topic


def _normalise(value: str) -> str:
    return value.strip().lower()


def _topic_score(topic: Topic, profile: LearnerProfile) -> float:
    mastery = profile.assessment.get(_normalise(topic.name), 0.0)
    missing = 1.0 - mastery
    difficulty_factor = topic.difficulty / 5
    return 0.65 * missing + 0.35 * difficulty_factor


def _prerequisite_gap(topic: Topic, profile: LearnerProfile) -> float:
    if not topic.prerequisites:
        return 0.0

    known = {_normalise(skill) for skill in profile.skills}
    mastery = profile.assessment

    gaps = []
    for prereq in topic.prerequisites:
        key = _normalise(prereq)
        if key in known:
            continue
        gaps.append(1.0 - mastery.get(key, 0.0))

    return max(gaps, default=0.0)


def recommend(profile: LearnerProfile, max_weeks: int = 4) -> LearningPlan:
    known = {_normalise(skill) for skill in profile.skills}

    candidates = []
    for topic in TOPICS:
        if _normalise(topic.name) in known:
            mastery = profile.assessment.get(_normalise(topic.name), 1.0)
            if mastery >= 0.8:
                continue

        score = _topic_score(topic, profile) + 0.25 * _prerequisite_gap(topic, profile)
        candidates.append((score, topic))

    candidates.sort(key=lambda pair: pair[0], reverse=True)

    selected: list[tuple[float, Topic]] = []
    selected_names: set[str] = set()
    available_hours = profile.weekly_hours * max_weeks

    for _, topic in candidates:
        required = [p for p in topic.prerequisites if p not in selected_names]
        prereq_hours = sum(
            t.hours for _, t in candidates
            if t.name in required
        )

        if topic.hours + prereq_hours <= available_hours - sum(t.hours for _, t in selected):
            selected.append((0.0, topic))
            selected_names.add(topic.name)

    # Guarantee a useful result even for a very constrained learner.
    if not selected and candidates:
        selected.append((0.0, candidates[0][1]))

    plan: list[PlanItem] = []
    current_week = 1
    week_hours = 0.0

    for _, topic in selected:
        remaining = profile.weekly_hours - week_hours
        if topic.hours > remaining and week_hours > 0:
            current_week += 1
            week_hours = 0.0

        hours = min(topic.hours, profile.weekly_hours)
        reason = (
            "Large assessed skill gap."
            if profile.assessment.get(_normalise(topic.name), 0.0) < 0.5
            else "High-value topic for the target goal."
        )

        plan.append(
            PlanItem(
                week=min(current_week, max_weeks),
                topic=topic.name,
                hours=hours,
                reason=reason,
            )
        )
        week_hours += hours

        if week_hours >= profile.weekly_hours:
            current_week += 1
            week_hours = 0.0

    gap_values = [
        1.0 - profile.assessment.get(_normalise(topic.name), 0.0)
        for _, topic in selected
    ]

    estimated_gap = sum(gap_values) / len(gap_values) if gap_values else 0.0

    return LearningPlan(
        goal=profile.goal,
        estimated_gap_score=round(estimated_gap, 3),
        priority_topics=[topic.name for _, topic in selected[:5]],
        plan=plan[:12],
    )
