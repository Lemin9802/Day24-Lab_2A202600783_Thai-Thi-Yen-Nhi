from __future__ import annotations

import pandas as pd
import pytest

from scripts.generate_data import generate_patients
from src.pii.anonymizer import MedVietAnonymizer


@pytest.fixture
def anonymizer() -> MedVietAnonymizer:
    return MedVietAnonymizer()


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return generate_patients(50)


class TestPIIDetection:
    def test_cccd_detected(self, anonymizer: MedVietAnonymizer) -> None:
        text = "Bệnh nhân Nguyen Van A, CCCD: 012345678901"
        results = anonymizer.analyzer.analyze(text=text, language="vi", entities=["VN_CCCD"])
        assert len(results) >= 1
        assert results[0].entity_type == "VN_CCCD"

    def test_phone_detected(self, anonymizer: MedVietAnonymizer) -> None:
        text = "Liên hệ: 0912345678"
        results = anonymizer.analyzer.analyze(text=text, language="vi", entities=["VN_PHONE"])
        assert len(results) >= 1
        assert results[0].entity_type == "VN_PHONE"

    def test_email_detected(self, anonymizer: MedVietAnonymizer) -> None:
        text = "Email: nguyenvana@gmail.com"
        results = anonymizer.analyzer.analyze(text=text, language="vi", entities=["EMAIL_ADDRESS"])
        assert len(results) >= 1
        assert results[0].entity_type == "EMAIL_ADDRESS"

    def test_detection_rate_above_95_percent(self, anonymizer: MedVietAnonymizer, sample_df: pd.DataFrame) -> None:
        pii_columns = ["ho_ten", "cccd", "so_dien_thoai", "email"]
        rate = anonymizer.calculate_detection_rate(sample_df, pii_columns)
        print(f"\nDetection rate: {rate:.2%}")
        assert rate >= 0.95, f"Detection rate {rate:.2%} < 95%"


class TestAnonymization:
    def test_pii_not_in_output(self, anonymizer: MedVietAnonymizer, sample_df: pd.DataFrame) -> None:
        df_anon = anonymizer.anonymize_dataframe(sample_df)
        output_text = df_anon.astype(str).to_string(index=False)
        for original_cccd in sample_df["cccd"]:
            assert str(original_cccd) not in output_text
        for original_phone in sample_df["so_dien_thoai"]:
            assert str(original_phone) not in output_text

    def test_non_pii_columns_unchanged(self, anonymizer: MedVietAnonymizer, sample_df: pd.DataFrame) -> None:
        df_anon = anonymizer.anonymize_dataframe(sample_df)
        pd.testing.assert_series_equal(sample_df["benh"], df_anon["benh"], check_names=False)
        pd.testing.assert_series_equal(
            sample_df["ket_qua_xet_nghiem"],
            df_anon["ket_qua_xet_nghiem"],
            check_names=False,
        )
        pd.testing.assert_series_equal(sample_df["patient_id"], df_anon["patient_id"], check_names=False)
