# Troubleshooting

## Import error

Run commands from the project root:

```bash
cd AI-personalized-learning-engine
uvicorn app.main:app --reload
```

## Tests

```bash
pytest -q
```

## API example

```bash
curl -X POST http://127.0.0.1:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"goal":"AI Engineer","skills":["Python","SQL"],"weekly_hours":10,"assessment":{"machine learning":0.3,"python":0.8,"sql":0.7}}'
```
