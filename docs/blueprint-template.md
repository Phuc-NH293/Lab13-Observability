# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: Nguyễn Hồng Phúc Observability Team
- [REPO_URL]: https://github.com/Phuc-NH293/Lab13-Observability.git
- [MEMBERS]:
  - Member A: Nguyễn Hồng Phúc | Role: Logging & PII
  - Member B: Nguyễn Hồng Phúc | Role: Tracing & Enrichment
  - Member C: Nguyễn Hồng Phúc | Role: SLO & Alerts
  - Member D: Nguyễn Hồng Phúc | Role: Load Test & Dashboard
  - Member E: Nguyễn Hồng Phúc | Role: Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: 71 Langfuse `agent_run` traces
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: `docs/evidence/01-correlation-id-logs.png`
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: `docs/evidence/02-pii-redaction-logs.png`
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: `docs/evidence/03-langfuse-trace-waterfall.png`
- [TRACE_WATERFALL_EXPLANATION]: The Langfuse trace `bd6b0642bfee379c947f9e1d6ecbdbf9` shows an `agent_run` trace with child spans for retrieval and LLM work. The `rag_retrieve` span isolates retrieval latency and the `llm_generate` span isolates model response latency, which makes root-cause analysis faster than reading a single end-to-end timing.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: `docs/evidence/04-dashboard-6-panels.png`
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 2654ms |
| Error Rate | < 2% | 28d | 0% |
| Cost Budget | < $2.5/day | 1d | $0.0215 current run |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: `docs/evidence/05-alert-rules-runbook.png`
- [SAMPLE_RUNBOOK_LINK]: `docs/alerts.md#L3`

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: P95 latency increased during the injected incident. The incident request returned `latency_ms=2654` with correlation ID `req-27287f7b`.
- [ROOT_CAUSE_PROVED_BY]: Langfuse trace `31a5b81b57f76227ae6539b7f7968132` showed `latency=2.686s` and metadata `latency_ms=2654`. Local logs also contain the matching correlation ID `req-27287f7b`.
- [FIX_ACTION]: Disabled the `rag_slow` incident toggle via `POST /incidents/rag_slow/disable`, returning incidents to `{"rag_slow": false, "tool_fail": false, "cost_spike": false}`.
- [PREVENTIVE_MEASURE]: Keep the `high_latency_p95` alert enabled, inspect RAG spans first during latency events, and apply fallback retrieval or query truncation if retrieval latency dominates.

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]: Nguyễn Hồng Phúc
- [TASKS_COMPLETED]: Nguyễn Hồng Phúc implemented structured JSON logging, correlation ID propagation, and PII redaction.
- [EVIDENCE_LINK]: `app/middleware.py`, `app/logging_config.py`, `app/pii.py`, `tests/test_observability_flow.py`

### [MEMBER_B_NAME]: Nguyễn Hồng Phúc
- [TASKS_COMPLETED]: Nguyễn Hồng Phúc implemented Langfuse tracing, trace metadata enrichment, child spans, and quality scoring.
- [EVIDENCE_LINK]: `app/tracing.py`, `app/agent.py`, Langfuse trace `bd6b0642bfee379c947f9e1d6ecbdbf9`

### [MEMBER_C_NAME]: Nguyễn Hồng Phúc
- [TASKS_COMPLETED]: Nguyễn Hồng Phúc configured SLOs, alert rules, and runbook documentation.
- [EVIDENCE_LINK]: `config/slo.yaml`, `config/alert_rules.yaml`, `docs/alerts.md`, `tests/test_alert_rules.py`

### [MEMBER_D_NAME]: Nguyễn Hồng Phúc
- [TASKS_COMPLETED]: Nguyễn Hồng Phúc ran load-test style sample traffic and built the 6-panel dashboard from exported `/metrics`.
- [EVIDENCE_LINK]: `docs/dashboard.html`, `app/main.py`, `scripts/load_test.py`, `http://127.0.0.1:8010/dashboard`

### [MEMBER_E_NAME]: Nguyễn Hồng Phúc
- [TASKS_COMPLETED]: Nguyễn Hồng Phúc prepared the demo evidence and completed the final observability report.
- [EVIDENCE_LINK]: `docs/blueprint-template.md`, `docs/dashboard-spec.md`, `docs/grading-evidence.md`

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: Cost metrics are tracked per request with `cost_usd`, `avg_cost_usd`, and `total_cost_usd`; evidence in `app/metrics.py`, `/metrics`, and Langfuse trace metadata.
- [BONUS_AUDIT_LOGS]: Not implemented.
- [BONUS_CUSTOM_METRIC]: Implemented `quality_score` as both an in-memory metric and a Langfuse trace score; evidence in `app/agent.py`, `app/metrics.py`, and Langfuse score `quality_score`.
