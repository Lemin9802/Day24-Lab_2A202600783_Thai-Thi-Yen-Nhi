cd "C:\Users\THAI NHI\Desktop\VinUni\Day24-Track02-Lab-Assignment"

@'
# MedViet Data Governance & Security Lab

**Course:** AICB-P2T2 - Lab #24 Extended  
**Submission Day:** 30 June 2026  
**Student Name:** Thái Thị Yến Nhi  
**Student ID:** 2A202600783  

---

## Quick Links for Grading

| Area | Link |
|---|---|
| Main implementation folder | [medviet-governance/](./medviet-governance/) |
| Instructor notebook and agent governance materials | [data-governance-lab/](./data-governance-lab/) |
| PII detector | [src/pii/detector.py](./medviet-governance/src/pii/detector.py) |
| PII anonymizer | [src/pii/anonymizer.py](./medviet-governance/src/pii/anonymizer.py) |
| RBAC policy | [src/access/policy.csv](./medviet-governance/src/access/policy.csv) |
| RBAC module | [src/access/rbac.py](./medviet-governance/src/access/rbac.py) |
| FastAPI application | [src/api/main.py](./medviet-governance/src/api/main.py) |
| Encryption vault | [src/encryption/vault.py](./medviet-governance/src/encryption/vault.py) |
| Data validation | [src/quality/validation.py](./medviet-governance/src/quality/validation.py) |
| OPA policy | [policies/opa_policy.rego](./medviet-governance/policies/opa_policy.rego) |
| Compliance checklist | [compliance_checklist.md](./medviet-governance/compliance_checklist.md) |
| Tests | [tests/test_pii.py](./medviet-governance/tests/test_pii.py) |
| Generated anonymized dataset | [data/processed/patients_anonymized.csv](./medviet-governance/data/processed/patients_anonymized.csv) |
| Security and test reports | [reports/](./medviet-governance/reports/) |
| Lab scope evidence | [lab_scope_evidence.md](./medviet-governance/reports/lab_scope_evidence.md) |
| Data governance notebook README | [data-governance-lab/README.md](./data-governance-lab/README.md) |
| Agent governance policy reference | [medviet-data-policy.yaml](./data-governance-lab/policies/medviet-data-policy.yaml) |

---

## Latest Verified Results

| Check | Result | Evidence |
|---|---:|---|
| PII detection rate | 100.00% | Output from `scripts/run_anonymization.py` |
| PII unit tests | 6 passed | [reports/test_results.txt](./medviet-governance/reports/test_results.txt) |
| Encryption round trip | Passed | Output from `src/encryption/vault.py` |
| Bandit SAST | No issues identified | [reports/bandit_report.json](./medviet-governance/reports/bandit_report.json) |
| TruffleHog secret scan | PASS, 0 verified secrets | [reports/trufflehog_report.txt](./medviet-governance/reports/trufflehog_report.txt) |
| pip-audit | Reviewed with mitigation | [reports/pip_audit_report.txt](./medviet-governance/reports/pip_audit_report.txt), [reports/pip_audit_mitigation.md](./medviet-governance/reports/pip_audit_mitigation.md) |
| Raw PII data committed | No | Enforced through [.gitignore](./.gitignore) |

Actual anonymization output:

    Detection rate: 100.00%
    Saved anonymized data to data\processed\patients_anonymized.csv

