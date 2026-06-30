"""Local envelope encryption demo for Lab 24.

Production systems should use a managed KMS/HSM instead of a local .vault_key
file. This module is intentionally small so learners can understand the flow:
KEK encrypts DEK; DEK encrypts data.
"""
from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class SimpleVault:
    """Mimic the envelope encryption pattern for local development."""

    def __init__(self, master_key_path: str = ".vault_key") -> None:
        self.master_key_path = Path(master_key_path)
        self.kek = self._load_or_create_kek()

    def _load_or_create_kek(self) -> bytes:
        if self.master_key_path.exists():
            return base64.b64decode(self.master_key_path.read_bytes())

        kek = os.urandom(32)  # 256-bit key
        self.master_key_path.write_bytes(base64.b64encode(kek))
        try:
            os.chmod(self.master_key_path, 0o600)
        except OSError:
            # chmod may fail on some Windows filesystems; the lab still works.
            pass
        return kek

    def generate_dek(self) -> tuple[bytes, bytes]:
        plaintext_dek = os.urandom(32)
        aesgcm = AESGCM(self.kek)
        nonce = os.urandom(12)
        encrypted_dek = nonce + aesgcm.encrypt(nonce, plaintext_dek, None)
        return plaintext_dek, encrypted_dek

    def decrypt_dek(self, encrypted_dek: bytes) -> bytes:
        nonce = encrypted_dek[:12]
        ciphertext = encrypted_dek[12:]
        aesgcm = AESGCM(self.kek)
        return aesgcm.decrypt(nonce, ciphertext, None)

    def encrypt_data(self, plaintext: str) -> dict[str, str]:
        plaintext_dek, encrypted_dek = self.generate_dek()
        aesgcm = AESGCM(plaintext_dek)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
        del plaintext_dek

        return {
            "encrypted_dek": base64.b64encode(encrypted_dek).decode("utf-8"),
            "ciphertext": base64.b64encode(nonce + ciphertext).decode("utf-8"),
            "algorithm": "AES-256-GCM",
        }

    def decrypt_data(self, encrypted_payload: dict[str, str]) -> str:
        encrypted_dek = base64.b64decode(encrypted_payload["encrypted_dek"])
        ciphertext_with_nonce = base64.b64decode(encrypted_payload["ciphertext"])

        plaintext_dek = self.decrypt_dek(encrypted_dek)
        nonce = ciphertext_with_nonce[:12]
        ciphertext = ciphertext_with_nonce[12:]
        aesgcm = AESGCM(plaintext_dek)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        del plaintext_dek
        return plaintext.decode("utf-8")

    def encrypt_column(self, df: Any, column: str):
        """Encrypt one DataFrame column and return a modified copy."""
        df = df.copy()
        df[column] = df[column].apply(lambda x: json.dumps(self.encrypt_data(str(x)), ensure_ascii=False))
        return df


if __name__ == "__main__":
    vault = SimpleVault()
    original = "Nguyen Van A - CCCD: 012345678901"
    encrypted = vault.encrypt_data(original)
    decrypted = vault.decrypt_data(encrypted)
    assert decrypted == original, "Encryption round-trip FAILED!"
    print("Encryption test passed")
