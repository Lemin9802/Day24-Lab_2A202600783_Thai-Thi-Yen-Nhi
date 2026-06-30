"""Data quality validation for MedViet patient datasets."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd

VALID_CONDITIONS = {"Tiểu đường", "Huyết áp cao", "Tim mạch", "Khỏe mạnh"}
EMAIL_RE = re.compile(r"(?i)^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$")


def build_patient_expectation_suite() -> dict[str, Any]:
    """Return the expectation suite definition used by this lab.

    The README mentions Great Expectations; this dictionary mirrors the required
    checks and keeps the lab runnable even when GE APIs differ by version.
    """
    return {
        "suite_name": "patient_data_suite",
        "expectations": [
            {"column": "patient_id", "expectation": "not_null"},
            {"column": "cccd", "expectation": "length_between", "min": 11, "max": 12},
            {"column": "ket_qua_xet_nghiem", "expectation": "between", "min": 0, "max": 50},
            {"column": "benh", "expectation": "in_set", "value_set": sorted(VALID_CONDITIONS)},
            {"column": "email", "expectation": "email_regex"},
            {"column": "patient_id", "expectation": "unique"},
        ],
    }


def validate_anonymized_data(filepath: str, original_filepath: str = "data/raw/patients_raw.csv") -> dict[str, Any]:
    """Validate anonymized data and return a submission-friendly summary."""
    path = Path(filepath)
    df = pd.read_csv(path, dtype={"cccd": str, "so_dien_thoai": str})
    results: dict[str, Any] = {
        "success": True,
        "failed_checks": [],
        "stats": {"total_rows": len(df), "columns": list(df.columns)},
    }

    def fail(message: str) -> None:
        results["success"] = False
        results["failed_checks"].append(message)

    required_columns = ["patient_id", "benh", "ket_qua_xet_nghiem", "cccd", "so_dien_thoai", "email"]
    for column in required_columns:
        if column not in df.columns:
            fail(f"Missing required column: {column}")
        elif df[column].isna().any():
            fail(f"Null values found in column: {column}")

    if "patient_id" in df.columns and df["patient_id"].duplicated().any():
        fail("Duplicate patient_id values found")

    if "benh" in df.columns:
        invalid = set(df["benh"].dropna()) - VALID_CONDITIONS
        if invalid:
            fail(f"Invalid disease labels: {sorted(invalid)}")

    if "ket_qua_xet_nghiem" in df.columns:
        values = pd.to_numeric(df["ket_qua_xet_nghiem"], errors="coerce")
        if values.isna().any() or not values.between(0, 50).all():
            fail("ket_qua_xet_nghiem must be numeric and between 0 and 50")

    # Processed data should not contain raw 12-digit CCCD values copied from the
    # input. Fake CCCDs can still be 12 digits, so compare against originals.
    original_path = Path(original_filepath)
    if original_path.exists() and "cccd" in df.columns:
        original_df = pd.read_csv(original_path, dtype={"cccd": str, "so_dien_thoai": str})
        original_cccds = set(original_df["cccd"].astype(str)) if "cccd" in original_df.columns else set()
        leaked_cccds = set(df["cccd"].astype(str)) & original_cccds
        if leaked_cccds:
            fail(f"Original CCCD values leaked into anonymized data: {len(leaked_cccds)}")

        if len(original_df) != len(df):
            fail(f"Row count changed: original={len(original_df)}, anonymized={len(df)}")

    return results


if __name__ == "__main__":
    print(validate_anonymized_data("data/processed/patients_anonymized.csv"))