Actual processed-data preview:

    ho_ten   email                     dia_chi                              bac_si_phu_trach
    BN_0001  patient.0001@example.com  Ocean Park 1, Gia Lâm, Hà Nội        BS. Nguyễn Hoài An
    BN_0002  patient.0002@example.net  Ocean Park 1, Gia Lâm, Hà Nội        BS. Lê Thanh Huyền
    BN_0003  patient.0003@example.org  Ocean Park 1, Gia Lâm, Hà Nội        BS. Phạm Thu Trang
    BN_0004  patient.0004@example.com  Ocean Park 1, Gia Lâm, Hà Nội        BS. Đỗ Ngọc Minh
    BN_0005  patient.0005@example.net  Ocean Park 1, Gia Lâm, Hà Nội        BS. Trần Bảo Ngọc
    BN_0006  patient.0006@example.org  Ocean Park 2, Văn Giang, Hưng Yên    BS. Lê Quang Hưng
    BN_0007  patient.0007@example.com  Ocean Park 2, Văn Giang, Hưng Yên    BS. Vũ Minh Châu
    BN_0008  patient.0008@example.net  Ocean Park 2, Văn Giang, Hưng Yên    BS. Đặng Gia Khánh
    BN_0009  patient.0009@example.org  Ocean Park 2, Văn Giang, Hưng Yên    BS. Nguyễn Hoài An
    BN_0010  patient.0010@example.com  Ocean Park 3, Văn Giang, Hưng Yên    BS. Lê Thanh Huyền

Actual pytest output:

    tests/test_pii.py::TestPIIDetection::test_cccd_detected PASSED
    tests/test_pii.py::TestPIIDetection::test_phone_detected PASSED
    tests/test_pii.py::TestPIIDetection::test_email_detected PASSED
    tests/test_pii.py::TestPIIDetection::test_detection_rate_above_95_percent PASSED
    tests/test_pii.py::TestAnonymization::test_pii_not_in_output PASSED
    tests/test_pii.py::TestAnonymization::test_non_pii_columns_unchanged PASSED

    6 passed

Actual encryption output:

    Encryption test passed

Actual Bandit output:

    Test results:
        No issues identified.

Actual TruffleHog report summary:

    Status: PASS

    Summary:
    - Verified secrets: 0
    - Unverified secrets: 0

Actual pip-audit result:

    Status: REVIEWED WITH MITIGATION

    Summary:
    - Known vulnerabilities found: 1
    - Affected package: cryptography 46.0.7
    - Advisory ID: GHSA-537c-gmf6-5ccf
    - Fixed version suggested by audit: 48.0.1

    Reason for not upgrading in this lab:
    presidio-anonymizer requires cryptography >=46.0.4,<47.0.0. Upgrading cryptography to 49.0.0 creates a dependency conflict and may break the PII anonymization pipeline.

---

## Project Overview

This repository contains the completed implementation for the MedViet Data Governance & Security for AI Platform lab.

The lab simulates a Vietnamese healthcare AI startup, MedViet, that processes patient records for machine learning while needing to satisfy privacy, governance, security, and compliance requirements. The implementation protects personally identifiable information, enforces least-privilege access control, encrypts sensitive data, validates anonymized data quality, scans for security risks, and maps the controls to Vietnamese data protection requirements.

The completed implementation is in:

[medviet-governance/](./medviet-governance/)

The instructor-provided notebook and Agent Governance reference materials are kept in:

[data-governance-lab/](./data-governance-lab/)

---

## Repository Structure

| Path | Description |
|---|---|
| [medviet-governance/](./medviet-governance/) | Main completed lab implementation |
| [medviet-governance/src/](./medviet-governance/src/) | Source code for PII, RBAC, API, encryption, and validation |
| [medviet-governance/scripts/](./medviet-governance/scripts/) | Data generation and anonymization scripts |
| [medviet-governance/tests/](./medviet-governance/tests/) | Automated PII detection and anonymization tests |
| [medviet-governance/policies/](./medviet-governance/policies/) | OPA data access policy |
| [medviet-governance/reports/](./medviet-governance/reports/) | Test and security scan reports |
| [medviet-governance/data/processed/](./medviet-governance/data/processed/) | Anonymized dataset submitted with the repo |
| [data-governance-lab/](./data-governance-lab/) | Instructor notebook and Agent Governance reference material |
| [.github/hooks/pre-commit](./.github/hooks/pre-commit) | Security pre-commit hook example |
| [.gitignore](./.gitignore) | Excludes raw PII data, keys, virtual environments, and temporary files |

