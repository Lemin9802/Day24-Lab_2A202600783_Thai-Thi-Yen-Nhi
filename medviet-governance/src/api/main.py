"""FastAPI demo for MedViet RBAC data access."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from fastapi import Depends, FastAPI

from src.access.rbac import get_current_user, require_permission
from src.pii.anonymizer import MedVietAnonymizer

app = FastAPI(title="MedViet Data API", version="1.0.0")
anonymizer = MedVietAnonymizer()

RAW_DATA_PATH = Path("data/raw/patients_raw.csv")
PROCESSED_DATA_PATH = Path("data/processed/patients_anonymized.csv")


def _load_raw_data() -> pd.DataFrame:
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError("Missing data/raw/patients_raw.csv. Run scripts/generate_data.py first.")
    return pd.read_csv(RAW_DATA_PATH, dtype={"cccd": str, "so_dien_thoai": str})


@app.get("/api/patients/raw")
@require_permission(resource="patient_data", action="read")
async def get_raw_patients(current_user: dict = Depends(get_current_user)):
    """Return raw patient data. Only admin should be able to access this."""
    del current_user
    df = _load_raw_data()
    return {"records": df.head(10).to_dict(orient="records")}


@app.get("/api/patients/anonymized")
@require_permission(resource="training_data", action="read")
async def get_anonymized_patients(current_user: dict = Depends(get_current_user)):
    """Return anonymized patient data for model training."""
    del current_user
    df = _load_raw_data()
    df_anon = anonymizer.anonymize_dataframe(df)
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_anon.to_csv(PROCESSED_DATA_PATH, index=False)
    return {"records": df_anon.head(10).to_dict(orient="records")}


@app.get("/api/metrics/aggregated")
@require_permission(resource="aggregated_metrics", action="read")
async def get_aggregated_metrics(current_user: dict = Depends(get_current_user)):
    """Return aggregate metrics without exposing raw PII."""
    del current_user
    df = _load_raw_data()
    by_condition = df["benh"].value_counts().reset_index()
    by_condition.columns = ["benh", "patient_count"]
    return {
        "total_patients": int(len(df)),
        "patients_by_condition": by_condition.to_dict(orient="records"),
        "avg_test_result": round(float(df["ket_qua_xet_nghiem"].mean()), 2),
    }


@app.delete("/api/patients/{patient_id}")
@require_permission(resource="patient_data", action="delete")
async def delete_patient(patient_id: str, current_user: dict = Depends(get_current_user)):
    """Simulate patient deletion. In the lab this is an RBAC demo only."""
    return {
        "status": "deleted",
        "patient_id": patient_id,
        "performed_by": current_user["username"],
    }


@app.get("/health")
async def health():
    return {"status": "ok", "service": "MedViet Data API"}
