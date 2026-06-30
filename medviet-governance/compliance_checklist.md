# ND13/2023 Compliance Checklist - MedViet AI Platform

## Scope Note

This checklist separates completed lab controls from production-only governance controls.

Items marked **Done** are implemented in this repository. Items marked **Planned** are not missing lab work; they are production deployment or organizational controls that require real infrastructure, SIEM, TLS gateway, KMS/HSM, consent system, DPO ownership, or incident response process.

The lab deliverables are completed in `medviet-governance/` and supported by the evidence files in `medviet-governance/reports/`.


﻿# ND13/2023 Compliance Checklist - MedViet AI Platform

This checklist maps the implemented MedViet data governance controls to ND13/2023-style privacy requirements and ISO 27001-style technical safeguards.

The project is a lab implementation, so production-only controls such as real SIEM integration, TLS termination, KMS/HSM, and formal DPO appointment are documented as planned controls.

---

## A. Data Localization

| Control | Status | Evidence / Implementation |
|---|---:|---|
| Patient-like raw data is not committed to Git | Done | `.gitignore` excludes `data/raw/*.csv` and `**/data/raw/*.csv` |
| Only anonymized processed data is submitted | Done | `medviet-governance/data/processed/patients_anonymized.csv` |
| Restricted data export outside Vietnam is denied by policy | Done | `medviet-governance/policies/opa_policy.rego` |
| Production storage must be located in Vietnam | Planned | Deployment requirement for production infrastructure |
| Backups must remain within Vietnam | Planned | Production backup policy requirement |

---

## B. Explicit Consent

| Control | Status | Evidence / Implementation |
|---|---:|---|
| Consent must be collected before using patient data for AI training | Planned | Production consent-management requirement |
| Consent records should include timestamp, purpose, data scope, and consent version | Planned | Production consent database requirement |
| Users must be able to withdraw consent | Planned | Data subject request workflow documented below |
| Raw data and anonymized training data are separated | Done | Raw data excluded from Git; anonymized output generated separately |

Implementation note:

The lab does not process real patient data. For production, MedViet should maintain a consent table linked to `patient_id`, training purpose, consent timestamp, consent version, and withdrawal status.

---

## C. Breach Notification - 72 Hours

| Control | Status | Evidence / Implementation |
|---|---:|---|
| Incident response plan for data breach | Planned | Production runbook requirement |
| Alerting for abnormal access or PII exposure | Planned | Prometheus/Grafana or SIEM integration |
| 72-hour notification procedure | Planned | Compliance process requirement |
| Secret scanning included in submission | Done | `medviet-governance/reports/trufflehog_report.txt` |
| Static security scanning included in submission | Done | `medviet-governance/reports/bandit_report.json` |
| Dependency audit included in submission | Done with mitigation | `medviet-governance/reports/pip_audit_report.txt` and `pip_audit_mitigation.md` |

---

## D. DPO Appointment

| Control | Status | Evidence / Implementation |
|---|---:|---|
| Data Protection Officer appointed | Planned | Production governance requirement |
| DPO contact channel defined | Planned | Example: `dpo@medviet.example.vn` |
| DPO reviews DPIA, consent flow, breach response, and audit evidence | Planned | Production compliance workflow |
| Technical evidence prepared for review | Done | Reports and source files are included in the repository |

---

## E. Technical Controls Mapping

| ND13 Requirement | Technical Control | Status | Evidence / File | Owner |
|---|---|---:|---|---|
| Data minimization | PII detection and anonymization before training ingestion | Done | `src/pii/detector.py`, `src/pii/anonymizer.py` | AI Team |
| PII protection | CCCD, phone, email, person name detection | Done | `src/pii/detector.py` | AI Team |
| Anonymization | Names, emails, CCCD, phone numbers, addresses, doctors, and birth dates anonymized or generalized | Done | `data/processed/patients_anonymized.csv` | AI Team |
| Utility preservation | Disease labels, lab results, patient IDs, and visit dates preserved for ML use | Done | `src/pii/anonymizer.py` | AI Team |
| Purpose limitation | Raw data, anonymized training data, and aggregated metrics are separated by resource/API endpoint | Done | `src/api/main.py` | AI Team |
| Access control | Casbin RBAC in FastAPI | Done | `src/access/rbac.py`, `src/access/policy.csv` | Platform Team |
| Least privilege | Admin, ML engineer, data analyst, and intern roles enforce different access levels | Done | `src/access/policy.csv` | Platform Team |
| Raw PII restriction | Raw patient data endpoint is admin-only | Done | `src/api/main.py` | Platform Team |
| Data localization | Restricted data export outside Vietnam is denied | Done | `policies/opa_policy.rego` | Platform Team |
| Encryption at rest | Local AES-256-GCM envelope encryption demo | Done for lab | `src/encryption/vault.py` | Infra Team |
| Production key management | Replace local `.vault_key` with KMS/HSM | Planned | Production architecture requirement | Infra Team |
| Encryption in transit | Enforce HTTPS/TLS 1.3 at API gateway or reverse proxy | Planned | Production deployment requirement | Infra Team |
| Audit logging | Log user, role, resource, action, decision, status code, and timestamp | Planned | FastAPI middleware recommended below | Platform Team |
| Breach detection | Alert on failed auth, 403 spikes, and abnormal raw PII access | Planned | Prometheus/Grafana or SIEM recommended below | Security Team |
| Secret protection | Secret scanning and security reports included | Done | `reports/trufflehog_report.txt`, `reports/bandit_report.json` | Security Team |
| Dependency security | pip-audit report included with mitigation note | Reviewed | `reports/pip_audit_report.txt`, `reports/pip_audit_mitigation.md` | Security Team |
| Data subject request | Delete cascade across raw store, processed store, backups, feature store, and model registry | Planned | Production deletion playbook | Data Governance Team |

