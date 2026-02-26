import uuid
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

class UserCreate(BaseModel):
    
    username: str = Field(min_length=3)
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=8)
    
    @field_validator("email")
    @classmethod
    def normalize_email(cls, email: str) -> str:
        return email.strip().lower()
    
    @field_validator("username")
    @classmethod
    def normalize_username(cls, username: str) -> str:
        username =  username.strip()
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        return username

    @field_validator("first_name", "last_name")
    @classmethod
    def normalize_names(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 1:
            raise ValueError("Name cannot be empty")
        return v
    
    @field_validator("password")
    @classmethod
    def normalize_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        return password

class UserResponse(BaseModel):
    
    uid: uuid.UUID
    first_name: str
    last_name: str
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
            

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @field_validator("first_name", "last_name")
    @classmethod
    def normalize_names(cls, v: str | None):
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        return v

    