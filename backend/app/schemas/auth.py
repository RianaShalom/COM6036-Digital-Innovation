from pydantic import BaseModel


# Defines the JWT access token returned after successful authentication.
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"