---

## Implemented Features

### 1. Vietnamese PII Detection

Implemented custom Presidio recognizers for Vietnamese healthcare data.

Detected entities:

| Entity | Description |
|---|---|
| `VN_CCCD` | Vietnamese 12-digit citizen ID |
| `VN_PHONE` | Vietnamese mobile phone number |
| `EMAIL_ADDRESS` | Email address |
| `PERSON` | Vietnamese person name pattern |

Main files:

- [detector.py](./medviet-governance/src/pii/detector.py)
- [anonymizer.py](./medviet-governance/src/pii/anonymizer.py)

The detector uses custom pattern recognizers and fallback logic so the pipeline can run even when a full Vietnamese spaCy NER model is not available.

---

### 2. PII Anonymization Pipeline

Implemented a full anonymization pipeline for patient records.

| Raw column | Treatment in processed data |
|---|---|
| `ho_ten` | Replaced with stable anonymized IDs such as `BN_0001` |
| `cccd` | Replaced with generated fake CCCD values |
| `so_dien_thoai` | Replaced with generated fake Vietnamese phone numbers |
| `email` | Replaced with safe synthetic emails such as `patient.0001@example.com` |
| `dia_chi` | Generalized to Ocean Park area level, removing exact apartment or unit details |
| `bac_si_phu_trach` | Replaced with synthetic doctor names |
| `ngay_sinh` | Generalized to decade level |

ML-useful columns preserved:

- `patient_id`
- `benh`
- `ket_qua_xet_nghiem`
- `ngay_kham`

Generated anonymized output:

[patients_anonymized.csv](./medviet-governance/data/processed/patients_anonymized.csv)

The raw dataset is intentionally not committed because it contains patient-like PII.

---

### 3. RBAC with Casbin and FastAPI

Implemented role-based access control using Casbin and FastAPI.

Roles and demo tokens:

| User | Token | Role |
|---|---|---|
| Alice | `token-alice` | `admin` |
| Bob | `token-bob` | `ml_engineer` |
| Carol | `token-carol` | `data_analyst` |
| Dave | `token-dave` | `intern` |

Implemented API rules:

| Endpoint | Access rule |
|---|---|
| `GET /api/patients/raw` | Admin only |
| `GET /api/patients/anonymized` | Admin and ML engineer |
| `GET /api/metrics/aggregated` | Admin, ML engineer, and data analyst |
| `DELETE /api/patients/{patient_id}` | Admin only |

Main files:

- [model.conf](./medviet-governance/src/access/model.conf)
- [policy.csv](./medviet-governance/src/access/policy.csv)
- [rbac.py](./medviet-governance/src/access/rbac.py)
- [main.py](./medviet-governance/src/api/main.py)

Verified behavior:

- Bob is denied access to raw PII.
- Alice can read raw patient data.
- Carol can read aggregated metrics.
- Bob cannot delete patient data.

---

### 4. Envelope Encryption

Implemented local envelope encryption with AES-256-GCM.

Encryption pattern:

    Master Key / KEK -> encrypts Data Key / DEK -> encrypts data

Main file:

[encryption/vault.py](./medviet-governance/src/encryption/vault.py)

The local `.vault_key` is generated only for local development and is excluded from Git.

Verified output:

    Encryption test passed

---

### 5. Data Quality Validation

Implemented validation checks for anonymized patient data.

Checks include:

- Required columns
- Non-null critical fields
- Valid disease categories
- Valid lab result range
- Unique `patient_id`
- Row count consistency
- Original direct identifiers are not retained

Main file:

[quality/validation.py](./medviet-governance/src/quality/validation.py)

---

### 6. Security Scanning

Security and test reports are included in:

[medviet-governance/reports/](./medviet-governance/reports/)

