# Case Study: LLM Eval Regression Gateway

## Problem

Teams shipping LLM-backed support or platform assistants need a repeatable way to block
unsafe prompt, policy, or model changes before rollout. Manual spot checks miss regressions,
and many demo projects stop at one-off notebooks instead of a runnable gate.

## What Was Built

This project packages a deterministic regression gateway around a bundled eval set. It exposes
an HTTP API and CLI, writes JSON, Markdown, and JUnit-style release artifacts, emits
Prometheus-friendly metrics, and includes container plus deployment assets for local or
cloud-oriented demos.

## Why This Shape

- Deterministic checks keep the project runnable without paid model APIs.
- Bundled demo responders simulate baseline versus candidate release behavior.
- The failing candidate case demonstrates how an insecure infrastructure recommendation can be blocked.
- Baseline-versus-candidate comparisons make the release decision traceable instead of binary.
- Markdown and JUnit outputs make the same gate usable in pull requests, CI systems, and demo walkthroughs.
- ECS and Kubernetes assets show how the same service could be deployed in standard platform setups.

## Tradeoffs

- The scoring model is heuristic, so it demonstrates release gates rather than semantic quality.
- Demo responders are intentionally simple and not meant as real assistant logic.
- The Terraform layout is a concise skeleton, not a hardened production stack.

## What It Demonstrates

- AI platform release gating patterns
- Regression-budget comparisons for safe model rollout decisions
- Policy-focused regression testing
- FastAPI service packaging
- Containerization and deployment scaffolding
- Metrics and operational reporting
- Recruiter-friendly documentation tied to runnable code

## Next Improvements

1. Add real provider adapters for OpenAI, Anthropic, or local models.
2. Add richer rubric scoring and dataset versioning.
3. Add authentication, rate limiting, and signed report storage.
4. Add drift dashboards and pull request comment automation.
