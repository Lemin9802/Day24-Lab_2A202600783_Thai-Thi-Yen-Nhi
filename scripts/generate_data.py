"""Generate fake MedViet patient records for Lab 24.

The generated CSV is intentionally ignored by git because raw patient-like data,
even fake data, should not be part of the final submission package.
"""
from __future__ import annotations

import random
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker("vi_VN")
Faker.seed(42)
random.seed(42)

RAW_DATA_PATH = Path("data/raw/patients_raw.csv")


def fake_cccd() -> str:
    """Return a 12-digit CCCD-like value.

    The first digit is kept non-zero so pandas does not silently trim the value
    to 11 digits when learners open the CSV without dtype hints.
    """
    return str(random.randint(1, 9)) + "".join(str(random.randint(0, 9)) for _ in range(11))


def fake_vn_phone() -> str:
    return "0" + random.choice(["3", "5", "7", "8", "9"]) + "".join(
        str(random.randint(0, 9)) for _ in range(8)
    )


def generate_patients(n: int = 200) -> pd.DataFrame:
    records: list[dict[str, object]] = []
    for _ in range(n):
        records.append(
            {
                "patient_id": fake.uuid4(),
                "ho_ten": fake.name(),
                "cccd": fake_cccd(),
                "ngay_sinh": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%d/%m/%Y"),
                "so_dien_thoai": fake_vn_phone(),
                "email": fake.email(),
                "dia_chi": fake.address().replace("\n", ", "),
                "benh": random.choice(["Tiểu đường", "Huyết áp cao", "Tim mạch", "Khỏe mạnh"]),
                "ket_qua_xet_nghiem": round(random.uniform(3.5, 12.0), 2),
                "bac_si_phu_trach": fake.name(),
                "ngay_kham": fake.date_this_year().strftime("%d/%m/%Y"),
            }
        )
    return pd.DataFrame(records)


def main() -> None:
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = generate_patients()
    df.to_csv(RAW_DATA_PATH, index=False)
    print(f"Generated {len(df)} patient records at {RAW_DATA_PATH}")
    print(df.head(3))
    print("\nPII columns: ho_ten, cccd, ngay_sinh, so_dien_thoai, email, dia_chi, bac_si_phu_trach")
    print("Sensitive non-PII columns kept for ML: benh, ket_qua_xet_nghiem")


if __name__ == "__main__":
    main()
