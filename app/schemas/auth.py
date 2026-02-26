from pydantic import BaseModel, EmailStr, Field, field_validator

class LoginRequest(BaseModel):
    
    email: EmailStr
    password: str = Field(min_length=8)
    
    @field_validator("email")
    @classmethod
    def normalize_email(cls, email: str) -> str:
        return email.strip().lower()
    
    @field_validator("password")
    @classmethod
    def normalize_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        return password
    
class TokenResponse(BaseModel):
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class RefreshRequest(BaseModel):
    
    refresh_token: str
    