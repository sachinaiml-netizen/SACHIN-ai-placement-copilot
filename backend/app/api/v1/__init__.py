from app.api.v1 import admin, ats, auth, interviews, jobs, knowledge, resumes, roadmap, skills

ALL_ROUTERS = [
    auth.router,
    resumes.router,
    ats.router,
    skills.router,
    jobs.router,
    roadmap.router,
    interviews.router,
    knowledge.router,
    admin.router,
]
