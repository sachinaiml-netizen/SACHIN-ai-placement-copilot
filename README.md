# SACHIN AI Placement Copilot

A production-oriented **explainable job-ranking system** built with Python, FastAPI, scikit-learn and React.

## Problem

Keyword matching is a weak proxy for job fit. A useful candidate-matching system should combine multiple signals and explain its ranking.

This project implements a deterministic baseline:

**candidate profile → feature extraction → hybrid ranking → score + reasons + skill gaps**

## Engineering highlights

- FastAPI REST API with typed Pydantic contracts
- TF-IDF semantic similarity with word n-grams
- Skill-coverage scoring
- Role-alignment scoring
- Experience-fit factor
- Explainable ranking output
- Unit tests with pytest
- Docker image
- GitHub Actions CI
- Small React client
- Representative job dataset separated from application code

## Architecture

```text
                Candidate Profile
                       |
                       v
              +------------------+
              | Pydantic Schema  |
              +--------+---------+
                       |
                       v
              +------------------+
              | Feature Builder  |
              +--------+---------+
                       |
                       v
              +---------------------------+
              | Explainable Hybrid Ranker |
              | 45% semantic similarity    |
              | 40% skill coverage         |
              | 15% role alignment         |
              | experience adjustment      |
              +-------------+-------------+
                            |
                            v
                  Ranked Jobs + Gaps
                            |
                            v
                       React UI
```

The ranking core intentionally remains deterministic. An LLM can be added later for resume extraction, interview coaching or natural-language explanations without making the core ranking opaque.

## API

### `GET /health`
Returns service status.

### `GET /jobs`
Returns the representative job dataset.

### `POST /match`
Ranks jobs for a candidate.

Example request:

```json
{
  "name": "Sachin",
  "target_roles": ["AI Engineer", "Software Engineer"],
  "skills": ["Python", "FastAPI", "SQL", "Machine Learning", "DSA"],
  "years_experience": 0,
  "resume_summary": "AI/ML engineering student focused on backend software and applied machine learning."
}
```

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

API docs: `http://127.0.0.1:8000/docs`

## Tests

```bash
pytest -q
```

## Docker

```bash
docker build -t sachin-placement-copilot .
docker run -p 8000:8000 sachin-placement-copilot
```

Open `http://127.0.0.1:8000/` for the browser client.

## Repository structure

```text
.
├── .github/workflows/ci.yml
├── backend/app/
│   ├── data/jobs.json
│   ├── main.py
│   ├── schemas.py
│   └── scoring.py
├── frontend/
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       └── styles.css
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```

## Limitations

The included jobs are representative sample data, not live job-market data. The scoring model is a transparent baseline, not a learned hiring decision model.

## Next engineering steps

- Resume PDF extraction
- Embedding-based retrieval
- PostgreSQL persistence
- Authentication
- LLM interview coach
- Evaluation dashboard
- Observability and latency metrics

## Placement Signal Desk

The repository also includes a self-contained, browser-side workflow tool at [`frontend/placement-desk.html`](frontend/placement-desk.html).

It adds:
- Job-description fit analysis with a visible 60/25/15 skill/role/experience formula
- Detected skill overlap and skill gaps
- A role-specific proof-of-work sprint checklist
- Evidence-based recruiter/engineer outreach drafts
- A local application pipeline with status updates and CSV/JSON export

Run the FastAPI application and open `http://127.0.0.1:8000/placement-desk.html`, or open the HTML file directly in a modern browser. The tool uses local browser storage for its profile and tracker, has no LLM API dependency, and does not send outreach or scrape job boards. Scores are heuristic keyword evidence, not hiring probabilities. Verify every result manually.


Live demo: https://sachin-placement-signal-desk-hsachin3278-3215.vercel.app
