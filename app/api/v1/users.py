from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshRequest, TokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.core.user import authenticate_user, create_user, get_user_by_uid
from app.utils.jwt import create_access_token, create_refresh_token, decode_token


router = APIRouter()

user_dependency = Annotated[User, Depends(get_current_user)]

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: user_dependency) -> User:
    
    return current_user
