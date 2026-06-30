# Milestone 2 Artifact Summary - Days 21 to 24

**Student Name:** Thái Thị Yến Nhi  
**Student ID:** 2A202600783  
**Prepared for:** Day 25 - GPU FinOps, Cost Optimization, Quiz, and Milestone 2  

---

## Purpose

This file consolidates the main artifacts from Day 21 to Day 24 for Milestone 2 preparation.

The four labs together cover the Chapter 5 operational stack:

- CI/CD and MLOps automation
- LLMOps, prompt versioning, RAG evaluation, and guardrails
- Monitoring, observability, alerting, tracing, logs, drift detection, and cross-day integration
- Data governance, PII anonymization, RBAC, encryption, policy, and compliance mapping

---

## Repository Links

| Day | Topic | Repository |
|---|---|---|
| Day 21 | MLOps CI/CD, DVC, MLflow, GCP deployment | [Day21 Repository](https://github.com/Lemin9802/Day21_Mlops-Lab_2A202600783_Thai-Thi-Yen-Nhi) |
| Day 22 | LLMOps, prompt versioning, RAGAS, guardrails | [Day22 Repository](https://github.com/Lemin9802/Day22-Lab_2A202600783_Thai-Thi-Yen-Nhi) |
| Day 23 | Observability stack, monitoring, tracing, logging, drift | [Day23 Repository](https://github.com/Lemin9802/Day23-Lab_2A202600783_Thai-Thi-Yen-Nhi) |
| Day 24 | Data governance, PII pipeline, RBAC, security, compliance | [Day24 Repository](https://github.com/Lemin9802/Day24-Lab_2A202600783_Thai-Thi-Yen-Nhi) |

---

## Day 21 - MLOps CI/CD, DVC, MLflow, and Deployment

Main artifacts:

| Area | Evidence / Artifact |
|---|---|
| Data and pipeline versioning | `dvc.yaml`, `dvc.lock` |
| Data generation | `generate_data.py`, `add_new_data.py` |
| Model training | `src/train.py` |
| Model evaluation | `src/evaluate.py`, `outputs/metrics.json` |
| Hyperparameter tuning | `src/tune.py` |
| Daily training report | `src/report.py` |
| Label shift check | `src/check_label_shift.py` |
| Model serving | `src/serve.py` |
| CI/CD workflow | `.github/workflows/mlops.yml` |
| Regression gate | `config/baseline_metrics.json` |
| Submission evidence | `submission/`, `submission/REPORT.md`, `submission/screenshots/` |

Verified results:

| Item | Result |
|---|---|
| Final model | RandomForestClassifier |
| Selected hyperparameters | `n_estimators=200`, `max_depth=10`, `min_samples_split=2` |
| Best tuning accuracy | 0.6480 |
| Best weighted F1 score | 0.6464 |
| Deployment evidence | FastAPI health and prediction screenshots |
| Cloud artifact evidence | GCS screenshot included |
| DagsHub / MLflow evidence | Included in bonus evidence screenshots |

Milestone 2 relevance:

Day 21 demonstrates reproducible MLOps, CI/CD gates, experiment tracking, remote artifact storage, model evaluation, and deployment evidence.

---

## Day 22 - LLMOps, Prompt Versioning, RAG Evaluation, and Guardrails

Main artifacts:

| Area | Evidence / Artifact |
|---|---|
| PDF-based RAG pipeline | `src/01_langsmith_rag_pipeline.py` |
| Data loader and retriever | `src/utils/data_loader.py` |
| LLM factory | `src/utils/llm_factory.py` |
| QA set | `src/qa_pairs.py` |
| Prompt Hub and A/B routing | `src/02_prompt_hub_ab_routing.py` |
| RAGAS evaluation | `src/03_ragas_evaluation.py` |
| Guardrails validators | `src/04_guardrails_validator.py` |
| Unified runner | `src/run_all.py` |
| LangSmith evidence | `evidence/01_langsmith_traces.png`, `evidence/01_langsmith_project_overview.png` |
| Prompt Hub evidence | `evidence/02_prompt_hub.png` |
| A/B routing log | `evidence/02_ab_routing_log.txt` |
| RAGAS reports | `evidence/03_ragas_report.json`, `evidence/03_ragas_rows.csv`, `data/ragas_report.json` |
| Guardrails logs | `evidence/04_pii_demo_log.txt`, `evidence/04_json_demo_log.txt` |

RAGAS results:

| Metric | Overall | V1 | V2 |
|---|---:|---:|---:|
| Faithfulness | 0.9717 | 0.9543 | 0.9940 |
| Answer relevancy | 0.8182 | 0.8472 | 0.7891 |
| Context recall | 0.9617 | 0.9580 | 0.9654 |
| Context precision | 0.8889 | 0.8333 | 0.9167 |

Additional results:

| Item | Result |
|---|---|
| LangSmith project | `day22-lab` |
| Successful traces | More than 50 |
| Error rate | 0% |
| Prompt V1 route count | 29 |
| Prompt V2 route count | 21 |
| Total RAGAS evaluated samples | 100 |
| LLM model | `qwen2.5:7b` |
| Embedding model | `nomic-embed-text` |

Milestone 2 relevance:

Day 22 demonstrates LLMOps traceability, prompt versioning, deterministic A/B routing, RAG quality evaluation, and guardrails for safer outputs.

---

## Day 23 - Observability, Monitoring, Tracing, Logging, and Drift

Main artifacts:

| Area | Evidence / Artifact |
|---|---|
| FastAPI instrumentation | `01-instrument-fastapi/app/` |
| Prometheus and Grafana | `02-prometheus-grafana/` |
| Grafana dashboards | `02-prometheus-grafana/grafana/dashboards/` |
| Alertmanager | `02-prometheus-grafana/alertmanager/` |
| Loki | `03-tracing-and-logs/loki/` |
| OpenTelemetry Collector | `03-tracing-and-logs/otel-collector/` |
| Drift detection | `04-drift-detection/` |
| Cross-day integration | `05-integration/` |
| Final reflection and checklist | `submission/REFLECTION.md` |
| Final verification log | `submission/make-verify.log` |
| Screenshots | `submission/screenshots/` |

Verified results:

| Item | Result |
|---|---|
| Final verification | 12/12 checks passed |
| Metrics dashboard | AI Service Overview dashboard included |
| SLO dashboard | SLO Burn Rate dashboard included |
| Cost dashboard | Cost & Tokens dashboard included |
| Cross-day dashboard | Day19 Qdrant and Day20 llama.cpp metrics included |
| Alerting | Alertmanager and Slack firing/resolved evidence included |
| Tracing | Jaeger trace evidence included |
| Logs | JSON logs with trace ID included |
| Drift detected | `prompt_length`, `response_quality` |
| No meaningful drift | `embedding_norm`, `response_length` |

Milestone 2 relevance:

Day 23 demonstrates production-style observability with metrics, dashboards, alerts, traces, structured logs, drift detection, and cross-day operational integration.

---

## Day 24 - Data Governance, PII Pipeline, RBAC, Security, and Compliance

Main artifacts:

| Area | Evidence / Artifact |
|---|---|
| Main implementation | `medviet-governance/` |
| Instructor notebook and agent governance reference | `data-governance-lab/` |
| PII detector | `medviet-governance/src/pii/detector.py` |
| PII anonymizer | `medviet-governance/src/pii/anonymizer.py` |
| Generated anonymized dataset | `medviet-governance/data/processed/patients_anonymized.csv` |
| RBAC policy and module | `medviet-governance/src/access/policy.csv`, `medviet-governance/src/access/rbac.py` |
| FastAPI RBAC API | `medviet-governance/src/api/main.py` |
| Envelope encryption | `medviet-governance/src/encryption/vault.py` |
| Data validation | `medviet-governance/src/quality/validation.py` |
| OPA policy | `medviet-governance/policies/opa_policy.rego` |
| Compliance checklist | `medviet-governance/compliance_checklist.md` |
| Reports | `medviet-governance/reports/` |
| Lab scope evidence | `medviet-governance/reports/lab_scope_evidence.md` |

Verified results:

| Check | Result |
|---|---:|
| PII detection rate | 100.00% |
| PII tests | 6 passed |
| Encryption round trip | Passed |
| Bandit SAST | No issues identified |
| TruffleHog | PASS, 0 verified findings |
| pip-audit | Reviewed with mitigation |
| Raw PII committed | No |
| Local vault key committed | No |

Actual output evidence:

    Detection rate: 100.00%
    Saved anonymized data to data\processed\patients_anonymized.csv

    BN_0001  patient.0001@example.com  Ocean Park 1, Gia Lâm, Hà Nội        BS. Nguyễn Hoài An
    BN_0002  patient.0002@example.net  Ocean Park 1, Gia Lâm, Hà Nội        BS. Lê Thanh Huyền
    BN_0003  patient.0003@example.org  Ocean Park 1, Gia Lâm, Hà Nội        BS. Phạm Thu Trang

    6 passed
    Encryption test passed

Milestone 2 relevance:

Day 24 demonstrates data governance and security controls around PII minimization, anonymization, least-privilege access, policy enforcement, encryption, security scanning, and compliance mapping.

---

## Chapter 5 Mapping

| Chapter 5 Area | Day | Evidence |
|---|---|---|
| CI/CD | Day 21 | GitHub Actions workflow, test gate, eval gate, deploy workflow |
| MLOps | Day 21 | DVC, MLflow, DagsHub, model artifacts |
| LLMOps | Day 22 | LangSmith tracing, Prompt Hub, prompt A/B routing, RAGAS |
| Guardrails | Day 22 | PII validator and JSON formatter validator |
| Monitoring | Day 23 | Prometheus metrics and Grafana dashboards |
| Alerting | Day 23 | Alertmanager and firing/resolved evidence |
| Tracing | Day 23 | Jaeger trace with GenAI span attributes |
| Logs | Day 23 | Structured JSON logs with trace correlation |
| Drift Detection | Day 23 | Drift summary and Evidently report |
| Governance | Day 24 | RBAC, OPA, compliance checklist |
| Data Security | Day 24 | PII anonymization, encryption, security reports |

---

## Milestone 2 Readiness Checklist

| Item | Status | Evidence |
|---|---:|---|
| Day 21 artifacts documented | Done | Day 21 README and submission folder |
| Day 22 artifacts documented | Done | Day 22 README and evidence folder |
| Day 23 artifacts documented | Done | Day 23 README and submission folder |
| Day 24 lab completed | Done | Day 24 README and medviet-governance folder |
| Security and audit evidence included | Done | Day 24 reports folder |
| Chapter 5 concepts mapped to artifacts | Done | Mapping table above |
| Cross-day operational story prepared | Done | This file |
| Raw data and local keys excluded | Done | Day 24 repository checks |
| Production-only controls documented honestly | Done | Day 24 compliance checklist and lab scope evidence |

---

## One-Slide Milestone 2 Narrative

From Day 21 to Day 24, the work builds a progressively more production-ready AI platform:

1. Day 21 establishes reproducible MLOps with DVC, MLflow, CI/CD, evaluation gates, and deployment evidence.
2. Day 22 adds LLMOps capabilities through LangSmith tracing, prompt versioning, RAG evaluation, and guardrails.
3. Day 23 adds observability through metrics, dashboards, alerts, traces, logs, drift detection, and cross-day integration.
4. Day 24 adds governance and security through PII detection, anonymization, RBAC, OPA policy, encryption, security scans, and ND13 compliance mapping.

Together, these artifacts show the Milestone 2 operational foundation: CI/CD, LLMOps, Monitoring, and Governance.
