# Job Intelligence Agent — n8n Workflow Pack

A practical n8n workflow blueprint for turning a pasted job post into a structured, evidence-based application plan. Built as a small proof-of-work project for AI-agent engineering.

## What it does

1. Accepts a job post and a candidate profile through an n8n Webhook.
2. Normalizes the input into a consistent JSON shape.
3. Calls an LLM through a configurable HTTP Request node to extract requirements and produce a structured assessment.
4. Scores fit with an explicit evidence-first rubric, distinguishing demonstrated evidence, adjacent experience, and gaps.
5. Produces a tailored proof-of-work sprint and a recruiter/engineering outreach draft.
6. Stops at human review. It does **not** automatically send email, message recruiters, or submit applications.

## Why it is designed this way

Hiring fit should not be inferred from keywords alone. The workflow asks for evidence tied to specific requirements and marks unsupported claims as gaps. The final node creates a draft for human review, not an autonomous hiring decision.

## Files

- `workflow.json`: n8n workflow export. Import it into n8n and configure the LLM endpoint/credentials before running.
- `sample-input.json`: example webhook payload with a fictional role and explicitly labelled sample candidate profile.
- `sample-output.json`: example result schema; illustrative, not a live model output.
- `EVALUATION.md`: manual evaluation cases and limitations.

## Setup

1. Run an n8n instance you control.
2. Import `workflow.json`.
3. Configure the **LLM Analysis (configure credentials)** HTTP Request node to use an LLM endpoint you have access to. The exported workflow uses placeholder values; it is not expected to run against a real provider until configured.
4. Set the model to return valid JSON matching the schema shown in `sample-output.json`.
5. Activate the workflow and POST the JSON from `sample-input.json` to its webhook test URL.
6. Review the returned evidence and draft manually.

## Request

```json
{
  "job_posting": "Paste the full job description here",
  "candidate_profile": {
    "skills": ["Python", "FastAPI", "SQL"],
    "projects": [
      {"name": "Example API project", "evidence": "Built a REST endpoint and tests"}
    ],
    "preferences": ["AI engineering", "backend Python"]
  }
}
```

## Safety and limitations

- This is a workflow prototype, not a production recruiting system.
- It does not scrape job boards, access private company systems, or send messages.
- All fit scoring is advisory and should be reviewed by a human.
- Never submit credentials, private personal data, or confidential employer data to an unapproved model provider.
- LLM responses can be wrong or omit requirements. Check the extracted requirements against the original job post.
- The sample output is illustrative. It is not proof of an actual successful run.

## Evaluation

See [EVALUATION.md](EVALUATION.md) for test cases, expected safeguards, and manual acceptance criteria.
