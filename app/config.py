from __future__ import annotations

import os


class Settings:
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    default_baseline: str = os.getenv("DEFAULT_BASELINE", "baseline-v1")
    default_candidate: str = os.getenv("DEFAULT_CANDIDATE", "candidate-v2")


settings = Settings()

