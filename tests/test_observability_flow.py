import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_sample_requests_emit_enriched_scrubbed_logs() -> None:
    log_path = Path("data/logs.jsonl")
    if log_path.exists():
        log_path.unlink()

    client = TestClient(app)
    for line in Path("data/sample_queries.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        response = client.post("/chat", json=json.loads(line))
        assert response.status_code == 200
        assert response.headers["x-request-id"] == response.json()["correlation_id"]
        assert int(response.headers["x-response-time-ms"]) >= 0

    records = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]
    api_records = [record for record in records if record.get("service") == "api"]

    assert len({record["correlation_id"] for record in api_records}) >= 10
    for record in api_records:
        assert record["correlation_id"].startswith("req-")
        assert record["user_id_hash"]
        assert record["session_id"]
        assert record["feature"]
        assert record["model"]
        assert record["env"]

    raw_logs = json.dumps(records)
    assert "@" not in raw_logs
    assert "0987654321" not in raw_logs
    assert "4111" not in raw_logs


def test_dashboard_route_serves_six_panel_dashboard() -> None:
    client = TestClient(app)
    response = client.get("/dashboard")

    assert response.status_code == 200
    html = response.text
    for title in [
        "Latency P50/P95/P99",
        "Traffic",
        "Error Rate With Breakdown",
        "Cost Over Time",
        "Tokens In/Out",
        "Quality Proxy",
    ]:
        assert title in html
