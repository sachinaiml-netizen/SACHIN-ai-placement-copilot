# AI Personalized Learning Engine

A production-oriented prototype for generating **personalized learning plans** from learner goals, current skills, available study time and target outcomes.

## Problem

Most learning systems recommend the same sequence to every learner. A useful adaptive system should identify skill gaps, prioritize prerequisites and produce a plan that fits the learner's time constraints.

## Solution

```text
Learner Profile
   |
   +--> Goal / target role
   +--> Current skills
   +--> Weekly study hours
   +--> Assessment signals
            |
            v
      Skill Graph + Gap Analysis
            |
            v
      Priority / Prerequisite Engine
            |
            v
      Personalized Learning Plan
            |
            v
      Explainable recommendations
```

This project uses deterministic recommendation logic as the baseline. An LLM can later generate explanations or teaching content without becoming the hidden decision-maker.

## Example

Input:

```json
{
  "goal": "AI Engineer",
  "skills": ["Python", "SQL"],
  "weekly_hours": 10,
  "assessment": {
    "machine_learning": 0.45,
    "python": 0.80,
    "sql": 0.60
  }
}
```

Output:

```json
{
  "estimated_gap_score": 0.44,
  "priority_topics": [
    "Machine Learning",
    "APIs",
    "Model Evaluation"
  ],
  "plan": [
    {"week": 1, "topic": "Machine Learning Foundations", "hours": 4},
    {"week": 1, "topic": "Model Evaluation", "hours": 3},
    {"week": 1, "topic": "FastAPI", "hours": 3}
  ]
}
```

## Engineering

- Python
- FastAPI
- Pydantic
- Graph-style prerequisite representation
- Explainable scoring
- Unit/API tests
- Docker
- GitHub Actions CI

## Why this matters

The same architecture can power:

- interview preparation
- corporate upskilling
- student learning plans
- role-specific technical roadmaps
- adaptive course sequencing

## Production roadmap

- LLM-generated explanations
- AI lesson/video generation
- learner knowledge tracing
- PostgreSQL persistence
- vector retrieval over course material
- feedback loop from assessment outcomes
- recommendation evaluation dashboard
