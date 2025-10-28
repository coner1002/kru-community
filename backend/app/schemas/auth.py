from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.models.user import Language

class UserRegister(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    nickname: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=8)
    preferred_lang: Language = Language.KO

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

class OAuthCallback(BaseModel):
    code: str
    state: Optional[str] = None