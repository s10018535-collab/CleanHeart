import hashlib
import hmac

from config import OFFICER_PASSWORD_HASH, OFFICER_SALT, PBKDF2_ITERATIONS


def verify_officer_password(password: str) -> bool:
    attempt = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        OFFICER_SALT.encode("utf-8"),
        PBKDF2_ITERATIONS,
    ).hex()
    return hmac.compare_digest(attempt, OFFICER_PASSWORD_HASH)
