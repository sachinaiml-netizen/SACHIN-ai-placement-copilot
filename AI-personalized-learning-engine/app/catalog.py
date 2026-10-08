from .schemas import Topic

TOPICS = [
    Topic(name="Python", difficulty=2, hours=8, prerequisites=[]),
    Topic(name="SQL", difficulty=2, hours=8, prerequisites=[]),
    Topic(name="Data Structures", difficulty=3, hours=14, prerequisites=["Python"]),
    Topic(name="Machine Learning", difficulty=3, hours=16, prerequisites=["Python", "SQL"]),
    Topic(name="Model Evaluation", difficulty=3, hours=8, prerequisites=["Machine Learning"]),
    Topic(name="FastAPI", difficulty=2, hours=8, prerequisites=["Python"]),
    Topic(name="REST APIs", difficulty=2, hours=6, prerequisites=["Python"]),
    Topic(name="LLM Applications", difficulty=4, hours=14, prerequisites=["Python", "REST APIs"]),
    Topic(name="RAG", difficulty=4, hours=12, prerequisites=["LLM Applications", "SQL"]),
    Topic(name="MLOps Basics", difficulty=4, hours=14, prerequisites=["Machine Learning", "FastAPI"]),
]
