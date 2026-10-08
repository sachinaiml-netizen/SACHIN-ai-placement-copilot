from __future__ import annotations

from typing import Iterable, List
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .schemas import CandidateProfile, Job, MatchResult


def _normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9+#. ]+", " ", value.lower()).strip()


def _skill_set(skills: Iterable[str]) -> set[str]:
    return {_normalise(skill) for skill in skills if skill.strip()}


def _role_alignment(candidate_roles: Iterable[str], title: str) -> float:
    title_text = _normalise(title)
    roles = [_normalise(role) for role in candidate_roles]
    if not roles:
        return 0.0
    exact = max((1.0 if role in title_text else 0.0 for role in roles), default=0.0)
    token_overlap = max(
        (
            len(set(role.split()) & set(title_text.split()))
            / max(len(set(role.split())), 1)
            for role in roles
        ),
        default=0.0,
    )
    return min(1.0, 0.7 * exact + 0.3 * token_overlap)


def _experience_fit(years: float, minimum: float) -> float:
    if years >= minimum:
        return 1.0
    if minimum == 0:
        return 1.0
    # Graceful score for students rather than an all-or-nothing filter.
    return max(0.0, years / minimum)


def rank_jobs(candidate: CandidateProfile, jobs: List[Job]) -> List[MatchResult]:
    candidate_skills = _skill_set(candidate.skills)
    candidate_doc = _normalise(
        " ".join(candidate.target_roles) + " " +
        " ".join(candidate.skills) + " " +
        candidate.resume_summary
    )

    job_docs = [
        _normalise(job.title + " " + " ".join(job.skills) + " " + job.description)
        for job in jobs
    ]

    docs = [candidate_doc] + job_docs
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    matrix = vectorizer.fit_transform(docs)
    semantic = cosine_similarity(matrix[0:1], matrix[1:]).ravel()

    results: List[MatchResult] = []

    for index, job in enumerate(jobs):
        required = _skill_set(job.skills)
        overlap = candidate_skills & required
        skill_coverage = len(overlap) / len(required) if required else 1.0
        role_alignment = _role_alignment(candidate.target_roles, job.title)
        experience_fit = _experience_fit(candidate.years_experience, job.min_experience)

        # Weighted, interpretable baseline.
        score = (
            45.0 * float(semantic[index]) +
            40.0 * skill_coverage +
            15.0 * role_alignment
        ) * (0.75 + 0.25 * experience_fit)

        reasons = []
        if overlap:
            reasons.append(f"Matching skills: {', '.join(sorted(overlap))}")
        if role_alignment >= 0.7:
            reasons.append("Target role aligns closely with the job title.")
        if experience_fit == 1.0:
            reasons.append("Experience requirement is satisfied for the baseline.")
        elif job.min_experience > 0:
            reasons.append(
                f"Experience gap: role asks for {job.min_experience:g}+ years."
            )

        gaps = sorted(required - candidate_skills)

        results.append(
            MatchResult(
                job_id=job.id,
                title=job.title,
                company=job.company,
                location=job.location,
                score=round(max(0.0, min(100.0, score)), 2),
                skill_coverage=round(skill_coverage, 3),
                role_alignment=round(role_alignment, 3),
                experience_fit=round(experience_fit, 3),
                reasons=reasons,
                gaps=gaps,
            )
        )

    return sorted(results, key=lambda item: item.score, reverse=True)
