from __future__ import annotations

from threading import Lock


class MetricsRegistry:
    def __init__(self) -> None:
        self._lock = Lock()
        self.eval_requests_total = 0
        self.eval_failures_total = 0
        self.last_pass_rate = 0.0

    def record_eval(self, pass_rate: float, failed: bool) -> None:
        with self._lock:
            self.eval_requests_total += 1
            self.last_pass_rate = pass_rate
            if failed:
                self.eval_failures_total += 1

    def render_prometheus(self) -> str:
        return "\n".join(
            [
                "# HELP eval_requests_total Total evaluation requests.",
                "# TYPE eval_requests_total counter",
                f"eval_requests_total {self.eval_requests_total}",
                "# HELP eval_failures_total Total failed release gates.",
                "# TYPE eval_failures_total counter",
                f"eval_failures_total {self.eval_failures_total}",
                "# HELP eval_last_pass_rate Last observed pass rate.",
                "# TYPE eval_last_pass_rate gauge",
                f"eval_last_pass_rate {self.last_pass_rate}",
                "",
            ]
        )


metrics = MetricsRegistry()

