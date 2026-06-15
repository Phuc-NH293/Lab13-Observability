from pathlib import Path


def test_alert_rules_cover_required_symptoms_and_runbooks() -> None:
    config = Path("config/alert_rules.yaml").read_text(encoding="utf-8")
    runbook = Path("docs/alerts.md").read_text(encoding="utf-8")

    required_rules = {
        "high_latency_p95": "latency_p95_ms > 5000 for 30m",
        "high_error_rate": "error_rate_pct > 5 for 5m",
        "cost_budget_spike": "hourly_cost_usd > 2x_baseline for 15m",
    }

    for name, condition in required_rules.items():
        assert f"name: {name}" in config
        assert f"condition: {condition}" in config
        assert "type: symptom-based" in config
        assert "runbook: docs/alerts.md#" in config

    assert "## 1. High latency P95" in runbook
    assert "## 2. High error rate" in runbook
    assert "## 3. Cost budget spike" in runbook
