# llm-eval-regression-gateway

Production-shaped AI platform portfolio project for release-gating LLM-backed assistants with
deterministic policy evals, a FastAPI service, JSON reports, Docker packaging, Kubernetes manifests,
Terraform scaffolding, and Prometheus-friendly metrics.

## Business Problem

Prompt, policy, and model changes can silently weaken production assistants. Teams need a repeatable
gate that catches unsafe recommendations, missing guardrails, and operational regressions before rollout.

## What This Project Does

- runs a bundled eval suite against a `baseline` or `candidate` demo responder
- compares candidate results against a baseline with explicit regression budgets
- scores required policy coverage, forbidden content, and latency budgets
- returns a release decision through CLI or HTTP API
- writes JSON, Markdown, and JUnit-style artifacts for CI or release reviews
- exposes `/health`, `/evaluate`, `/compare`, `/reports/latest`, and `/metrics`
- ships Docker, Kubernetes, and Terraform assets for recruiter-readable deployment paths

## Architecture

```mermaid
flowchart LR
    A[Bundled evalset JSONL] --> B[Deterministic evaluator]
    C[Demo baseline and candidate responders] --> B
    B --> D[Single-model release summary]
    D --> E[CLI evaluate]
    D --> F[FastAPI /evaluate]
    D --> L[Baseline vs candidate compare]
    L --> M[CLI compare]
    L --> N[FastAPI /compare]
    F --> G[/metrics]
    N --> G
    F --> H[/reports/latest]
    N --> H
    F --> I[Docker image]
    I --> J[Kubernetes deployment]
    I --> K[ECS Fargate skeleton]
```

## Repository Layout

```text
.
├── app
├── docs
├── evals
├── infra
│   ├── docker
│   ├── k8s
│   └── terraform
├── src
└── tests
```

## Local Setup

```bash
make setup
```

## Run Tests

```bash
make test
```

Optional lint:

```bash
make lint
```

## Run the CLI Gate

Successful baseline gate:

```bash
.venv/bin/llm-eval-gateway evaluate --model baseline --output reports/baseline.json --markdown-output reports/baseline.md --junit-output reports/baseline.xml
```

Candidate gate with an intentional policy failure:

```bash
.venv/bin/llm-eval-gateway evaluate --model candidate --output reports/candidate.json --markdown-output reports/candidate.md --junit-output reports/candidate.xml
```

The candidate run exits non-zero because the bundled `terraform-public-bucket` case recommends
approval instead of blocking insecure infrastructure.

Baseline-vs-candidate comparison with regression budgets:

```bash
.venv/bin/llm-eval-gateway compare --output reports/compare.json --markdown-output reports/compare.md
```

The comparison report highlights new failed cases, score delta, and latency delta so a release
manager can decide whether the candidate stays inside the allowed regression budget.

Artifact outputs:

- `reports/*.json` for machine-readable gate results
- `reports/*.md` for pull request summaries or release notes
- `reports/*.xml` for JUnit-compatible CI ingestion on single-model eval runs

## Run the API

```bash
make run
```

Example requests:

```bash
curl http://localhost:8080/health
curl -X POST http://localhost:8080/evaluate -H "Content-Type: application/json" -d '{"model_name":"candidate"}'
curl -X POST http://localhost:8080/compare -H "Content-Type: application/json" -d '{"candidate_model":"candidate"}'
curl http://localhost:8080/reports/latest
curl http://localhost:8080/metrics
```

## Docker

```bash
make docker-build
make docker-run
```

Or with Compose:

```bash
docker compose up --build
```

## Kubernetes

Update the deployment image, then apply:

```bash
kubectl apply -k infra/k8s
kubectl rollout status deployment/llm-eval-regression-gateway
kubectl port-forward service/llm-eval-regression-gateway 8080:80
```

Included:

- readiness and liveness probes on `/health`
- Prometheus scrape annotations for `/metrics`
- CPU and memory requests and limits
- non-root container security context
- optional HPA manifest

## Terraform

`infra/terraform` provisions an ECS Fargate skeleton with a CloudWatch log group, execution role,
security group, task definition, and service.

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
```

## Observability and Security Basics

- Prometheus-compatible counters and gauges on `/metrics`
- JSON, Markdown, and JUnit-friendly reports suitable for CI artifacts
- Non-root Docker user
- No hardcoded secrets or API keys
- Policy cases cover destructive actions, credential safety, SLO burn, and insecure Terraform
- Comparison metrics track regression-check volume and latest score delta

## CI/CD Note

The GitHub workflow is stored at `docs/github-actions/ci.yml` because the current GitHub token
does not have `workflow` scope. To enable a real `.github/workflows/ci.yml` push later, run:

```bash
gh auth refresh -h github.com -s workflow
```

## Verified Commands

The following commands are intended to be run and recorded in this repo:

```bash
make setup
make test
make lint
.venv/bin/llm-eval-gateway evaluate --model baseline --output reports/baseline.json --markdown-output reports/baseline.md --junit-output reports/baseline.xml
.venv/bin/llm-eval-gateway evaluate --model candidate --output reports/candidate.json --markdown-output reports/candidate.md --junit-output reports/candidate.xml
.venv/bin/llm-eval-gateway compare --output reports/compare.json --markdown-output reports/compare.md
make docker-build
```

## Limitations

- Demo responders are deterministic stand-ins, not real hosted LLMs.
- The scoring model checks required and forbidden terms rather than deep semantic quality.
- The Terraform stack is a portfolio skeleton and should not be treated as production hardening.
- Regression budgets are repo-level heuristics and should be tuned per assistant before production use.

## What This Project Demonstrates

**AI Platform / MLOps**

- release-gating patterns for LLM changes
- eval dataset packaging and report generation
- operational policy checks before rollout
- baseline-vs-candidate regression budgeting
- CI-friendly release artifacts for machine and human review

**DevOps / Platform Engineering**

- container packaging and local runtime
- Kubernetes and ECS deployment scaffolding
- metrics exposure and release artifact handling
- automation through Makefile and testable interfaces
