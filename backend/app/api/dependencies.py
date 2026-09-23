from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.user import User
from app.services import user_service


# Defines the endpoint used by OAuth2 clients to obtain an access token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# Retrieves the authenticated user from the JWT supplied with the request.
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user_id = UUID(decode_access_token(token))
    except (ValueError, TypeError, jwt.InvalidTokenError):
        raise credentials_exception

    user = user_service.get_user(db, user_id)

    if user is None:
        raise credentials_exception

    return user