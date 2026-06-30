"""Anonymization pipeline for MedViet patient data."""
from __future__ import annotations

import hashlib
from typing import Callable

import pandas as pd
from faker import Faker
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

from .detector import build_vietnamese_analyzer, detect_pii

fake = Faker("vi_VN")
Faker.seed(42)


def fake_cccd() -> str:
    return str(fake.random_number(digits=12, fix_len=True))


def fake_vn_phone() -> str:
    prefix = fake.random_element(elements=("03", "05", "07", "08", "09"))
    return prefix + "".join(str(fake.random_digit()) for _ in range(8))


def _hash_value(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class MedVietAnonymizer:
    def __init__(self) -> None:
        self.analyzer = build_vietnamese_analyzer()
        self.anonymizer = AnonymizerEngine()

    def anonymize_text(self, text: str, strategy: str = "replace") -> str:
        """Anonymize text with replace, mask, or hash strategy."""
        text = "" if pd.isna(text) else str(text)
        results = detect_pii(text, self.analyzer)
        if not results:
            return text

        if strategy == "hash":
            return self._hash_detected_spans(text, results)

        if strategy == "mask":
            operators = {
                "DEFAULT": OperatorConfig(
                    "mask",
                    {"chars_to_mask": 8, "masking_char": "*", "from_end": False},
                )
            }
        elif strategy == "replace":
            operators = {
                "PERSON": OperatorConfig("replace", {"new_value": fake.name()}),
                "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": fake.email()}),
                "VN_CCCD": OperatorConfig("replace", {"new_value": fake_cccd()}),
                "VN_PHONE": OperatorConfig("replace", {"new_value": fake_vn_phone()}),
            }
        else:
            raise ValueError(f"Unsupported anonymization strategy: {strategy}")

        anonymized = self.anonymizer.anonymize(text=text, analyzer_results=results, operators=operators)
        return anonymized.text

    @staticmethod
    def _hash_detected_spans(text: str, results: list) -> str:
        output = text
        for result in sorted(results, key=lambda r: r.start, reverse=True):
            original = output[result.start : result.end]
            digest = _hash_value(original)[:16]
            replacement = f"<HASH_{result.entity_type}_{digest}>"
            output = output[: result.start] + replacement + output[result.end :]
        return output

    def anonymize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Anonymize patient dataframe while preserving ML-useful columns."""
        df_anon = df.copy()

        self._replace_column(df_anon, "ho_ten", lambda _: fake.name())
        self._replace_column(df_anon, "cccd", lambda _: fake_cccd())
        self._replace_column(df_anon, "so_dien_thoai", lambda _: fake_vn_phone())
        self._replace_column(df_anon, "email", lambda _: fake.email())
        self._replace_column(df_anon, "dia_chi", lambda _: fake.address().replace("\n", ", "))
        self._replace_column(df_anon, "bac_si_phu_trach", lambda _: fake.name())

        if "ngay_sinh" in df_anon.columns:
            df_anon["ngay_sinh"] = df_anon["ngay_sinh"].apply(self._generalize_birth_date)

        return df_anon

    @staticmethod
    def _replace_column(df: pd.DataFrame, column: str, generator: Callable[[object], str]) -> None:
        if column in df.columns:
            df[column] = df[column].apply(generator)

    @staticmethod
    def _generalize_birth_date(value: object) -> str:
        """Generalize dd/mm/yyyy to a decade bucket such as 1980s."""
        text = "" if pd.isna(value) else str(value)
        year = text[-4:] if len(text) >= 4 else ""
        if year.isdigit():
            return f"{year[:3]}0s"
        return "unknown"

    def calculate_detection_rate(self, original_df: pd.DataFrame, pii_columns: list[str]) -> float:
        """Calculate the percentage of PII cells with at least one detection."""
        total = 0
        detected = 0

        for col in pii_columns:
            if col not in original_df.columns:
                continue
            for value in original_df[col].astype(str):
                total += 1
                results = detect_pii(value, self.analyzer)
                if results:
                    detected += 1

        return detected / total if total > 0 else 0.0


def anonymize_csv(
    input_path: str = "data/raw/patients_raw.csv",
    output_path: str = "data/processed/patients_anonymized.csv",
) -> pd.DataFrame:
    """Load raw patient data, anonymize it, save processed output, and return it."""
    df = pd.read_csv(input_path, dtype={"cccd": str, "so_dien_thoai": str})
    anonymizer = MedVietAnonymizer()
    df_anon = anonymizer.anonymize_dataframe(df)
    df_anon.to_csv(output_path, index=False)
    return df_anon
