# Lab 24 Execution Checkpoints

Use this file while completing the lab on branch `lab24-implementation`.

## Checkpoint 0 — Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Expected: packages install successfully.

## Checkpoint 1 — Generate raw data

```bash
python scripts/generate_data.py
```

Expected:
- `data/raw/patients_raw.csv` exists.
- Console prints 200 rows generated.
- Raw CSV is ignored by git.

## Checkpoint 2 — Run anonymization pipeline

```bash
python scripts/run_anonymization.py
```

Expected:
- Detection rate is at least 95%.
- `data/processed/patients_anonymized.csv` exists.
- PII columns are replaced or generalized.

## Checkpoint 3 — Run PII tests

```bash
pytest tests/test_pii.py -v --tb=short
```

Expected: all tests pass.

## Checkpoint 4 — Run RBAC API

```bash
uvicorn src.api.main:app --reload
```

In another terminal:

```bash
curl -H "Authorization: Bearer token-bob" http://localhost:8000/api/patients/raw
curl -H "Authorization: Bearer token-alice" http://localhost:8000/api/patients/raw
curl -H "Authorization: Bearer token-carol" http://localhost:8000/api/metrics/aggregated
curl -X DELETE -H "Authorization: Bearer token-bob" http://localhost:8000/api/patients/abc123
```

Expected:
- Bob raw data request returns 403.
- Alice raw data request returns 200.
- Carol aggregated metrics request returns 200.
- Bob delete request returns 403.

## Checkpoint 5 — Encryption round-trip

```bash
python src/encryption/vault.py
```

Expected: `Encryption test passed`.

## Checkpoint 6 — Security audit reports

```bash
mkdir -p reports
pytest tests/ -v --tb=short > reports/test_results.txt
bandit -r src/ -f json -o reports/bandit_report.json
trufflehog git file://. --only-verified > reports/trufflehog_report.txt
```

Expected:
- `reports/test_results.txt`
- `reports/bandit_report.json`
- `reports/trufflehog_report.txt`

## Checkpoint 7 — OPA policy

```bash
echo '{
  "user": {"role": "ml_engineer"},
  "resource": "production_data",
  "action": "delete"
}' | opa eval -d policies/opa_policy.rego -I "data.medviet.data_access.allow"
```

Expected: false.

## Checkpoint 8 — Final package

```bash
zip -r lab24_submission_<ten_sv>.zip \
    src/ tests/ policies/ data/processed/ \
    compliance_checklist.md reports/ requirements.txt
```

Do not include:
- `data/raw/`
- `.vault_key`
- real credentials
- `test_secret.py`
