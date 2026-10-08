# Architecture Notes

## Design choice

The project uses a deterministic ranking core before introducing an LLM. This makes the baseline reproducible, testable and explainable.

## Ranking

For each candidate/job pair:

1. Build a normalized text representation.
2. Compute TF-IDF cosine similarity over unigrams and bigrams.
3. Calculate required-skill coverage.
4. Calculate target-role alignment.
5. Calculate an experience-fit adjustment.
6. Return score, positive reasons and explicit skill gaps.

The baseline score is:

`(0.45 × semantic similarity + 0.40 × skill coverage + 0.15 × role alignment) × experience adjustment`

The weights are intentionally explicit so they can be tuned and evaluated later.

## Production evolution

A production version would replace sample jobs with a versioned job-ingestion pipeline and persist candidates/jobs in PostgreSQL. Semantic retrieval could use embeddings, while the deterministic score remains as an interpretable re-ranking stage.

LLMs should be used where language generation adds value—resume extraction, interview generation and explanation—not as an unquestionable hiring decision-maker.
