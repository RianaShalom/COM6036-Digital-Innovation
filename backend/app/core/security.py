from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

# Creates the password hashing utility used to securely store passwords.
password_hash = PasswordHash.recommended()

# Defines the signing algorithm used to create and validate JWT access tokens.
ALGORITHM = "HS256"


# Hashes a plaintext password before it is stored in the database.
def hash_password(password: str) -> str:
    return password_hash.hash(password)


# Checks whether a supplied plaintext password matches a stored password hash.
def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


# Creates a JWT access token containing the authenticated user's ID.
def create_access_token(subject: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM,
    )


# Decodes a JWT access token and returns the user ID stored in its subject.
def decode_access_token(token: str) -> str:
    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[ALGORITHM],
    )

    subject = payload.get("sub")

    if not subject:
        raise ValueError("Token does not contain a subject.")

    return subject
