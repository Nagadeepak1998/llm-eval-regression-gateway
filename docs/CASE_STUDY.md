# Case Study: LLM Eval Regression Gateway

## Problem

Prompt and model changes can degrade support quality, routing accuracy, or
incident handling behavior before operators notice. Teams need a fast release
gate that can run locally or in CI and catch obvious regressions before rollout.

## Goal

Build a self-contained portfolio project that looks like a small internal AI
platform service: measurable evaluation criteria, an API wrapper, deployment
assets, and documentation that a recruiter or hiring manager can inspect.

## Design Choices

- **Synthetic eval set** keeps the project runnable without external data.
- **Deterministic providers** make regression outcomes reproducible in tests.
- **Rule-based scoring** keeps the metrics interpretable.
- **FastAPI** exposes the evaluation gate as a service instead of a script only.
- **Prometheus metrics** make release-gate behavior observable.
- **Kubernetes and Terraform skeletons** show deployment awareness without
  depending on a real cloud account.

## Tradeoffs

- This is an evaluation harness, not a serving system for real LLM traffic.
- Deterministic mocks are less impressive than live model adapters, but they are
  honest, reproducible, and suitable for a portfolio project finished in one run.
- The Terraform footprint is intentionally narrow so the project stays locally
  verifiable.

## Failure Modes Covered

- Candidate output misclassifies support or incident type
- Candidate downgrades severity
- Candidate suggests the wrong operational action
- Candidate omits required handling keywords
- Candidate includes obviously unsafe phrases
- Candidate latency regresses materially over baseline

## What Recruiters Should Notice

- The project is runnable on a laptop with one setup command.
- It connects evaluation logic, API delivery, testing, and deployment assets in one repo.
- It shows practical AI platform judgment: measurable gates, observability, and controlled scope.

## Next Steps

1. Replace mock providers with real provider adapters.
2. Add stored historical runs and trend reporting.
3. Gate pull requests on policy thresholds.
4. Add dashboards and alerting for ongoing evaluation health.