| Report | Link | Result |
|---|---|---|
| Pytest | [test_results.txt](./medviet-governance/reports/test_results.txt) | 6 passed |
| Bandit | [bandit_report.json](./medviet-governance/reports/bandit_report.json) | No issues identified |
| TruffleHog | [trufflehog_report.txt](./medviet-governance/reports/trufflehog_report.txt) | PASS, 0 verified secrets |
| pip-audit | [pip_audit_report.txt](./medviet-governance/reports/pip_audit_report.txt) | Reviewed with mitigation |
| pip-audit mitigation | [pip_audit_mitigation.md](./medviet-governance/reports/pip_audit_mitigation.md) | Dependency constraint explained |

---

### 7. OPA Policy

Implemented Open Policy Agent rules for governance-level data access control.

Policy includes:

- Default deny
- Admin full access
- ML engineer access to training data and model artifacts
- Data analyst access to aggregated metrics and reports
- Intern access only to sandbox data
- Deny export of restricted data outside Vietnam

Main file:

[opa_policy.rego](./medviet-governance/policies/opa_policy.rego)

---

### 8. Compliance Checklist

Completed a compliance checklist mapping technical controls to Vietnamese data protection and ISO 27001-style requirements.

Covered areas:

- Data localization
- Consent management
- Data minimization
- Access control
- Encryption
- Audit logging
- Breach notification
- Data Protection Officer ownership
- Production hardening recommendations

Main file:

[compliance_checklist.md](./medviet-governance/compliance_checklist.md)

---

## How to Run

From the repository root:

    .\.venv\Scripts\Activate.ps1
    cd medviet-governance

Install dependencies:

    python -m pip install --upgrade pip setuptools wheel
    python -m pip install -r requirements.txt

Generate local raw data:

    python scripts/generate_data.py

Run anonymization:

    python scripts/run_anonymization.py

Run tests:

    python -m pytest tests/test_pii.py -v --tb=short

Test encryption:

    python src/encryption/vault.py

Run the FastAPI RBAC demo:

    python -m uvicorn src.api.main:app --reload

Example API checks:

    curl -H "Authorization: Bearer token-bob" http://localhost:8000/api/patients/raw
    curl -H "Authorization: Bearer token-alice" http://localhost:8000/api/patients/raw
    curl -H "Authorization: Bearer token-carol" http://localhost:8000/api/metrics/aggregated
    curl -X DELETE -H "Authorization: Bearer token-bob" http://localhost:8000/api/patients/abc123

---

## Privacy and Submission Notes

The following files are intentionally excluded from Git:

- `data/raw/*.csv`
- `.vault_key`
- `.venv/`
- `test_secret.py`
- `*.zip`
- temporary audit logs such as `trufflehog_raw.log` and `pip_audit_raw.txt`

This prevents raw patient-like data, local encryption keys, virtual environments, archives, and test credentials from being committed.

Only the anonymized processed dataset is included:

[patients_anonymized.csv](./medviet-governance/data/processed/patients_anonymized.csv)

No raw PII data, local vault key, virtual environment, temporary audit logs, or test secret file is committed.

Production-only controls are documented as planned controls, not omitted work.

---

## Lab Deliverables Mapping

| Requirement | Implementation |
|---|---|
| PII detection rate >= 95% | Implemented and tested; achieved 100.00% |
| PII anonymization | Implemented in [anonymizer.py](./medviet-governance/src/pii/anonymizer.py) |
| RBAC API | Implemented with Casbin and FastAPI |
| Encryption at rest demo | Implemented with AES-256-GCM envelope encryption |
| Security scanning | Bandit, TruffleHog, and pip-audit reports included |
| OPA policy | Implemented in [opa_policy.rego](./medviet-governance/policies/opa_policy.rego) |
| Compliance checklist | Completed in [compliance_checklist.md](./medviet-governance/compliance_checklist.md) |
| Raw data exclusion | Enforced through [.gitignore](./.gitignore) |
