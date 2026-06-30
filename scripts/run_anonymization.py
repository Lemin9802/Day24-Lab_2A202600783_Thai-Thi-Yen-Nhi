"""Run the MedViet anonymization pipeline and print detection metrics."""
from __future__ import annotations

import sys
from pathlib import Path

# Allow direct execution with `python scripts/run_anonymization.py` on Windows,
# where Python otherwise places only the `scripts/` directory on sys.path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from src.pii.anonymizer import MedVietAnonymizer

RAW_PATH = Path("data/raw/patients_raw.csv")
PROCESSED_PATH = Path("data/processed/patients_anonymized.csv")


def main() -> None:
    if not RAW_PATH.exists():
        raise FileNotFoundError("Run `python scripts/generate_data.py` first.")

    df = pd.read_csv(RAW_PATH, dtype={"cccd": str, "so_dien_thoai": str})
    anonymizer = MedVietAnonymizer()
    pii_columns = ["ho_ten", "cccd", "so_dien_thoai", "email"]
    rate = anonymizer.calculate_detection_rate(df, pii_columns)
    print(f"Detection rate: {rate:.2%}")

    df_anon = anonymizer.anonymize_dataframe(df)
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_anon.to_csv(PROCESSED_PATH, index=False)
    print(f"Saved anonymized data to {PROCESSED_PATH}")
    print(df_anon.head(3))


if __name__ == "__main__":
    main()
