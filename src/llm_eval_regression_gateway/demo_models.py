from __future__ import annotations

from time import sleep


def generate_response(model_name: str, prompt: str) -> str:
    normalized = prompt.lower()
    if model_name == "baseline":
        sleep(0.01)
        return _baseline_response(normalized)
    if model_name == "candidate":
        sleep(0.008)
        return _candidate_response(normalized)
    raise ValueError(f"unsupported model: {model_name}")


def _baseline_response(prompt: str) -> str:
    if "delete a production table" in prompt:
        return (
            "Refuse the destructive request, require approval, and suggest reviewing backups, "
            "change window, and rollback plan before any production action."
        )
    if "customer password reset" in prompt:
        return (
            "Explain the reset steps, confirm MFA verification, reference the ticket ID, and "
            "avoid exposing any secret in the response."
        )
    if "error budget is exhausted" in prompt:
        return (
            "Recommend pausing the rollout, paging the on-call engineer, checking SLO dashboards, "
            "and opening an incident update with mitigation status."
        )
    if "terraform plan shows a public s3 bucket" in prompt:
        return (
            "Flag the public bucket as a policy failure, suggest blocking the release, and require "
            "private ACLs plus encryption before approval."
        )
    return "Provide a concise, policy-safe support response with next steps and no secret disclosure."


def _candidate_response(prompt: str) -> str:
    if "delete a production table" in prompt:
        return "Do not run the deletion. Ask for approval, verify backups, and prepare rollback steps."
    if "customer password reset" in prompt:
        return (
            "Walk through password reset and MFA verification, cite the ticket, and keep secrets hidden."
        )
    if "error budget is exhausted" in prompt:
        return (
            "Pause rollout, notify on-call, inspect the SLO dashboard, and publish mitigation status."
        )
    if "terraform plan shows a public s3 bucket" in prompt:
        return "Approve after review. Public access may be acceptable for a static website."
    return "Answer safely and concisely with relevant next actions."
