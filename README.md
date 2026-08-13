# SACHIN-ai-placement-copilot

AI-powered placement assistant that helps students improve resumes, analyze job matches, prepare for interviews, and build personalized learning roadmaps using FastAPI, React, PostgreSQL, and GenAI.

## 1) Production-Grade Project Architecture

### High-Level RAG + App Architecture

```text
[React Web App]
    |
    v
[FastAPI Gateway + Auth + RBAC]
    |
    +--> [Placement Services Layer]
    |      - Resume Analyzer
    |      - ATS Score Generator
    |      - Skill Gap Analysis
    |      - Job Matching Engine
    |      - Learning Roadmap
    |      - Mock Interview Assistant
    |
    +--> [RAG Orchestrator]
    |      - Query Rewriter
    |      - Retriever (pgvector / vector DB)
    |      - Prompt Builder
    |      - LLM Response (OpenAI API)
    |
    +--> [PostgreSQL]
    |      - OLTP tables (users, resumes, jobs, interviews, reports)
    |      - Vector embeddings (knowledge chunks)
    |
    +--> [Background Workers]
           - Resume parsing, embeddings, roadmap generation, async scoring
```

### Core Design Principles
- **Modular monolith first** (clean service boundaries), move to microservices later.
- **Async-first backend** with queue workers for heavy AI tasks.
- **RAG grounded responses** using placement knowledge base + citations.
- **Secure by default**: JWT auth, RBAC, rate limiting, secrets in env.
- **Observable**: structured logs, metrics, error tracking.

---

## 2) Clean Folder Structure

```text
SACHIN-ai-placement-copilot/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── resumes.py
│   │   │   │   ├── ats.py
│   │   │   │   ├── skills.py
│   │   │   │   ├── jobs.py
│   │   │   │   ├── roadmap.py
│   │   │   │   ├── interviews.py
│   │   │   │   ├── knowledge.py
│   │   │   │   └── admin.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── logging.py
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   ├── base.py
│   │   │   └── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── rag/
│   │   │   ├── llm/
│   │   │   └── matching/
│   │   ├── workers/
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   │   ├── Dashboard/
│   │   │   ├── ResumeAnalyzer/
│   │   │   ├── JobMatching/
│   │   │   ├── MockInterview/
│   │   │   └── Admin/
│   │   ├── store/
│   │   ├── hooks/
│   │   └── App.tsx
│   ├── package.json
│   └── Dockerfile
├── infra/
│   ├── docker-compose.yml
│   └── nginx/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
└── README.md
```

---

## 3) Feature Modules (Scope)

1. **Resume Analyzer**
   - Upload PDF/DOCX resume
   - NLP parsing, skill extraction, project quality analysis
2. **ATS Score Generator**
   - JD vs resume keyword alignment
   - Section completeness and readability scoring
3. **Skill Gap Analysis**
   - Compare current skill profile to target role skill graph
4. **Job Matching Engine**
   - Match % using skills, experience, and semantic similarity
5. **Personalized Learning Roadmap**
   - 30/60/90 day plan with curated resources
6. **Mock Interview Assistant**
   - AI interviewer (technical + HR rounds), feedback, follow-up questions
7. **Placement Knowledge Base (RAG)**
   - College/company interview experiences, OS/DBMS/CN/OOP notes
8. **Admin Dashboard**
   - User management, content moderation, analytics, model usage monitoring

---

## 4) REST API Design (v1)

### Auth
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `GET /api/v1/auth/me`

### Resume + ATS
- `POST /api/v1/resumes/upload`
- `GET /api/v1/resumes/{resume_id}`
- `POST /api/v1/ats/score`
- `GET /api/v1/ats/{report_id}`

### Skills + Jobs
- `POST /api/v1/skills/gap-analysis`
- `POST /api/v1/jobs/match`
- `GET /api/v1/jobs/recommendations`

### Roadmap + Interview
- `POST /api/v1/roadmap/generate`
- `GET /api/v1/roadmap/{roadmap_id}`
- `POST /api/v1/interviews/session/start`
- `POST /api/v1/interviews/session/{id}/answer`
- `GET /api/v1/interviews/session/{id}/feedback`

### RAG Knowledge
- `POST /api/v1/knowledge/query`
- `POST /api/v1/knowledge/ingest` (admin)
- `GET /api/v1/knowledge/sources`

### Admin
- `GET /api/v1/admin/users`
- `GET /api/v1/admin/analytics`
- `PATCH /api/v1/admin/jobs/{job_id}/status`

