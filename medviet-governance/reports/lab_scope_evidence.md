# Lab Scope and Evidence Summary

This file explains which requirements are implemented in the repository and which controls are documented as production deployment requirements.

## Lab Deliverables Completed

| Lab requirement | Status | Evidence |
|---|---:|---|
| Vietnamese PII detection | Done | src/pii/detector.py |
| PII anonymization pipeline | Done | src/pii/anonymizer.py, data/processed/patients_anonymized.csv |
| Detection rate above 95% | Done | reports/test_results.txt, script output shows 100.00% |
| RBAC demo with multiple roles | Done | src/access/policy.csv, src/access/rbac.py, src/api/main.py |
| FastAPI data access endpoints | Done | src/api/main.py |
| Encryption at rest demo | Done | src/encryption/vault.py |
| Security audit reports | Done | reports/bandit_report.json, reports/trufflehog_report.txt, reports/pip_audit_report.txt |
| OPA policy | Done | policies/opa_policy.rego |
| ND13 compliance mapping | Done | compliance_checklist.md |
| Raw data exclusion | Done | .gitignore excludes raw CSV and vault key |

## Production Controls Documented but Not Deployed

The following controls are intentionally documented as production requirements instead of being marked as fully implemented in this local lab repository.

| Production control | Why it is not marked fully done |
|---|---|
| TLS 1.3 gateway enforcement | Requires production API gateway or reverse proxy deployment |
| SIEM / centralized audit logging | Requires deployed infrastructure and log storage |
| Prometheus/Grafana breach detection | Requires monitoring stack deployment |
| DPO appointment | Organizational governance process, not local code |
| Consent management database | Requires real user identity and consent system |
| Backup localization policy | Requires production storage and backup infrastructure |
| KMS/HSM key management | Requires cloud or enterprise secrets infrastructure |

## Summary

The lab implementation is complete for the required technical scope. Production-only compliance controls are mapped to concrete technical solutions in the compliance checklist instead of being incorrectly marked as fully deployed.
