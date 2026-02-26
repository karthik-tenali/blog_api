from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import LoginRequest, RefreshRequest, TokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.core.user import authenticate_user, create_user, get_user_by_uid
from app.utils.jwt import create_access_token, create_refresh_token, decode_token

router = APIRouter()

db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_new_user(input_data: UserCreate, db: db_dependency):
    try:
        user = await create_user(
            db,
            input_data.email,
            input_data.username,
            input_data.first_name,
            input_data.last_name,
            input_data.password
        )
    except ValueError as e:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=str(e)
            )
    
    return user

@router.post("/login", response_model=TokenResponse)
async def login_user(input_data: LoginRequest, db: db_dependency):
    user = await authenticate_user(db, input_data.email, input_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=" Invalid username or password"
        )
    
    access_token = create_access_token(user.uid)
    refresh_token = create_refresh_token(user.uid)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    
@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(input_data: RefreshRequest, db: db_dependency):
    
    payload = decode_token(input_data.refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
        
    uid = payload.get("sub")
    
    user = await get_user_by_uid(db, uid) # type: ignore
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )  
         
    access_token = create_access_token(user.uid)

    return TokenResponse(
        access_token=access_token,
        refresh_token=input_data.refresh_token,
    )