---

## F. Implemented Evidence Summary

### PII Detection and Anonymization

Evidence:

- `medviet-governance/src/pii/detector.py`
- `medviet-governance/src/pii/anonymizer.py`
- `medviet-governance/data/processed/patients_anonymized.csv`
- `medviet-governance/reports/test_results.txt`

Verified local result:

    Detection rate: 100.00%
    Saved anonymized data to data\processed\patients_anonymized.csv

Processed data preview:

    BN_0001  patient.0001@example.com  Ocean Park 1, Gia Lâm, Hà Nội      BS. Nguyễn Hoài An
    BN_0002  patient.0002@example.net  Ocean Park 1, Gia Lâm, Hà Nội      BS. Lê Thanh Huyền
    BN_0003  patient.0003@example.org  Ocean Park 1, Gia Lâm, Hà Nội      BS. Phạm Thu Trang

---

### RBAC and Least Privilege

Evidence:

- `medviet-governance/src/access/model.conf`
- `medviet-governance/src/access/policy.csv`
- `medviet-governance/src/access/rbac.py`
- `medviet-governance/src/api/main.py`

Verified behavior:

| Test case | Expected result |
|---|---|
| Bob reads raw patient data | 403 Forbidden |
| Alice reads raw patient data | 200 OK |
| Carol reads aggregated metrics | 200 OK |
| Bob deletes patient data | 403 Forbidden |

---

### Encryption

Evidence:

- `medviet-governance/src/encryption/vault.py`

Verified output:

    Encryption test passed

Production note:

The local `.vault_key` is only for lab demonstration and is excluded from Git. In production, the Key Encryption Key should be stored in a KMS/HSM instead of a local file.

---

### Security Reports

Evidence:

- `medviet-governance/reports/test_results.txt`
- `medviet-governance/reports/bandit_report.json`
- `medviet-governance/reports/trufflehog_report.txt`
- `medviet-governance/reports/pip_audit_report.txt`
- `medviet-governance/reports/pip_audit_mitigation.md`

Verified summary:

| Report | Result |
|---|---|
| Pytest | 6 passed |
| Bandit | No issues identified |
| TruffleHog | PASS, 0 verified secrets, 0 unverified secrets |
| pip-audit | Reviewed with mitigation |

pip-audit note:

`cryptography` is pinned to `>=46.0.4,<47.0.0` because `presidio-anonymizer` requires that version range. Upgrading to `cryptography >=48.0.1` creates a dependency conflict and may break the PII anonymization pipeline. The mitigation is documented in `reports/pip_audit_mitigation.md`.

---

## G. Remaining Production Implementation Notes

### Audit Logging

Implement FastAPI middleware that writes structured JSON logs with:

- `request_id`
- `username`
- `role`
- `resource`
- `action`
- `allowed`
- `status_code`
- `timestamp`

Recommended storage:

- write-once audit bucket
- centralized SIEM
- restricted access log store

---

### Breach Detection

Create Prometheus counters or SIEM rules for:

- failed login attempts
- denied RBAC requests
- abnormal raw PII endpoint access
- repeated access from the same token
- unusual export requests

Configure Grafana or SIEM alerts for abnormal spikes and trigger the incident response workflow.

---

### TLS and Deployment

For production deployment:

- terminate TLS 1.3 at Nginx, Traefik, or a cloud load balancer
- reject plain HTTP
- enable HSTS
- rotate certificates automatically
- restrict internal service-to-service traffic

---

### Data Subject Request

Maintain an index from real user identity to `patient_id`.

A deletion request should remove or invalidate data from:

- raw data store
- processed anonymized store when applicable
- feature store
- cached artifacts
- training queues
- backup retention workflow
- model registry metadata when applicable

---

## H. Final Compliance Status

| Area | Status |
|---|---:|
| Data minimization | Done |
| PII anonymization | Done |
| RBAC least privilege | Done |
| OPA data export policy | Done |
| Encryption demo | Done for lab |
| Security scans | Done |
| Compliance mapping | Done |
| Production audit logging | Planned |
| Production TLS enforcement | Planned |
| Production DPO process | Planned |
| Production data subject request workflow | Planned |

Overall status: lab implementation complete, with production-only controls documented as future deployment requirements.