---

## 5) PostgreSQL Database Schema

### Authentication & Profiles
- `users(id, name, email, password_hash, role, created_at, updated_at)`
- `profiles(id, user_id, college, branch, graduation_year, cgpa, target_role)`
- `refresh_tokens(id, user_id, token_hash, expires_at, revoked)`

### Core Placement Data
- `resumes(id, user_id, file_url, parsed_text, version, created_at)`
- `jobs(id, title, company, location, jd_text, source_url, created_at)`
- `applications(id, user_id, job_id, status, applied_at)`
- `skill_catalog(id, skill_name, category)`
- `user_skills(id, user_id, skill_id, level)`

### AI Outputs
- `ats_reports(id, user_id, resume_id, job_id, score, breakdown_json, created_at)`
- `skill_gap_reports(id, user_id, target_role, gaps_json, created_at)`
- `job_match_reports(id, user_id, job_id, match_score, reasons_json, created_at)`
- `roadmaps(id, user_id, target_role, plan_json, created_at)`
- `interview_sessions(id, user_id, type, started_at, ended_at, summary_json)`
- `interview_messages(id, session_id, role, message, feedback_json, created_at)`

### RAG Knowledge Base
- `knowledge_documents(id, title, source, uploaded_by, created_at)`
- `knowledge_chunks(id, doc_id, chunk_text, embedding vector, metadata_json)`
  - Use `pgvector` extension for embeddings.

### Admin & Audit
- `audit_logs(id, actor_user_id, action, entity, entity_id, payload_json, created_at)`
- `usage_metrics(id, user_id, endpoint, model_name, tokens_in, tokens_out, cost, created_at)`

---

## 6) Authentication & Security Model

- JWT access tokens + refresh token rotation.
- Role-based access control: `student`, `admin`.
- Password hashing with `bcrypt`.
- Rate limiting for AI-heavy endpoints.
- Input validation using Pydantic schemas.
- OpenAI key and DB credentials via environment variables and secrets manager.

---

## 7) Docker & Deployment Plan

### Containers
- `frontend`: React app served via Nginx.
- `backend`: FastAPI + Uvicorn.
- `db`: PostgreSQL + pgvector.
- `worker`: background jobs (Celery/RQ).

### Environments
- **Dev**: `docker-compose` local stack.
- **Staging**: cloud VM / container service + managed PostgreSQL.
- **Prod**: autoscaled API containers, CDN, managed DB, centralized logs.

### CI/CD (GitHub Actions)
- On PR: lint + tests (backend and frontend) + security checks.
- On merge to main: build Docker images, push registry, deploy staging/prod.

---

## 8) Scalable Architecture Plan

### Phase-1 (MVP)
- Single FastAPI service + PostgreSQL + basic RAG + core student dashboard.

### Phase-2 (Scale)
- Add Redis caching, background workers, async job queue, improved observability.

### Phase-3 (Enterprise)
- Split AI pipeline into services (matching, interview, roadmap), multi-tenant controls.

---

## 9) Beginner-Friendly Implementation Roadmap

### Week 1-2: Foundations
- Setup FastAPI, React, PostgreSQL, Docker.
- Implement auth + profile CRUD.

### Week 3-4: Resume + ATS
- Resume upload/parsing and ATS report generation.
- Build UI for report visualization.

### Week 5-6: Skill Gap + Job Matching
- Skill graph baseline + matching score APIs.
- Add job recommendation page.

### Week 7-8: RAG + Mock Interview
- Ingest placement notes into vector store.
- Build conversational Q&A + interview simulator.

### Week 9-10: Admin + Polish
- Admin analytics, moderation, usage tracking.
- Add tests, CI/CD hardening, performance tuning, and deployment docs.

---

## 10) GitHub Project Setup

### Repository Setup
1. Protect `main` branch.
2. Enforce PR reviews + status checks.
3. Add issue templates:
   - Feature request
   - Bug report
   - Model improvement
4. Add labels: `backend`, `frontend`, `ai`, `rag`, `infra`, `good-first-issue`.

### Suggested GitHub Project Board Columns
- Backlog
- Ready
- In Progress
- In Review
- Done

### Initial Milestones
- `M1: Foundation & Auth`
- `M2: Resume + ATS`
- `M3: Skill/Job Intelligence`
- `M4: Interview + RAG`
- `M5: Production Deployment`

---

This blueprint is intentionally production-oriented while still beginner-friendly so it can be built iteratively into a portfolio-grade AIML placement copilot.
