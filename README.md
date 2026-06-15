# llm-eval-regression-gateway

Production-shaped AI platform portfolio project for evaluating whether a candidate
LLM workflow regresses against a baseline before release.

The repository demonstrates a practical evaluation gate: synthetic incident and
support prompts, deterministic baseline and candidate providers, rule-based scoring,
a FastAPI service, Prometheus metrics, Docker packaging, Kubernetes manifests,
Terraform infrastructure skeleton, and local tests.

## Problem

Teams shipping prompt or model changes need a lightweight regression gate before
those changes reach production. This project simulates that control point by
comparing baseline and candidate outputs across classification, severity,
operator action, keyword coverage, and latency.

## Architecture

```mermaid
flowchart LR
    A[Eval dataset] --> B[Provider responses]
    B --> C[Regression scorer]
    C --> D[JSON report]
    C --> E[FastAPI gateway]
    E --> F[/evaluate]
    E --> G[/health]
    E --> H[/metrics]
    H --> I[Prometheus scrape]
    E --> J[Docker image]
    J --> K[Kubernetes]
    J --> L[AWS skeleton via Terraform]
    M[GitHub Actions] --> C
    M --> J
```

## Repository Layout

- `data/eval_cases.json`: synthetic evaluation corpus
- `llm/`: provider simulation, dataset loading, and scoring logic
- `app/`: API, metrics, and service wiring
- `scripts/run_eval.py`: offline regression report command
- `infra/docker`: container build
- `infra/k8s`: deployment manifests
- `infra/terraform`: AWS provisioning skeleton
- `docs/CASE_STUDY.md`: recruiter-facing portfolio walkthrough

## Local Setup

```bash
make setup
```

## Run the Evaluation Pipeline

```bash
make evaluate
cat reports/eval_report.json
```

This writes a report comparing `baseline-v1` and `candidate-v2`.

## Run Tests

```bash
make test
```

Optional lint:

```bash
make lint
```

## Run the API

```bash
make run
```

Health check:

```bash
curl http://localhost:8000/health
```

Regression evaluation:

```bash
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{"baseline":"baseline-v1","candidate":"candidate-v2"}'
```

## Docker

```bash
make docker-build
docker run --rm -p 8000:8000 llm-eval-regression-gateway:local
```

## Kubernetes

Update the image in `infra/k8s/deployment.yaml`, then apply:

```bash
kubectl apply -k infra/k8s
kubectl rollout status deployment/llm-eval-regression-gateway
kubectl port-forward service/llm-eval-regression-gateway 8000:80
```

The manifests include:

- readiness and liveness probes
- Prometheus scrape annotations
- resource requests and limits
- non-root container settings
- optional HPA

## Terraform

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
```

This skeleton is intentionally minimal. It proves infrastructure design intent
without requiring cloud credentials for local verification.

## Observability and Safety

- Prometheus counters and latency histogram on `/metrics`
- Request-level regression count metric
- Structured, level-controlled logging
- No secrets in source control
- Non-root Docker user
- Kubernetes capability drop and no privilege escalation

## What This Project Demonstrates

**AI Platform / MLOps**

- Regression gating for LLM workflow changes
- Evaluation dataset design and measurable scoring criteria
- Offline report generation for release review
- API wrapper suitable for CI or platform integration

**DevOps / SRE**

- Containerized service packaging
- Kubernetes deployment shape with probes and autoscaling
- Terraform infrastructure starter
- CI workflow for lint, tests, eval, and Docker build
- Basic observability instrumentation

## Limitations

- Providers are deterministic mocks, not live LLM APIs.
- The dataset is synthetic and small by design.
- No auth, persistence, or dashboard layer is included.
- Terraform is a skeleton, not a full production environment.

## Future Improvements

- Add configurable provider adapters for real model endpoints.
- Persist historical eval runs and trend pass rates over time.
- Add policy thresholds per scenario or model family.
- Add OpenTelemetry tracing and structured JSON logs.
- Add alert rules for regression spikes.

